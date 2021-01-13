---
title: '[ECCV2020] Efficient Semantic Video Segmentation with Per-frame Inference'
date: 2020-07-20 11:18:40
tags:
- Video Semantic Segmentation
- Inter-frame Consistency
- ECCV2020
mathjax: true
---

## Abstract

现有算法的问题：如果将图像语义分割网络直接应用于视频语义分割任务，则可能产生不一致的结果。先进的方法考虑了视频序列中的相关性，例如，通过使用光流将结果传播到相邻帧，或使用多帧信息提取 frame representations，这可能导致结果不准确或产生时延。

本文的解决方案：在训练时将时间一致性作为额外约束，在测试时独立处理每帧。

为了缩小小模型和大模型之间的性能差距，设计了新的知识蒸馏方法。

代码：https://git.io/vidseg

## Approach

本节展示如何在训练中利用时间信息。引入如下内容：

- temporal loss：提高 single-frame models 的时间一致性。
- temporal consistency knowledge distillation：将时间一致性从大模型迁移到小模型。

### Motion Guided Temporal Consistency

将先前预测作为监督信号，为两帧之间对应的像素分配一致的标签。

对于两个输入帧 $I_t,I_{t+k}$，有：

<img src="https://i.loli.net/2020/07/20/xgK59l8kb3e2EUS.png" alt="image-20200720133638910" style="zoom:50%;" />

$q^i_t$ 是 segmentation map $Q_t$ 在 位置 $i$ 处的 predicted class probability。$\hat q^i_{t+k->t}$ 是利用 motion estimation network (e.g., FlowNet) $f(·)$ 将 $t+k$ 帧的 class probability warp 到 $t$ 帧后的值。

$V_{t->t+k}$ 用于移除 warpping error 导致的噪声：

<img src="https://i.loli.net/2020/07/20/H4lU2dJLQwV7qOD.png" alt="image-20200720134400622" style="zoom:50%;" />

实现时，使用预训练的光流估计网络。

### Temporal Consistency Knowledge Distillation

为了训练紧凑的网络，提出蒸馏机制，利用教师网络 $T$ 训练学生网络 $S$。其中，教师网络已经用交叉熵损失和时间一致性损失进行训练，取得了很高的分割精度和时间一致性。