---
title: >-
  [AAAI2020] SiamFC++: Towards Robust and Accurate Visual Tracking with Target
  Estimation Guidelines
date: 2020-04-24 12:27:02
tags:
- AAAI2020
- Tracking
categories:
- [Tracking, Architecture]
---

作者提出 4 条设计准则：

- decomposition of classification and state estimation。
- classification score without ambiguity：在每个位置预测 1 个分类得分，并在该位置进行回归。
  - 基于 anchor 的机制为什么导致歧义？The anchor-based counterparts which consider the location on the input image as the center of multiple anchor boxes, output **multiple classification score at the same location** and regress the target bounding box with respect to these anchor boxes, leading to **ambiguous** matching between anchor and object. 同一个位置预测多个分类得分，这不好。
- tracking without prior knowledge：anchor 机制引入了先验，这是不好的。因此本文不基于 anchor 进行回归，而是直接进行回归。
  - 为什么 anchor 机制引入了先验？因为 anchor 指定了目标的尺度和长宽比。
- estimation quality score 质量得分：直接使用分类得分未必好。需要设计与分类得分无关的质量得分，作用是对预测的边框的质量进行打分。也就是说，对于一个位置，不仅能预测该位置有无目标，还能**预测**在该位置处的**预测**的边框质量。(**predict** the IoU score between **predicted** boxes and ground-truth boxes similar)

![image-20200320203024927](https://i.loli.net/2020/04/24/UqsEAreTQHgxkz8.png)

损失函数：

<img src="https://i.loli.net/2020/04/24/zjLS4EfopyeaZ8W.png" alt="image-20200424123222296" style="zoom:50%;" />

其中，$L_{cls}$ 是 focal loss，$L_{quality}$ 是用于 quality assessment 的 binary cross entropy (BCE) loss，$L_{reg}$ 是 IoU loss。注意，仅为正样本计算 $L_{quality}$ 和 $L_{reg}$。

本文中，使用 Prior Spatial Score (PSS) 计算 quality assessment：

<img src="https://i.loli.net/2020/04/24/t9jlfEwTJnCBdQL.png" alt="image-20200424123921051" style="zoom:50%;" />