---
title: '[CVPR2020] Tracking by Instance Detection: A Meta-Learning Approach'
date: 2020-05-11 18:18:13
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Meta-Learning]
---

## Abstract

本文的核心思想是将检测器转换为跟踪器，具体做法分为三步：

1. 选择任一使用梯度下降法训练的目标检测器。
2. [meta-learning] 使用 MAML 在大量跟踪序列上训练检测器。
3. [domain adaptation] 对于新的跟踪视频，使用第一帧，通过几次梯度下降微调检测器。

##  Learning an Instance Detector with MAML

将检测器转换为跟踪器的关键是进行良好的初始化，以便在只有初始帧可用时，能够快速适应新目标。

给定一段视频 $V_i$，我们收集一组训练集 $\mathcal D^s_i$，在 meta learning 中称为 support set。

将检测模型定义为 $h(x;\pmb\theta_0)$，其中 $x$ 是输入图像，$\pmb\theta_0$ 是检测器参数。

我们在 support set 上进行 $k$ 次梯度下降来更新检测器：

<img src="https://i.loli.net/2020/05/11/gJbTad8i5rjBNQc.png" alt="image-20200511182514561" style="zoom:50%;" />

该过程称为 inner-level optimization。

为了评估已训练的检测器的泛化性，我们从相同的视频 $V_i$ 中收集另一组样本 $\mathcal D^t_i$，称为 target set。

在 target set 上计算损失：

<img src="https://i.loli.net/2020/05/11/61zbtcmYf2xHXn9.png" alt="image-20200511184949016" style="zoom:50%;" />

Overall training objective 是寻找对任意跟踪视频来说都良好的 initialization status $\pmb \theta_0$：

<img src="https://i.loli.net/2020/05/11/clLZf5tuyFoEMW3.png" alt="image-20200511185318302" style="zoom:50%;" />

该过程称为 outer-level optimization。