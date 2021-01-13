---
title: >-
  [BMVC2017] Online Adaptation of Convolutional Neural Networks for Video Object
  Segmentation
date: 2020-05-08 16:39:36
tags:
- BWVC2017
- Video Object Segmentation
mathjax: true
---

## Abstract

现有视频目标分割算法的问题：最近的 one-shot video object segmentation (OSVOS) 算法仅在第一帧微调，但是在测试过程中对网络不再调整，因此无法适应表观的巨大变化。

本文的解决方案：提出 Online Adaptive Video Object Segmentation (OnAVOS)，基于网络置信度和 spatial configuration 选择训练样本，对网络进行在线更新。

## Introduction

OnAVOS 基于在线选择的训练样本更新神经网络。为了避免漂移，选择网络非常确定属于目标的像素作为正样本，并将远离 last assumed pixel mask 的像素作为负样本。

我们进一步证明，简单地在每一帧执行在线更新都会导致模型漂移。因此，本文提出在 online updates 时添加第一帧作为额外训练样本。

## Online Adaptation

本文的 online adaptation 的基本思想是使用预测置信度高的像素作为训练样本，即将前景预测概率超过阈值  $\alpha$ 的像素作为正样本。有人认为，使用这些像素作为正样本是没有用的，因为网络已经为它们提供了非常自信的预测。但是，重要的是，online adaptation 必须保留对 positive class 的记忆，以便与要添加的负样本保持平衡。在我们的实验中，省略此步骤会导致 foreground mask 出现孔洞。

对于负样本，一个简单的想法是使用前景概率非常低的像素。但这可能导致性能下降，因为表观发生较大变化时，将选择错误的像素作为负样本。因此我们根据两帧之间的运动很小的假设，来选择负样本。

具体而言，选择与最后预测的目标模板相距很远的所有像素作为负样本。

在实验中发现，仅采用上述样本进行训练会很快导致漂移。为了避免此问题，本文提出在 online updates 时添加第一帧作为额外训练样本，即：每帧只从 $n_{online}$ 次更新，其中仅 $n_{curr}$ 次使用当前帧更新，剩余次数使用第一帧更新。

同时，给予当前帧较小的权重 0.05。虽然看起来非常小，但是第一帧经常用于更新，很快会导致较小的梯度，而当前帧仅被选择了几次。