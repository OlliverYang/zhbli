---
title: '[ECCV2018] Distractor-aware Siamese Networks for Visual Object Tracking'
date: 2020-05-14 11:20:32
tags:
- Tracking
- ECCV2018
mathjax: true
categories:
- [Tracking, Template Update]
- [Tracking, Global Search]
---

## Abstract

现有跟踪算法的问题: 现有孪生跟踪器仅能区分 `foreground` 和 `non-semantic backgrounds`. 而 `semantic backgrounds`, 即 `distractors`, 影响了跟踪的鲁棒性. 

本文的解决方案: 学习 `distractor-aware` 的孪生跟踪器.

我们观察到, 训练数据的不平衡分布使得学习到的特征具有较少的判别性. 因此, 在离线学习阶段, 引入有效的采样策略, 使得模型集中于 semantic distractors.

在测试过程中, 设计了 distractor-aware module, 以执行增量学习, 将 general embedding 迁移到 current video domain.

引入全局搜索机制, 进行 long-term 跟踪.

https://github.com/foolwood/DaSiamRPN

##  Distractor-aware Siamese Networks

### Distractor-aware Training

#### Diverse categories of positive pairs can promote the generalization ability

视频检测数据集中的物体类别很少: VID 为 20 类, YTB-BB 为 30 类. 因此本文引入 ImageNet Det 和 COCO Det  图像数据集来扩大 positive pairs 的类别, 从而提高跟踪器的判别性和回归能力.

#### Semantic negative pairs can improve the discriminative ability

本文将 semantic negative pairs 纳入训练中. 负对中的目标可以来自不同类别或相同类别. 来自不同类别的负对可以防止跟踪器漂移到其他物体. 来自相同类别的负对可以使跟踪器专注于细粒度表示.

###  Distractor-aware Incremental Learning

虽然上述训练策略可以提高网络的判别能力, 但是仍然很难区分两个相似物体.

原因是 general representation domain 和 specifical target domains 没有对齐.

本文设计了 distractor-aware module, 以执行增量学习, 将 general embedding 迁移到 current video domain.

首先, 采用 NMS 在每帧选择 distractors $d_i$, 收集 distractor set:

<img src="https://i.loli.net/2020/05/14/JmTPwNXogVpKe3z.png" alt="image-20200514120523992" style="zoom:50%;" />

即, 得分最高的 proposal 为 $z_t$, 剩余的得分较高的 proposals 为 distractors.

下面引入 distractor-aware objective function, 用于对 proposals $\mathcal P$ 进行重新排序. 其中 $\mathcal P$ 与 exemplar 具有 topk 相似性. 最终选择的目标为 $q$:

<img src="https://i.loli.net/2020/05/14/4XV3FkAT59xG7zH.png" alt="image-20200514121225610" style="zoom:50%;" />

这种计算方式使得计算复杂度和内存使用量增加了 n 倍. 由于上式是线性运算, 因此可以进行加速:

<img src="https://i.loli.net/2020/05/14/mJQnPR2djAlifG9.png" alt="image-20200514121429253" style="zoom:50%;" />

本文还提出以学习率 $\beta$ 更新 target templates 和 distractor templates:

<img src="https://i.loli.net/2020/05/14/rUE2esT36ISvYMc.png" alt="image-20200514121554034" style="zoom:50%;" />

### DaSiamRPN for Long-term Tracking

利用跟踪得分判断使用局部搜索还是全局搜索.