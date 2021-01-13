---
title: '[CVPR2019] Target-Aware Deep Tracking'
date: 2020-04-24 10:19:51
tags:
- CVPR2019
- Tracking
mathjax: true
categories:
- [Tracking, Feature Extraction]
---

## Abstract

现有跟踪算法的问题：很多跟踪算法使用在通用目标识别任务上预训练的模型，但预训练模型对跟踪任务的贡献不如对其他目标识别任务大。

原因：目标跟踪中的物体可能是任意类别。因此，预训练模型很难将目标与背景区分开。

本文的解决方案：学习 target-aware features，相比于预训练特征，可以更好地识别目标。为此，设计 regression loss 和 ranking loss，用于生成 target-active features 和 scale-sensitive features。我们根据反传梯度确定每个卷积滤波器的重要性，并基于用于表示目标的 activations 来选择 target aware features。Target-aware features 与孪生网络（siamfc）整合以进行目标跟踪。

性能：

- https://xinli-zn.github.io/TADT-project-page/
- 33.7 FPS

## Introduction

使用预训练模型表示目标特征时，存在很多问题：

1. 目标可能是任意形式的。比如，目标可能是训练集中未见过的物体。或者，可能仅仅是物体的一部分。
2. 来自最后一个卷积的特征往往仅具有高层视觉信息，缺乏精确定位和尺度估计信息。
3. 分类网络致力于缩小类内差距，用于跟踪时，无法区分同类物体。
4. 计算量大。

一个分类网络中，反向传播的梯度可以反应特定类别的显著性。

> [33] Ramprasaath R Selvaraju, Michael Cogswell, Abhishek Das, Ramakrishna Vedantam, Devi Parikh, and Dhruv Batra. **Grad-cam: Visual explanations from deep networks via gradient-based localization**. In IEEE Conference on Computer Vision and Pattern Recognition, 2017.

使用 global average pooling，卷积滤波器的梯度能够决定用于表示该滤波器表示一个目标的重要性。为了选择最有效的滤波器，我们设计了两种损失：

1. 使用 hinge loss 将预训练特征回归到由高斯函数生成的 soft labels，并使用梯度选择 target-active 卷积滤波器。
2. 使用 ranking loss with pair-wise distance 寻找 scale-aware 卷积滤波器。

所选的重要滤波器的 activations 便是本文的 target-aware features。由于仅使用部分滤波器，计算量也减少了。

## Target-Aware Features

<img src="https://i.loli.net/2020/04/24/rLuQx19GUcgDTas.png" alt="image-20200424102819639" style="zoom:50%;" />

我们首先分析来自预训练分类模型的特征与用于跟踪的有效表示之间的差距。然后提出 target-aware feature model。

### Features of pre-trained CNNs

给定输出特征空间为 $\mathcal{X}$ 预训练特征提取器，可以跟踪通道重要性 $\Delta$ 生成子空间 $\mathcal{X}'$：

<img src="https://i.loli.net/2020/04/24/LNPET1DhOlfpS9W.png" alt="image-20200424103046271" style="zoom:50%;" />

其中 $\varphi$ 是用于选择重要通道的 mapping function。通道 $i$ 的重要性 $\Delta_i$ 计算为：

<img src="https://i.loli.net/2020/04/24/FTfJ5xceyjULkPV.png" alt="image-20200424103125966" style="zoom:50%;" />

其中 $G_{AP}(\cdot)$ 指 global average pooling 函数，$L$ 是设计的损失，$z_i$ 是第 $i$ 个滤波器的输出特征。

### Target-Active Features via Regression

将与目标中心对齐的图像块中的所有样本 $X_{i,j}$ 回归到高斯 label map $Y(i,j) = e^{-\frac{i^2+j^2}{2\sigma ^2}}$：

<img src="https://i.loli.net/2020/04/24/hgXBDW8LCvrFmqf.png" alt="image-20200424103220532" style="zoom:50%;" />

其中 $W$ 是 regressor weight。可以通过每个滤波器对拟合 label map 的贡献，计算其重要性：

<img src="https://i.loli.net/2020/04/24/n5X4GI9cs3OUJ6t.png" alt="image-20200424103239827" style="zoom:50%;" />

其中 $X_o$ 是 output prediction。

### Scale-Sensitive Features via Ranking

我们需要寻找对尺度变化最敏感的滤波器。我们将该问题建模为 ranking model：对训练样本按照尺寸接近目标的程度进行排序。我们利用了 [23] 中的 smooth approximated ranking loss 实现这一点：

> [23] Yuncheng Li, Yale Song, and Jiebo Luo. Improving pairwise ranking for multi-label image classification. In IEEE Conference on Computer Vision and Pattern Recognition, 2017.

<img src="https://i.loli.net/2020/04/24/QI8a4lqNt1ijvnP.png" alt="image-20200424103420326" style="zoom:50%;" />

其中 $(x_i, x_j)$ 是成对训练样本，$x_j$ 相比于 $x_i$，于目标尺寸的差距更小。$f(x,w)$ 是预测模型。

梯度计算为：

<img src="https://i.loli.net/2020/04/24/We8yw3VgiETcJn2.png" alt="image-20200424103636096" style="zoom:50%;" />

<img src="https://i.loli.net/2020/04/24/S2xQhvVzaYIibWk.png" alt="image-20200424103655075" style="zoom:50%;" />

其中 $W$ 是卷积层中的滤波器权重。

## Tracking Process

提出的跟踪框架由如下部分组成：

1. pre-trained feature extractor：使用分类任务离线训练。
2. target-aware feature module：仅使用第一帧训练。
3. Siamese matching module

测试时，使用 target-aware features 计算相似性得分：

<img src="https://i.loli.net/2020/04/24/rwXMPSqLpWRAoaE.png" alt="image-20200424103908919" style="zoom:50%;" />