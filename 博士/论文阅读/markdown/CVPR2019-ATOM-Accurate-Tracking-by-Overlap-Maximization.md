---
title: '[CVPR2019] ATOM: Accurate Tracking by Overlap Maximization'
date: 2020-05-10 19:13:30
tags:
- CVPR2019
- Tracking
mathjax: true
categories:
- [Tracking, Model Update]
---

## Abstract

分类模块：

- 使用两层卷积。
- 使用共轭梯度法在线更新。

## Proposed Method

### Online Tracking Approach

#### Classification Model

分类头的第一层是 $1\times 1$ 卷积，输出通道数是 64。

分类头的第二层是 $4\times 4$ 卷积，输出通道数是 1。

在第一帧中，使用数据扩增获得 30 个初始样本，使用 $N_{\text{GN}}=6$ 和 $N_\text{CG}=10$ 优化两层。

在后续帧中，仅优化第二层，每 10 帧优化一次，$N_{\text{GN}}=1$，$N_\text{CG}=5$。

## Experiments

### Ablation Study

#### Online Optimization

提出两个梯度下降的变种：

1. GD：使用与本文算法相同的迭代次数。
2. GD++：运行 5 倍多的迭代次数。

<img src="https://i.loli.net/2020/05/10/UsuGXJISi4HPepg.png" alt="image-20200510194638437" style="zoom:50%;" />