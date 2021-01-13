---
title: '[arXiv2004] A Simple Baseline for Multi-Object Tracking'
date: 2020-04-20 13:30:11
tags: Multi-Object Tracking
mathjax: true
---

## Abstract

现有 MOT 算法的问题：很少有算法在单个网络中同时进行目标检测和 reid。现有的尝试导致性能降低。

原因：现有的尝试未能正确学习 reid 分支。

本文的解决方案：分析了未能正确学习 reid 分支的原因，并提出了改进。

性能：

- https://github.com/ifzhang/FairMOT
- 速度：30 FPS。
- MOT17_MOTA：67.5（private_detector）。
- MOT20_MOTA：58.7（private_detector）。

## Introduction

分析了在单个网络中同时进行目标检测和 reid 的三个关键因素：

1. anchors 不适用于 reid。
   1. 原因：
      1. 表示不同图像块的多个 anchors 可能对应于同一个物体，这导致网络的严重歧义。
      2. 下采样为 8，这对 reid 来说太粗糙了。这导致目标中心与特征中心无法对齐。
   2. 方案：
      - 将 MOT 问题视为在高分辨率特征图上的 pixel-wise 关键点（即目标中心）估计问题和 identity classification 问题。
2. 多层特征聚合。
   - 这对 MOT 很重要，因为 reid 需要利用低层和高层特征来处理小目标和大目标，从而提成了对物体尺度变化的适应性。
3. reid 特征的维度。
   - 低维特征对 MOT 更好。因为训练数据少，而我们无法使用 reid 数据集。减少了过拟合风险，提高了鲁棒性。

## Related work

MOT 分为两阶段跟踪和一阶段跟踪：

- 两阶段跟踪
  - 优点：可以针对每个任务使用最佳模型而无需折中。
  - 缺点：速度慢，无法实现权重共享。
- 一阶段跟踪
  - 优点：速度块，权重共享。
  - 缺点：无法很好地学习 reid 分支。

## The Technical Approach

网络分为三部分：

1. backbone
2. 目标检测分支
3. reid 分支

### Backbone Network

使用基于 DLA 的变种 [45] 的 resnet34，下采样率为 4。

> Zhou, X., Wang, D., Kr¨ahenb¨uhl, P.: Objects as points. arXiv preprint arXiv:1904.07850 (2019)

### Object Detection Branch

与 [45] 相同，将目标检测视为基于中心点的边框回归任务，在 backbone 上附加 3 个  regression heads，分别用于估计 heatmaps，object center offsets 和边框尺寸。每个 head 一个是 256 通道的 $3\times 3$ 卷积，后接一个 $1\times 1$ 卷积。

#### Heatmap Head

heatmap 的尺寸是 $1\times H \times W$ （与特征图尺寸相同）。Ground truth 是以目标为中心的高斯。

#### Center Offset Head

由于下采样率为 4，必然引入误差。这对检测的影响不大，但对跟踪至关重要。因为应该根据准确的目标中心提取 reid 特征。

#### Box Size Head

与 reid 无关。

### Identity Embedding Branch

该分支的目的是生成可以区分不同目标的特征。通过在特征图上卷积为每个位置得到 128 为嵌入向量。

#### Loss Functions

#### Heatmap Loss

<img src="https://i.loli.net/2020/04/20/xTV9UOWnyFGZtJk.png" alt="image-20200420133241614" style="zoom:50%;" />

#### Offset and Size Loss

<img src="https://i.loli.net/2020/04/20/TQsqUZlCJ2NmRHP.png" alt="image-20200420133310654" style="zoom:50%;" />

#### Identity Embedding Loss

将身份嵌入视为分类任务：将训练集中具有同一人物的目标视作同一类。

<img src="https://i.loli.net/2020/04/20/bfgBwLqz4cxNrQa.png" alt="image-20200420133335418" style="zoom:50%;" />

$\mathbf{p}(k)$ 为 class distribution vector。

$\mathbf{L}^i(k)$ 为 GT class label 的 one-hot 表示。

$K$ 是类别数。

N 是图像中的目标数。

### Online Tracking

使用 reid 特征的距离，以及 IoU，来链接两帧的边框。

### Implementation Details

使用 DLA-34 的变种 [45] 作为 backbone。使用 coco 预训练参数对模型初始化。

在两个 RTX 2080 GPU 上的训练时间约 30 小时。