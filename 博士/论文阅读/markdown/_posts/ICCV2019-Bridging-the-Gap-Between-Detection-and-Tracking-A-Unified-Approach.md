---
title: '[ICCV2019] Bridging the Gap Between Detection and Tracking: A Unified Approach'
date: 2020-05-04 13:07:40
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Meta-Learning]
---

## Abstract

本文设计了通用的框架，用于之间在目标检测器上构建跟踪器。为了实现这一点，必须弥合三个关键的差距：

1. 目标检测器是特定于类别的，而跟踪器是类别无关的。
2. 目标检测器不能区分同一类别的实例，而这是跟踪器的关键功能。
3. Temporal cues 对跟踪器很重要，而检测器处理的是静态图像，没有时间信息。

为了解决上述问题，本文：

- 首先提出一个简单的 target-guidance module，用于引导检测器定位 target-relevant objects。
- 然后将元学习应用于目标检测器，以快速在线学习和调整  target-distractor classifier。
- 进一步引入 anchored updating strategy  以缓解过拟合问题。

性能：

- 在 4 个数据库上进行实验：OTB2013，OTB2015，UAV123，Need for Speed。

## Proposed Method

### Target-Guided Object Detection

本文提出  target-guidance module，输入时 target/search region features，输出的特征图与检测网络相同。后续部分保持不变。

具体而言，首先在目标特征上执行 ROI pooling，后跟卷积得到尺寸为 $C\times 1\times 1$，C 是特征通道数。具体按下图 (b) 的方式与 search features 进行融合。

![image-20200504135037727](https://i.loli.net/2020/05/04/RZXfPv8n79HA4FE.png)

损失函数与检测网络相同。

### Few-Shot Learning for Domain Adaptation

虽然上一节提到的模块可以检测到与目标相关的物体上，但是难以区分这些物体。

我们假设主要的原因是未考虑周围的负样本，从而削弱了检测器的判别性。为了弥补这一点，本文提出在少量样本上显式学习分类器。但是，直接在如此小的数据集上从头训练非常耗时，并会导致严重的过拟合。因此，本文用 few-shot learning 方法解决这一问题。

具体而言，采用 MAML 算法来训练 target-distractor classifier。MAML 学习了网络初始化，可以通过少量训练样本和几次迭代快速适应新的、看不见的任务。

在本文的模型中，作者发现检测器的 classification head 是 target-distractor classifier 的良好初始化，因此使用 meta layer 代替它，并从大量训练数据中学习针对任务进行微调。

具体而言，在训练过程中，从视频帧中采样 triplets $\{z_b,s_b,q_b\}_{b=1}^B$，其中 $B$ 是 batch size，$z_b,s_b,q_b$ 是三个 croped images，按时间顺序采样，即 exemplar, support and query images。对于 meta-parameter 为 $\theta$ 的 guided detector，希望学习初始的 $\theta=\theta_0$，使得在 `support set` $(z_b,s_b)$ 上进行梯度更新获得 $\theta_N$ 后，检测器能够在 query set $(z_b,q_b)$ 上表现良好。在 $(z_b,s_b)$ 上的第 $i$ 次梯度更新为（公式 1）：

<img src="https://i.loli.net/2020/05/04/fADi8bqCGrMc9T1.png" alt="image-20200504142857175" style="zoom:50%;" />

其中 $\mathcal {L}_{(z_b,s_b)}$ 是分类损失。meta-loss 为（公式 2）：

<img src="https://i.loli.net/2020/05/04/WHEMJF5RL8VXUie.png" alt="image-20200504143621041" style="zoom:50%;" />

其中我们显式地写出了 $\theta_N^b$ 依赖于 $\theta_0$。

对 meta-parameter $\theta_0$ 的更新为（公式 3）：

<img src="https://i.loli.net/2020/05/04/DGorPV6XF4SjgcY.png" alt="image-20200504143951753" style="zoom:50%;" />

公式 1 称作内循环，公式 3 称作外循环。由于微调过程是在不同样本上进行的（support/query set)，因此泛化能力得到了保证。

实验发现，同时微调 classification/regression head 效果更好。因此本文直接利用检测器的 loss 优化 $\theta_0$。

整个跟踪框架端到端训练。

### Online Tracking Approach

#### Anchored Updating

元学习的离线训练无法保证 contrinuous learning 的泛化能力。

受 anchor loss 的启发，提出  anchored updating strategy 以缓解过拟合现象。

具体而言，将第 1 帧学习的参数 $\theta_1$ 保存起来，第 $t$ 帧的参数 $\theta_t$ 定义为上一阵的参数与初始参数的线性组合：

<img src="https://i.loli.net/2020/05/04/7xiMSqXmZU3jOgJ.png" alt="image-20200504151309450" style="zoom:50%;" />

将 $\theta_0$ 称为 anchor parameters。由于 anchor parameters 在在线优化过程中具有固定的权重，因此可以缓解过拟合的问题。

### Instatiation on SSD and FasterRCNN

我们的模块具有通用性，可以适用于不同的目标检测器。但在本文中，对两个典型的检测框架进行实例化：SSD 和 Faster RCNN。

## Experiments

### Ablation Study

#### Few-shot Learning

将本文的 few-shot learning 算法与  brute force gradient descent (GD) 分别对网络进行微调。

见下表。

#### Anchored Updating

见下表。

#### Guidance Images

见下表。

<img src="https://i.loli.net/2020/05/04/OdEMQwSBZuWPHUm.png" alt="image-20200504152114044" style="zoom:50%;" />

#### Backbone Network Depth

<img src="https://i.loli.net/2020/05/04/m9o1QeSjFMpW5wZ.png" alt="image-20200504152202334" style="zoom:50%;" />