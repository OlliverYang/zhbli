---
title: '[arXiv2004] Fully Convolutional Online Tracking'
date: 2020-04-17 17:49:04
tags: Tracking
mathjax: true
categories:
- [Tracking, Model Update]
---

## Abstract

现有跟踪算法的问题：仅对分类分支进行简单地在线学习，难以对回归分支进行在线学习。

本文的解决方案：首次提出全卷积在线跟踪框架 FCOT，同时在线学习分类和回归分支。

主要贡献：

- 引入 anchor-free 边框回归分支，从而将整个跟踪网络统一为更简单的全卷积网络。
- 引入 regression model generator (RMG) 对回归分支在线优化，有效处理物体形变。

性能：

- 代码（待开源）：https://github.com/MCG-NJU/FCOT
- 速度：53 FPS。
- GOT-10k AO=62.7。

## Introduction

目标跟踪包括分类分支和回归分支。对于分类任务，可分为生成式跟踪器（SiamFC）和判别式跟踪器（DiMP）：

- 生成式：使用固定的 target template，不进行背景建模。
- 判别式：通过最大化目标和背景之间的 response gap 来学习自适应滤波器。

对于回归任务，现有方法通常取决于手工设计，例如锚框放置或边框框采样及选择。这种复杂设计使得回归分支难以在线更新。因此本文设计了简单的回归分支以进行在线更新。

因此，本文提出全卷积跟踪器，无需任何手工设计。核心是 online anchor-free 边框回归分支，直接回归每帧的边框尺寸。另外，提出在线优化算法，自适应调整回归分支参数。

FCOT 的具体设计：

1. 设计新的编码器-解码器结构，用于高分辨率特征提取。引入上采样层，对于提高准确性至关重要。
2. FCOT 由用于大致定位对象中心的分类分支和用于回归边界框大小的回归分支组成，通过可变形卷积实现。
3. 为了区分背景和目标，并解决物体形变问题，通过在线学习对两个分支的参数进行自适应调整。受DiMP的启发，我们设计了一种新颖的在线回归模型生成器（RMG），该模型由模型初始化器和在线模型优化器组成。

我们证明了在线边框回归器能够持续提高跟踪性能，尤其是对于更高的IoU标准。

与 SiamFC++ 的区别：

- 我们是在线跟踪器，专为分类和回归分支进行在线更新。而 SiamFC++ 是参数固定的生成式跟踪器。
- 我们的特征图分辨率更高。

## Our Method

