---
title: '[CVPR2020] One-shot Adversarial Attacks on Visual Tracking with Dual Attention'
date: 2020-08-14 14:55:48
tags:
- Tracking
- Adversarial Attack
- CVPR2020
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## Methodology

### One-shot Attack with Dual Loss

给定第一帧图像和目标边框，可以获得 target patch $z$。我们的目标是获得对抗性 target image $z^* = z + \Delta z$，使得跟踪结果变差。对抗样本定义为：

<img src="https://i.loli.net/2020/08/14/dwOyS9tYzB3VWN7.png" alt="image-20200814153246243" style="zoom:50%;" />

#### Batch Confidence Loss

我们仅在初始帧中执行攻击，因此在初始帧模拟跟踪过程以生成对抗样本。我们假定搜索区域$X$中包括n个候选$\{x_1,...,x_n\}$。

定义$f(z,x_i)$为跟踪模型，输出为预测得分，batch confidence 定义为：

<img src="https://i.loli.net/2020/08/14/N1JbGg5djOFiM4C.png" alt="image-20200814153929661" style="zoom:50%;" />

$R_{1:p}$ 表示得分前p高的候选，$R_{q:r}$ 表示得分排名从q到r的候选。

该损失的目的是是抑制具有高置信度的候选并激发具有中等置信度的候选。

#### Feature Loss

从CNN的特征空间中攻击所有候选。

令$\phi(\cdot)$表示CNN的特征图，将z和z*的特征图的欧氏距离最大化：

<img src="https://i.loli.net/2020/08/14/l54B7kZoFebw3fM.png" alt="image-20200814154707872" style="zoom:50%;" />

### Dual Attention Attacks

我们在两个损失函数上应用注意力机制。

#### Confidence Attention

该注意力机制可以区分具有不同置信度的候选的抑制/激发程度。

<img src="https://i.loli.net/2020/08/14/4MtgkjyhKdTCvx7.png" alt="image-20200814155326679" style="zoom:50%;" />

<img src="https://i.loli.net/2020/08/14/BRU7oq3CSL6FOQs.png" alt="image-20200814155430435" style="zoom:50%;" />

其中$d(x_i)$表示按照置信度排序的第i个候选到第1个候选坐标距离。

#### Feature Attention

<img src="https://i.loli.net/2020/08/14/c6LFT9P8GrmbKlJ.png" alt="image-20200814155922018" style="zoom:50%;" />

<img src="https://i.loli.net/2020/08/14/enBmzycjkdP8O6X.png" alt="image-20200814155939882" style="zoom:50%;" />