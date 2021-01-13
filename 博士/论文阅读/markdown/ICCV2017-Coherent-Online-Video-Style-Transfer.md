---
title: '[ICCV2017] Coherent Online Video Style Transfer'
date: 2020-07-19 11:12:59
tags:
- ICCV2017
- Inter-Frame Consistency
- Style Transfer
mathjax: true
---

## Abstract

现有算法的问题：虽然图像的风格迁移任务取得了成功，但是处理视频时，结果会闪烁。

本文的解决方案：第一个提出了用于在线视频风格迁移的**端到端**网络，可生成连贯的视频（`temporally coherent`）。

算法具有两个关键的思想：

1. 合并短期一致性
2. 将短期一致性传播为长期一致性

## Method

### Motivation

直觉是将风格化的结果从前一帧 warp 到当前帧，并自适应地将两者融合到一起。换句话说，前一帧的某些可追踪（traceable）的点/区域保持不变，而某些不可追踪的点/区域使用当前帧的新结果。这一策略具有两种作用：

1. 确保运动路径上的风格化结果尽可能稳定。
2. 避免了因遮挡或运动不连续而产生的伪影。

上述策略仅保留了短期一致性。我们需要将短期一致性进行传播，以获得长期一致性。在 $t-1$ 时刻，获得了组合特征图 $F^o_{t-1}$，该特征图受两帧一致性（ two-frame consistency）约束。在时刻 $t$，我们重新利用 $F^o_{t-1}$。这样，我们的网络每次只需要考虑两帧，但是仍然可以达到长期一致性。

###  Network Architecture

给定输入视频 $\{I_t|t=1...n\}$，任务是获得风格化的视频 $\{O_t|t=1...n\}$。对于第一帧 $I_1$，使用现有的风格化网络 $Net_0$ 产生风格化结果。同时生成 encoded features $F_1$，在处理第二帧时，$F_1$ 是我们提出的网络 $Net_1$ 的输入。从第二帧开始，使用 $Net_1$ 而不是 $Net_0$ 进行风格化迁移。

本文提出的 $Net_1$ 可保持相邻两帧的一致性，包含三个组件：

1. Style Sub-network
2. Flow Sub-network
3. Mask Sub-network

<img src="https://i.loli.net/2020/07/19/7bLORjPkiBnwVHQ.png" alt="image-20200719144729983" style="zoom:50%;" />

#### Style Sub-network

使用 [23] 作为默认的风格子网。

> [23] J. Johnson, A. Alahi, and L. Fei-Fei. **Perceptual losses for real-time style transfer and super-resolution**. arXiv preprint arXiv:1603.08155, 2016.

#### Flow Sub-network

使用 flownet [15] 作为默认的 flow 子网。

> [15] P. Fischer, A. Dosovitskiy, E. Ilg, P. Hausser, C. Hazırbas¸, ¨ V. Golkov, P. van der Smagt, D. Cremers, and T. Brox. **Flownet: Learning optical flow with convolutional networks**. arXiv preprint arXiv:1504.06852, 2015.

两个相邻帧 $I_{t-1}, I_t$ 首先编码为特征 $F_{t-1}, F_t$。$W_t$ 是由 flow 子网生成的 feature flow，并缩放到 $F_{t-1}$ 的尺寸。由于 $W_t$ 的值通常是小数，我们通过双线性插值将 $F_{t-1}$ warp 到 $F_t'$：

<img src="https://i.loli.net/2020/07/19/WTtw2NpjSZVHfJ7.png" alt="image-20200719150021593" style="zoom: 50%;" />

其中 $\mathcal W_{t-1}^t(\cdot)$ 是利用 $W_t$ 将特征从 $t-1$ warp 到 $t$ 的函数，即：

<img src="https://i.loli.net/2020/07/19/KJXQN7mnIfSCuyR.png" alt="image-20200719150349757" style="zoom:50%;" />

#### Mask Sub-network

给定 warped feature $F'_t$ 和 original feature $F_t$，mask 子网用于回归 composition mask $M$，$M$ 用于组合 $F'_t$ 和 $F_t$。$M$ 的值介于 0 到 1 之间。对于可跟踪的点/区域，mask 的值为 1，表示应该利用 $F'_t$ 以保持连贯性。否则 mask 的值为 0，以利用 $F_t$。

Mask 子网由三个卷积层构成，步长为 1。输入是两个特征图的绝对插值：

<img src="https://i.loli.net/2020/07/19/7SGAfxJQoVzvwXl.png" alt="image-20200719150957201" style="zoom:50%;" />

说明：差异大，表示属于不可跟踪点，尽量利用当前帧特征。差异小，表示属于可跟踪点，尽量利用上一帧特征。

输出是单通道 mask $M$。通过线性插值获得 composite features $F^o_t$：

<img src="https://i.loli.net/2020/07/19/pPZuXkHlM8AGgQi.png" alt="image-20200719151147462" style="zoom:50%;" />

#### Summary of $Net_1$

给定两个输入帧 $I_{t-1}$ 和 $I_t$，送入**参数固定**的风格子网的**编码器**中，得到特征图 $F_{t-1}, F_t$。

在另一个分支中，$I_{t−1}, I_t$ 送入 flow 子网生成 feature flow $W_t$，把特征 $F_{t-1}$ warp 成 $F'_t$。

接下来计算 $\Delta F$ 并送入 mask 子网得到 $M$，利用 $M$ 得到 $F^o_t$。

最后，将 $F^o_t$ 送入风格子网的**解码器**中，得到第 $t$ 帧的风格化结果。

### The Loss Function

为了训练 flow 和 mask 子网，损失包含 3 项：

1. coherence term
2. occlusion term
3. flow term

Coherence term 惩罚两个连续帧的风格化结果的不一致性：

<img src="https://i.loli.net/2020/07/19/mfoTYJXZkrcpbC6.png" alt="image-20200719152823661" style="zoom:50%;" />

$S_{t-1}$ 是 $t-1$ 帧独立计算的风格化结果。

Warping function $W^t_{t−1}(\cdot)$ 使用 ground-truth flow。

$M_g$ 是 ground-truth mask。

该损失鼓励 $O_t$ 和 $S_t$ 在可跟踪点/区域上的风格化结果保持一致。

相反，对于不可跟踪区域，occlusion loss 迫使 $O_t$ 和 $S_t$ 保持一致：

<img src="https://i.loli.net/2020/07/19/gVlYxQOtH6uJX3T.png" alt="image-20200719153650486" style="zoom:50%;" />

另外，还要约束 feature flow：

<img src="https://i.loli.net/2020/07/19/7dNgFB2lLRWyEDu.png" alt="image-20200719153856140" style="zoom:50%;" />

其中 $W^g_t \downarrow$ 表示将 ground-truth optical flow 下采样到与 $W_t$ 尺寸相同。