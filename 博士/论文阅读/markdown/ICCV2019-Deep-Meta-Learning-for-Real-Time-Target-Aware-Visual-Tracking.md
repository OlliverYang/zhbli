---
title: '[ICCV2019] Deep Meta Learning for Real-Time Target-Aware Visual Tracking'
date: 2020-04-27 14:52:29
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Meta-Learning]
---

## Abstract

现有跟踪算法的问题：需要进行 continuous re-training，而这涉及解决复杂的优化任务以适应目标新的表观。

本文的解决方案：提出基于孪生跟踪器和 meta-learner network 提出了可实时运行的 online 跟踪框架。

meta-learner network 的作用：向孪生网络添加 target-aware feature space，从而提供新的表观信息。

在 5 个数据集上验证了算法有效性，速度为 48 FPS。

## Introduction

大多数跟踪算法使用深度卷积特征作为特征提取器，并添加用于 `on-line adaptation` 的分类器或卷积滤波器。

这些算法的缺点：这些算法整合得不够好，两个不同的系统（特征提取器和分类器）分别构建和训练。这就导致分类器需要不断更新以适应目标表观变化，而训练样本有限。这种更新操作需要使用 SGD、Lagrange multipliers、ridge regression 等方法求解复杂的优化问题。这使得跟踪器的运行速度通常在 20 FPS 以下。另外，由于训练样本少，容易导致过拟合。为了解决过拟合问题，大多数算法将手动设计的正则项与  training hyper-parameter tuning scheme 结合在一起，以获得更好的结果。

本文将用于 target search 的 Siamese `matching network` 和用于 adaptive feature space update 的 meta-learner network 整合到一起，以解决上述问题。对于 meta-learner network，本文提出 parameter prediction network，该网络的设计灵感来自用于解决 few-shot learning 问题的 meta learning 方法。

本文提出的 meta-learner network 为 `matching network` **提供额外的 convolutional kernels 和 channel attention information**，这样可以自适应的修改 matching network 的特征空间，从而可以在跟踪过程中获得新的表观模板，同时避免过拟合。

给定新的表观训练样本，meta-learner tracker 仅能看到 matching network 最后一层的梯度。

本文还为 meta-learner network 设计了新的训练方式，阻止 meta-learner network 生成导致 matching network 过拟合的新参数，以维持特征空间的泛化能力。

利用 meta-learner network，通过一次前向传播就能构建 target-specific feature space，无需任何迭代优化，同时避免了过拟合，从而提高了跟踪性能。

##  Tracking with Meta-Learner

### Overview of Proposed Method

#### Components

定义 $x$ 为表示目标的图像块，$z$ 为包括目标的、具有更大背景区域的图像块。

给定表示目标的图像块 $x$ 和在先前帧获得的 context patches $\mathbf{z}_\delta = \{z_1,...,z_M\}$，meta-learner network 为 matching network 提供 target-specific weights。为了使权重适应 target patch，本文使用 matching network 的损失函数在最后一层的负梯度 $\delta$（公式2）：

<img src="https://i.loli.net/2020/05/01/2ok7x3jMWDBQTtz.png" alt="image-20200501151253293" style="zoom:50%;" />

其中，$\tilde y_i$ 是 generated binary response map，假设目标位于 $z_i$ 中的正确位置。

Meta-learner network 基于如下事实设计：对于不同的目标，$\delta$ 的特性也不同。因此，将 $\delta$ 作为输入，meta-learner network $g_\theta(\cdot)$ 可以根据输入生成 target-specific weights $w^{target}$（公式3）：

<img src="https://i.loli.net/2020/05/01/RqgTKCUJj6hoHr5.png" alt="image-20200501152811567" style="zoom:50%;" />

新的权重用于更新 matching network 的原始权重（公式4）：

<img src="https://i.loli.net/2020/05/01/Jwm78tETpgQkUvZ.png" alt="image-20200501152928542" style="zoom:50%;" />