![image-20200417191653613](https://i.loli.net/2020/04/17/27Vgio8b3Md5ljm.png)

设计原则：

1. 简单而统一的架构。将特征提取器、分类分支和回归分支用单一架构实现。
2. 准确的回归和分类。
   1. FCOT 生成更大的得分图和边框偏移图，使结果更精确。
   2. 对于回归，首次使用最速下降方法在线优化 Regression Model Generator。
   3. 对于分类，利用 DiMP 提出的 online target model generator 区分目标和背景。

###  Classification and Regression via Fully Convolutional Network

判别跟踪器如 ATOM、DIMP 性能很好，但是两阶段的，并执行复杂的目标回归过程。因此，我们为分类和回归引入了一个简单的全卷积网络来克服这些问题。

#### Feature Extraction

使用编解码器提取特征：

- 编码器包括 ResNet50 的 1~4 层。
- 解码器包括一个 $1 \times 1$ 卷积和两个简单的上采样层。
- 下采样率为 4。

Classification head 在训练和测试时一样，但 Regression Head 在训练和测试时不同。

- Regression Head-1 输出 1024 通道的特征图，用于生成 4 个回归滤波器。
- Regression Head-2 输出 256 通道的特征图，与 4 个滤波器进行回归卷积。

<img src="https://i.loli.net/2020/04/17/Y496rPnR7xygaFZ.png" alt="image-20200417192718516" style="zoom:50%;" />

#### Classification and Regression

在 FCOT 中，将跟踪形式化为逐像素预测问题。我们使用分类和回归分支分别预测一个 target center confidence map $M_{cls}$ 和四个 offsets maps $M_{reg}$：

<img src="https://i.loli.net/2020/04/17/QtRcr6XDT48fmkb.png" alt="image-20200417193826360" style="zoom: 33%;" />

$\phi$ 表示分类分支的特征提取器，$\theta$ 表示回归分支的特征提取器，$f_{cls}$ 和 $f_{reg}$ 表示由相应的 model generators 产生的滤波器。$*$ 表示卷积操作。

对于特征图的每个位置 $(x, y)$，可以将其映射回原图 $(\lfloor \frac{s}{2}+xs \rfloor, \lfloor\frac{s}{2}+ys \rfloor)$，其中 $s=4$ 为步长。

对于分类，$M_{cls}$ 表示像素位于目标中心的置信得分。训练时的 ground truth 是以目标中点 $c_t$ 为中心的高斯函数图。

对于回归，$M_{reg}(x,y)$ 是 4 维向量 $(l^\unicode{0x2A}, r^\unicode{0x2A}, t^\unicode{0x2A}, b^\unicode{0x2A})$，表示从点 $(x,y)$ 到映射到特征图中的目表边框的左、右、上、下边的距离。因此回归目标是：

<img src="https://i.loli.net/2020/04/17/w4FVLB6faHDirWp.png" alt="image-20200417193836328" style="zoom: 33%;" />

其中 $(x_0, y_0, x_1, y_1)$ 表示目标的边框。我们为针对目标中心 $c_t$ 半径为 2 的区域进行回归，而不仅为目标中心进行回归。

### Regression Model Generator

<img src="https://i.loli.net/2020/04/17/BAoU2GnevOQ1i8x.png" alt="image-20200417202244892"  />

回归模型包括：

- 模型初始化器
  - 输入：
    - 第一帧的回归特征
    - 第一帧的边框
  - 输出：
    - 回归卷积滤波器，即初始模型。
  - 结构：
    - 尺寸为 $3\times 3$ 的单个 ROI-pooling 层。
    - 为了提高速度，仅在第一帧的特征上执行 ROI pooling，产生粗略的模型。
  - 模型优化器
    - 输入：
      - 训练集的特征
      - 相应的边框
    - 作用：迭代更新模型。

模型优化器的在线回归训练损失：

<img src="https://i.loli.net/2020/04/17/NJy7oIlstERGCnP.png" alt="image-20200417193856004" style="zoom: 33%;" />

$N$ 是在线训练集 $S_{train}$ 的长度。

$S_{train}$ 由具有较高分类得分的以跟踪的帧组成。

$X$ 是由 Regression Head-1 提取的特征。

$M_{reg}^{(c)}$ 是 regression map $M_{reg}$ 中，中心位置 $c$ 对应的四维距离向量。

$X^{(c)}$ 是 $X$ 中的一部分，以 $c$ 为中心，面积为 $3\times 3$（与 regression model 的尺寸相同）。

$f$ 是回归卷积滤波器。

$*$ 是卷积操作。

$\lambda$ 是正则化因子。

使用梯度下降优化 $f$ 很慢，因此使用最速下降法求解。通过计算步长 $\alpha$ 来更新模型：

<img src="https://i.loli.net/2020/04/17/jJVNt4EdYHWnQMw.png" alt="image-20200417193907239" style="zoom: 33%;" />

步长和梯度的计算与 DiMP 相同。

### Offiline Training

离线训练分为两阶段：

1. 训练整个网络，除 regression optimizer 外。
2. 更新 regression optimizer，固定网络的其他部分。

由于在线优化模型是耗时的，而且在 regression model generator 中仅有一个参数 $\lambda$ 需要训练，因此这种两阶段训练方式使得训练时间大为缩短。

离线训练损失为：$L_{tot} = \alpha L_{cls} + \beta L_{reg}$，$\alpha = 100, \beta = 0.1$。

使用 8 RTX 2080ti 离线训练 50 小时。 
