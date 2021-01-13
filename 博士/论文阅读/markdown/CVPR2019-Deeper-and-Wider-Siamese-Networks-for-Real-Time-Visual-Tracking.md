---
title: '[CVPR2019] Deeper and Wider Siamese Networks for Real-Time Visual Tracking'
date: 2020-05-15 09:59:30
tags:
- CVPR2019
- Tracking
categories:
- [Tracking, 未分类]
---

## Abstract

现有跟踪算法的问题: 无法使用更深的网络. 原因有

1. 神经元的感受野扩大,导致特征的判别性和定位精度下降.
2. 卷积的 padding 引起位置偏差.

本文的解决方案: 提出新的残差模块以消除 padding 的负面影响, 该模块可以控制感受野尺寸和网络步长.

## Analysis of Performance Degradation

###  Analysis

<img src="https://i.loli.net/2020/05/15/i4d8NtGOpm1Tglc.png" alt="image-20200515124624034" style="zoom:50%;" />

对于 alexnet, 对比 10 和 3, stride 从 4 变为 8, 精度从 0.59 变为 0.60. 对比 3 和 9, stride 从 8 变为 16, 精度从 0.60 降为 0.55.

对于 vgg, 对比 10 和 3, stride 从 4 变为 8, 精度从 0.58 变为 0.61, 对比 3 和 9, stride 从 8 变为 16, 精度从 0.61 降为 0.54.