其中 $\mathbf w^{adapt} = \{w_1,w_2,...,[w_N,w^{target}]\}$，将 $w_N$ 和 $w^{target}$ 串接到一起。Meta-learner network 也会为特征图的每个通道生成 channel-wise sigmoid attention weight，用于调整  feature representation space。

###  Tracking algorithm

给定上一帧的 target patch $x$，可以在当前帧裁剪出 context image $z$。将这两幅图同时送入 matching network，可以获得  estimated response map $\hat y = f_{\mathbf w^{adapt}} (x, z)$。

在跟踪过程中，维护一个 context images 的内存 $\mathbf z_{mem} = \{z_1,...,z_K\}$，同时维护对应的 estimated response maps 的内存 $\hat {\mathbf y}_{mem}=\{\hat y_1,...,\hat y_K\}$。仅当 response map 中最大值超过阈值 $\tau$ 时，才将对应的 context image 放入内存。

为了更新目标的表观，基于 $\hat {\mathbf y}_{mem}$ 上的 minimum entropy criterion，在内存中选择 $M$ 个样本。该准则避免了有歧义的 response maps：

<img src="https://i.loli.net/2020/05/01/mYKDaJAqRMPeUH6.png" alt="image-20200501160306752" style="zoom:50%;" />

使用 $M$ 个 appearance samples $\mathbf z_\delta$，根据公式 2 和公式 3 获得 target-adaptive weights $w^{target}$。然后利用公式 4 更新 matching network。

### Network Implementation and Training

###  Matching Network

网络共 5 层，每层的 kernel size、input dimension、output dimension 分别为：

1. $11\times 11 \times 3 \times 128$
2. $5\times 5 \times 128 \times 256$
3. $3\times 3 \times 256 \times 384$
4. $3\times 3 \times 384 \times 256$
5. $1\times 1 \times 256 \times 192$

#### Meta-Learner Network

Meta-learner network 由三个全连接层组成，其中两个中间层具有 512 个单元。输入和输出分别为：

- 输入：gradient $\delta$，尺寸为 $1\times 1\times 256\times 192$。

- 输出：$w^{target}$，尺寸为 $1\times1\times 256\times 32$。

  将 $w_5$ 和 $w^{target}$ 串接起来，得到新的 kernel，尺寸为 $1\times 1\times 256 \times (192+32)$。

为了训练 meta-learner network，使用 ILSVRC 视频数据库验证集的 1314 段视频。训练过程如下：

1. 从 object trajectory 中随机采样一个 anchor target image $x$。
2. 从同一个目标的 object trajectory 中随机采样 $M'$ 个 context patches $\mathbf z_{reg} = \{z_1,...,z_{M'}\}$，其中 $M' \ge M$。为了避免过拟合，令 $M' = 2M$。实验中，$M = 8$。
3. 从 $\mathbf z_{reg}$ 中采样 $M$ 个样本构成 $\mathbf z_\delta$。
4. 通过公式 2 获得梯度 $\delta$。
5. 通过最小化损失函数来训练 meta-learner network：

<img src="https://i.loli.net/2020/05/01/oJleQ7hOIMVuxzW.png" alt="image-20200501161937898" style="zoom:50%;" />

补充：反传时，更新的是 $\theta$ 的梯度。因为是对 meta-learner network 进行训练。

## Experimental Results

### Experiments and Analysis

#### Quantitative Analysis

##### Effect of meta-learner network

本文提出的算法 MLT 与两个变种 MLT-mt 和 MLT-mt+ft 进行对比：

- MLT-mt 仅有 matching network，参数固定。
- MLT-mt+ft 使用在跟踪时获得的训练样本对 conv5 执行微调。

<img src="https://i.loli.net/2020/05/01/6zGYWPbMlcUtaNv.png" alt="image-20200501155543248" style="zoom:50%;" />