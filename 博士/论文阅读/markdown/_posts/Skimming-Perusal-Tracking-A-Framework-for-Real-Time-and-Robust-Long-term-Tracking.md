---
title: >-
  [ICCV2019] 'Skimming-Perusal' Tracking: A Framework for Real-Time and Robust Long-term
  Tracking
date: 2020-05-04 10:13:47
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Global Search]
---

## Abstract

现有跟踪算法的问题：很少有工作研究 long-term tracking，并且性能也不理想。

本文的解决方案：提出 skimming and perusal modules，用于实时 long-term tracking。

- perusal module：由两部分组成。
  -  bounding box regressor：用于生成一系列 candidate proposals。
  -  target verifier：使用 confidence score 选择  optimal candidate。这一得分可以确定被跟踪对象是否存在，并在下一帧中选择跟踪策略——局部搜索或全局搜索。
- skimming module：为了加速全局搜索，从大量滑动窗口中有效选择最可能的区域。

性能：

- https://github.com/iiau-tracker/SPLT
- 在两个数据库上进行实验：VOT-2018 long-term 和 OxUvA long-term benchmarks。
- 速度：25.7 FPS。

## ‘Skimming-Perusal’ Tracking Framework

![image-20200504104709260](https://i.loli.net/2020/05/04/Sog4ABKWPQ6xjch.png)

###  Robust Local Perusal with Offline-learned Regression and Verification Networks

Perusal module 由离线学习的 SiamRPN model（用于产生候选款）和离线学习的 verification model（用于选择最好的候选框）组成。

最简单的方法是选择由 SiamRPN 产生的得分最高的候选框，但是这样容易漂移到近似目标。因此本文利用 SiamRPN 产生候选框，使用额外的 verifier 推断每个候选框的 confidence score。

#### Offline-learned Verification Network

学习 embedding function $f(\cdot)$ 将 target template 和 candidate proposals 嵌入到  discriminative Euclidean space 中。通过 triplet loss 进行训练：

<img src="https://i.loli.net/2020/05/04/ThQ4VIkOmxS2Rlq.png" alt="image-20200504105559340" style="zoom:50%;" />

通过 verifier 选择最佳候选框，且令最佳候选框的得分为 $c_{i^*}$。如果 $c_{i^*}$ 大于阈值，则在下一帧局部搜索，否则执行全局搜索。

#### Cascaded Training

首先分别训练 SiamRPN 和 verifier，然后将 perusal module 应用于训练集，收集错误分类的样本作为 hard examples。最后，使用这些样本微调 verifier。

### Efficient Global Search with Offline-learned Skimming Module

全局搜索非常耗时。VOT2018LT 冠军算法 [38] 速度不足 5 FPS。

> [38] Yunhua Zhang, Dong Wang, Lijun Wang, Jinqing Qi, and Huchuan Lu. Learning regression and verification networks for long-term visual tracking. CoRR, abs/1809.04320, 2018.

为了解决这一问题，本文提出 skimming module：给定 target template $\mathcal Z$ 和 search region $\mathcal X$，该模块学习函数 $p=g(\mathcal{Z,X})$，其中 $p$ 表示 目标是否出现在搜索区域中。

当进行全局搜索时，会密集采样一系列滑动窗口，在这些区域上应用 skimming module，选择得分最高的 $K=3$ 个区域运行 perusal module。

## Experiments

### Ablation Study

#### Effectiveness of Different Components

设计了四种变体：

1. R：仅使用 SiameseRPN。
2. S+R：仅使用 skimming module 和 SiamRPN。
3. R+V：不使用 skimming module。
4. S+R+V：最终的 skimming-perusal tracker。

#### Threshold θ for Dynamically Switching

该实验展示了不同的阈值对精度和速度的影响。

#### Parameter K for Skimming

该实验展示了参数 K 取不同的值对精度和速度的影响。

#### Different Verification Networks

该实验展示了不同的 backbone 对精度和速度的影响。