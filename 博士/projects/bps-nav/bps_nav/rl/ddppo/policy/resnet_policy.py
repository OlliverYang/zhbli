#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Dict, List, Tuple, Optional

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from bps_nav.common.utils import Flatten, ResizeCenterCropper
from bps_nav.rl.ddppo.policy import regnetx, resnet
from bps_nav.rl.models.rnn_state_encoder import build_rnn_state_encoder
from bps_nav.rl.ppo import Net, Policy
from bps_nav.rl.ddppo.policy.resnet import FixupBasicBlock


try:
    from tensorrt_policy import TensorRTPolicy
except:
    TensorRTPolicy = None
    print("Failed to import TensorRT, no inference acceleration")


def standardize_weights(w):
    orig_size = w.size()
    w = w.view(w.size(0), -1)

    w_mean = w.mean(1, keepdim=True)
    w = w - w_mean
    w_var = (w * w).mean(1, keepdim=True)

    w = w * torch.rsqrt(w_var + 1e-5)

    return w


class ResNetPolicy(Policy):
    def __init__(
        self,
        observation_space,
        action_space,
        hidden_size=512,
        num_recurrent_layers=1,
        rnn_type="GRU",
        resnet_baseplanes=32,
        backbone="resnet18",
        use_avg_pool=False,
        obs_transform=ResizeCenterCropper(size=(256, 256)),
    ):
        super().__init__(
            ResNetNet(
                observation_space=observation_space,
                action_space=action_space,
                hidden_size=hidden_size,
                num_recurrent_layers=num_recurrent_layers,
                rnn_type=rnn_type,
                backbone=backbone,
                resnet_baseplanes=resnet_baseplanes,
                use_avg_pool=use_avg_pool,
                obs_transform=obs_transform,
            ),
            observation_space,
            action_space.n,
        )

    def init_trt(self, inference_batch_size):
        if TensorRTPolicy == None:
            return

        assert (
            self.ac.net.visual_encoder._n_input_rgb == 0
            or self.ac.net.visual_encoder._n_input_depth == 0
        )

        self.accelerated_net = TensorRTPolicy(
            inference_batch_size,
            self.ac.net.visual_encoder.spatial_size,
            self.ac.net.visual_encoder.num_baseplanes,
            self.ac.net.visual_encoder.output_shape[0],
            self.ac.net._hidden_size,
            self.ac.net.visual_encoder._n_input_rgb > 0,
            [1, 1, 1, 1],  # Assumes resnet9
            ResNetNet.visual_weights_cpu(self.ac.net),
        )

        import bps_pytorch 

        self.accel_out = bps_pytorch.make_fcout_tensor(
            self.accelerated_net.get_result_device_ptr(),
            0,
            inference_batch_size,
            self.ac.net._hidden_size,
        )

    def get_trt_weights(self):
        return ResNetNet.visual_weights_cpu(self.ac.net)

    def update_trt_weights(self, weights):
        if self.accelerated_net == None:
            return

        self.accelerated_net.update_weights(weights)


