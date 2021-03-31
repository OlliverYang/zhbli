"""
二分法目标跟踪
必须要多层融合，因为第一个隐层没办法学习到有用的东西。考虑反卷积？
目前方法的缺点：如果高层决定好采用哪个区域了，则底层就不需要对无关区域计算损失了。而且不这么做的话是错的，比如底层背景有小区域响应非常高，但是高层中该小区域想应高也许没有意义。
- 可以用  mask 来实现。
优点：只要最大值能对上，就不计算损失了，减少容易样本对训练的影响。
优点：假设有128*128的特征图，传统方法要计算128*128个位置，我们只需要计算4*8=32个位置。
优点：使用深层监督。
"""


import numpy as np
import torch
import torch.nn.functional as F
from sigmoid_ce_retina import SigmoidCrossEntropyRetina


def _gather_feat(feat, ind, mask=None):
    dim  = feat.size(2)
    ind  = ind.unsqueeze(2).expand(ind.size(0), ind.size(1), dim)
    feat = feat.gather(1, ind)
    if mask is not None:
        mask = mask.unsqueeze(2).expand_as(feat)
        feat = feat[mask]
        feat = feat.view(-1, dim)
    return feat


def _tranpose_and_gather_feat(feat, ind):
    feat = feat.permute(0, 2, 3, 1).contiguous()
    feat = feat.view(feat.size(0), -1, feat.size(3))
    feat = _gather_feat(feat, ind)
    return feat


def xcorr_depthwise(x, kernel):
    r"""
    Depthwise cross correlation. e.g. used for template matching in Siamese tracking network

    Arguments
    ---------
    x: torch.Tensor
        feature_x (e.g. search region feature in SOT)
    kernel: torch.Tensor
        feature_z (e.g. template feature in SOT)

    Returns
    -------
    torch.Tensor
        cross-correlation result
    """
    batch = int(kernel.size(0))
    channel = int(kernel.size(1))
    x = x.reshape(1, int(batch * channel), int(x.size(2)), int(x.size(3)))
    kernel = kernel.reshape(batch * channel, 1, int(kernel.size(2)),
                         int(kernel.size(3)))
    out = F.conv2d(x, kernel, groups=batch * channel)
    out = out.reshape(batch, channel, int(out.size(2)), int(out.size(3)))
    return out