class ResNetEncoder(nn.Module):
    def __init__(
        self,
        observation_space,
        baseplanes=32,
        ngroups=16,
        backbone=None,
        use_avg_pool=False,
        hidden_size=512,
        obs_transform=ResizeCenterCropper(size=(256, 256)),
    ):
        super().__init__()

        if "resne" in backbone:
            make_backbone = getattr(resnet, backbone)
        elif "regne" in backbone:
            make_backbone = getattr(regnetx, backbone)

        if "rgb" in observation_space.spaces:
            self._n_input_rgb = observation_space.spaces["rgb"].shape[0]
            self.spatial_size = observation_space.spaces["rgb"].shape[1:]
        else:
            self._n_input_rgb = 0

        if "depth" in observation_space.spaces:
            self._n_input_depth = observation_space.spaces["depth"].shape[0] + 10
            self.spatial_size = observation_space.spaces["depth"].shape[1:]
        else:
            self._n_input_depth = 0

        self.num_baseplanes = baseplanes
        if not self.is_blind:
            input_channels = self._n_input_depth + self._n_input_rgb
            self.backbone = make_backbone(input_channels, baseplanes, ngroups)

            flat_size = 1024
            if not use_avg_pool:
                initial_pool_size = 0
                self.spatial_size = tuple(s // 4 for s in self.spatial_size)
                for _ in range(self.backbone.num_compression_stages - 2):
                    self.spatial_size = tuple(
                        int((s + 2 - 2 - 1) / 2 + 1) for s in self.spatial_size
                    )

                final_compression_channels = flat_size / np.prod(self.spatial_size)
                final_compression_channels = int(
                    round(final_compression_channels / ngroups) * ngroups
                )

                compression_layers = [
                    nn.Conv2d(
                        self.backbone.final_channels,
                        out_channels=final_compression_channels,
                        kernel_size=3,
                        padding=1,
                        bias=not self.backbone.use_normalization,
                    ),
                ]

                if self.backbone.use_normalization:
                    compression_layers.append(
                        nn.GroupNorm(ngroups, final_compression_channels,),
                    )

                compression_layers.append(nn.ReLU(True))

                self.compression = nn.Sequential(*compression_layers)

                self.output_shape = (final_compression_channels, *self.spatial_size)
            else:
                compression_layers = [
                    nn.Conv2d(
                        self.backbone.final_channels,
                        out_channels=flat_size,
                        kernel_size=1,
                        bias=not self.backbone.use_normalization,
                    )
                ]

                if self.backbone.use_normalization:
                    compression_layers.append(nn.GroupNorm(ngroups, flat_size))

                compression_layers += [nn.ReLU(True), nn.AdaptiveAvgPool2d(1)]

                self.compression = nn.Sequential(*compression_layers)

                self.output_shape = (flat_size, 1, 1)

        self.layer_init()

    @property
    def is_blind(self):
        return self._n_input_rgb + self._n_input_depth == 0

    def layer_init(self):
        num_fixups = 0
        for m in self.modules():
            if isinstance(m, FixupBasicBlock):
                num_fixups += 1

        # Just use default initialization
        if num_fixups == 0:
            return

        for m in self.modules():
            if isinstance(m, FixupBasicBlock):
                m.layer_init(num_fixups)

    def forward(self, observations: Dict[str, torch.Tensor]) -> torch.Tensor:
        cnn_input: List[torch.Tensor] = []
        if "rgb" in observations:
            cnn_input.append(observations["rgb"])

        if "depth" in observations:
            cnn_input.append(observations["depth"])

        if len(cnn_input) == 1:
            x = cnn_input[0]
        else:
            x = torch.cat(cnn_input, 1)

        cnn_input = []

        x = self.backbone(x)
        x = self.compression(x)

        return x


class ResNetNet(Net):
    """Network which passes the input image through CNN and concatenates
    goal vector with CNN's output and passes that through RNN.
    """

    def __init__(
        self,
        observation_space,
        action_space,
        hidden_size,
        num_recurrent_layers,
        rnn_type,
        backbone,
        resnet_baseplanes,
        use_avg_pool,
        obs_transform=ResizeCenterCropper(size=(256, 256)),
    ):
        super().__init__()
        self.extra_sensor_names = []

        self.prev_action_embedding = nn.Embedding(action_space.n + 1, 32)
        self._n_prev_action = 32
        rnn_input_size = self._n_prev_action

        if "pointgoal_with_gps_compass" in observation_space.spaces:
            n_input_goal = 3
            self.tgt_embeding = nn.Linear(n_input_goal, 32)
            rnn_input_size += 32
        else:
            self.tgt_embeding = nn.Sequential()

        self._hidden_size = hidden_size

        self.visual_encoder = ResNetEncoder(
            observation_space,
            baseplanes=resnet_baseplanes,
            ngroups=resnet_baseplanes // 2,
            backbone=backbone,
            use_avg_pool=use_avg_pool,
            hidden_size=hidden_size,
            obs_transform=obs_transform,
        )

        if not self.visual_encoder.is_blind:
            self.visual_fc = nn.Sequential(
                nn.Flatten(),
                nn.Linear(
                    int(np.prod(self.visual_encoder.output_shape)),
                    self._hidden_size,
                    bias=False,
                ),
                nn.LayerNorm(self._hidden_size),
                nn.ReLU(True),
            )

        self.state_encoder = build_rnn_state_encoder(
            (0 if self.is_blind else self._hidden_size) + rnn_input_size,
            self._hidden_size,
            rnn_type=rnn_type,
            num_layers=num_recurrent_layers,
        )

        self.train()

    @property
    def output_size(self):
        return self._hidden_size

    @property
    def is_blind(self):
        return self.visual_encoder.is_blind

    @property
    def num_recurrent_layers(self):
        return self.state_encoder.num_recurrent_layers

    def forward(
        self,
        observations: Dict[str, torch.Tensor],
        rnn_hidden_states,
        prev_actions,
        masks,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        return self.rnn_forward(
            self.visual_forward(observations),
            rnn_hidden_states,
            prev_actions,
            masks,
            observations["pointgoal_with_gps_compass"]
            if "pointgoal_with_gps_compass" in observations
            else None,
        )

    @torch.jit.export
    def visual_forward(
        self, observations: Dict[str, torch.Tensor],
    ):
        visual_feats = self.visual_encoder(observations)

        return self.visual_fc(visual_feats)

    @torch.jit.export
    def rnn_forward(
        self,
        tensorrt_output,
        rnn_hidden_states,
        prev_actions,
        masks,
        goal_observations: Optional[torch.Tensor] = None,
    ):
        inputs: List[torch.Tensor] = [tensorrt_output]
        if goal_observations is not None:
            goal_observations = torch.stack(
                [
                    goal_observations[:, 0],
                    torch.cos(-goal_observations[:, 1]),
                    torch.sin(-goal_observations[:, 1]),
                ],
                -1,
            )
            goal_observations = self.tgt_embeding(goal_observations)
            inputs.append(goal_observations)

        prev_actions = torch.where(masks, prev_actions + 1, prev_actions.new_zeros(()))
        prev_actions = self.prev_action_embedding(prev_actions.view(-1))
        inputs.append(prev_actions)

        x = torch.cat(inputs, 1)
        x, rnn_hidden_states = self.state_encoder(x, rnn_hidden_states, masks)

        return x, rnn_hidden_states

    @staticmethod
    def visual_weights_cpu(net):
        cpu_weights = []
        for param in net.visual_encoder.parameters():
            cpu_weights.append(param.detach().cpu().numpy())
        for param in net.visual_fc.parameters():
            cpu_weights.append(param.detach().cpu().numpy())

        return cpu_weights