class Model(torch.nn.Module):
    def __init__(self, cfg):
        super(Model, self).__init__()
        self.cfg = cfg
        self.criteria = SigmoidCrossEntropyRetina()

        """构建网络"""
        self.hidden = torch.nn.ModuleList([])
        self.head = torch.nn.ModuleList([])
        self.decoder = torch.nn.ModuleList([])
        for i in range(8):
            if i == 0:
                in_channel = 3
                stride = 1
                deconv_padding = 2
            else:
                in_channel = self.cfg['OUT_CHANNEL']
                stride = 2
                deconv_padding = 1
            self.hidden.extend([
                torch.nn.Sequential(
                    torch.nn.Conv2d(in_channel, self.cfg['OUT_CHANNEL'], 3, dilation=1, stride=stride, padding=1),
                    torch.nn.BatchNorm2d(self.cfg['OUT_CHANNEL']),
                    torch.nn.ReLU()
                    )
            ])
            self.head.extend([
                torch.nn.Sequential(
                    torch.nn.Conv2d(self.cfg['OUT_CHANNEL'], 1, 1, padding=0),
                    torch.nn.BatchNorm2d(1)
                )
            ])
            self.decoder.extend([
                torch.nn.Sequential(
                    torch.nn.ConvTranspose2d(self.cfg['OUT_CHANNEL'], self.cfg['OUT_CHANNEL'], 4, dilation=1, stride=2, padding=deconv_padding),
                    torch.nn.BatchNorm2d(self.cfg['OUT_CHANNEL']),
                    torch.nn.ReLU()
                )
            ])
            # 反卷积知识：可以根据反卷积的 o(输入分辨率) s（步长） k（核大小） p（padding） 参数来计算反卷积的输出i。公式如下：i = ( o − 1 ) ∗ s + k − 2 ∗ p

    def forward(self, x, img_h, img_w, anno_xywh):
        """"""
        anno_xywh = anno_xywh.cpu().data.numpy()
        img_w = img_w.cpu().data.numpy()
        img_h = img_h.cpu().data.numpy()

        """进行编码"""
        encoder = []
        for i in range(len(self.hidden)):
            x = self.hidden[i](x)

            """计算目标在特征图上的位置"""
            with torch.no_grad():
                scale_x = x.shape[3] / img_w
                scale_y = x.shape[2] / img_h
                x1 = anno_xywh[:, 0]  # 相对于原始输入图像。未经过任何缩放。
                y1 = anno_xywh[:, 1]
                w = anno_xywh[:, 2]
                h = anno_xywh[:, 3]
                cx_abs = np.minimum((x1 + w / 2) * scale_x, x.shape[3] - 1).astype(np.int)
                cy_abs = np.minimum((y1 + h / 2) * scale_y, x.shape[2] - 1).astype(np.int)  # 绝对位置

            """提取目标位置的特征向量"""
            obj_vector = x[list(range(x.shape[0])), :, cy_abs, cx_abs].unsqueeze(2).unsqueeze(3)  # 这个索引方法很关键

            """执行互相关"""
            x = xcorr_depthwise(x, obj_vector)

            encoder.append(x)
        """进行编码"""

        """进行反卷积解码"""
        decoder = []
        for i in range(len(self.decoder)):
            x = self.decoder[i](x) + encoder[len(encoder)-1-i]
            decoder.append(x)

        heat_map_np = []
        h_anchor = 0  # 绝对位置
        w_anchor = 0
        for i in range(len(self.head)):
            heat_map = self.head[i](decoder[i])
            heat_map_np.append(heat_map.cpu().data.numpy())

            """裁剪成2*2的相对图像"""
            if i > 0:
                heat_map_cropped = torch.cat([heat_map[i_, :, h_anchor_:h_anchor_ + 2, w_anchor_:w_anchor_ + 2].unsqueeze(0) for i_, (h_anchor_, w_anchor_) in enumerate(zip(h_anchor, w_anchor))])
            else:
                heat_map_cropped = heat_map[:, :, h_anchor:h_anchor + 2, w_anchor:w_anchor + 2]  # 绝对位置

            """得到预测的目标在 2*2 特征图上的位置"""
            predicted_indices = torch.argmax(heat_map_cropped.reshape(heat_map_cropped.shape[0], -1), dim=1)  # 相对位置

            """得到目标在特征图上的GT位置（绝对位置）"""
            with torch.no_grad():
                scale_x = heat_map.shape[3] / img_w
                scale_y = heat_map.shape[2] / img_h
            x1 = anno_xywh[:, 0]  # 相对于原始输入图像。未经过任何缩放。
            y1 = anno_xywh[:, 1]
            w = anno_xywh[:, 2]
            h = anno_xywh[:, 3]
            cx_abs = np.minimum((x1 + w / 2) * scale_x, heat_map.shape[3] - 1).astype(np.int)
            cy_abs = np.minimum((y1 + h / 2) * scale_y, heat_map.shape[2] - 1).astype(np.int)

            """得到目标在 2*2 heat_map 上的GT位置(相对位置)"""
            cx = cx_abs - w_anchor
            cy = cy_abs - h_anchor
            gt_indices = cy * heat_map_cropped.shape[3] + cx

            """如果对应点已经最大了，则不需要计算损失，否则就需要计算"""
            # 只要彼批次里面有一个不相等的，则计算损失
            if np.any(gt_indices != predicted_indices.cpu().data.numpy()) or i == len(self.head) - 1:  # if torch.max(heat_map) > heat_map[:, :, cy, cx] or i == len(self.head) - 1:
                """生成计算损失所用的gt（尺寸2*2）"""
                mask = gt_indices != predicted_indices.cpu().data.numpy()

                gt = torch.zeros_like(heat_map_cropped, requires_grad=False, dtype=torch.long)
                gt[list(range(gt.shape[0])), :, cy, cx] = 1  # 顺序不要写反了~~

                """计算损失时，始终是4个点里选一个点(其实不太好实现。因为对于256*256的heatmap，怎么快速找到对应的4*4区域？)"""
                loss = self.criteria.forward(heat_map_cropped, gt, mask)
                break
            else:
                """如果预测对了，就到上一层去"""
                h_anchor = 2 * cy_abs
                w_anchor = 2 * cx_abs

        return i, loss, heat_map_np

    def test(self, x, img_h, img_w):
        """进行编码"""
        encoder = []
        for i in range(len(self.hidden)):
            x = self.hidden[i](x)
            encoder.append(x)

        """进行反卷积解码"""
        decoder = []
        for i in range(len(self.decoder)):
            x = self.decoder[i](x) + encoder[len(encoder) - 1 - i]
            decoder.append(x)

        heat_map_np = []
        prediction_cxy = []
        h_anchor = 0  # 绝对位置
        w_anchor = 0
        for i in range(len(self.head)):
            heat_map = self.head[i](decoder[i])
            heat_map_np.append(heat_map.cpu().data.numpy())

            """裁剪成2*2的相对图像"""
            heat_map_cropped = heat_map[:, :, h_anchor:h_anchor + 2, w_anchor:w_anchor + 2]  # 绝对位置

            """得到预测的目标在 2*2 特征图上的位置"""
            predicted_indices = torch.argmax(heat_map_cropped).item()  # 相对位置
            cy = predicted_indices // heat_map_cropped.shape[3]
            cx = predicted_indices % heat_map_cropped.shape[3]

            """得到预测的目标在特征图上的绝对位置"""
            cy_abs = cy + h_anchor
            cx_abs = cx + w_anchor
            prediction_cxy.append((int(cx_abs), int(cy_abs)))

            h_anchor = 2 * cy_abs
            w_anchor = 2 * cx_abs

        return heat_map_np, prediction_cxy