---
title: '[CVPR2020] Detection in Crowded Scenes: One Proposal, Multiple Predictions'
date: 2020-04-24 13:47:17
tags:
- CVPR2020
- Object Detection
mathjax: true
---

## Abstract

https://github.com/Purkialo/CrowdDet

本文提出 proposal-based object detector，用于检测密集场景下高度重叠的物体。核心是令每个 proposal 预测一组 correlated instances 而不是仅预测一个。通过这种方式，相邻的 proposals 可以推断出相同的实例集，而不是区分 individuals，这使得训练更容易。

本文还提出：

- EMD loss，用于监督 instance set prediction 的学习。
- 新的后处理方法 Set NMS，用于删除来自不同 proposals 中的重复项，旨在消除传统 NMS 的缺点。
- 可选的优化模块 RM，用于处理潜在的 false positives。



## Introduction

拥挤场景检测失败主要有两个原因：

1. 高度重叠的物体通常具有非常相似的特征，因此很难为每个 proposal 分别生成准确的预测。
2. 相似预测很容易被 NMS 删除。

## Our Approach: Multiple Instance Prediction

对于每个 proposal box $b_i$，不是预测一个物体，而是预测 correlated set of ground-truth instances $G(b_i)$：

<img src="https://i.loli.net/2020/04/24/sONmBzkFbxn2MGr.png" alt="image-20200424140540286" style="zoom:50%;" />

其中 $\mathcal{G}$ 是锁帧 ground truth boxes。

### Instance set prediction

使用 $K$ 个 detection functions 来产生一组预测 $\text{P}(b_i)$：

<img src="https://i.loli.net/2020/04/24/413GMibfKuIWdSU.png" alt="image-20200424141003910" style="zoom:50%;" />

其中 $K$ 是常数，指 $G(b_i)$ 的 maximum cardinality。$\mathbf{c}_i$ 是 class label with confidence，$\mathbf{l}_i$ 是对应的坐标。

###  EMD loss

我们设计损失函数 $\mathcal{L}(b_i)$ 最小化预测 $P(b_i)$ 和 ground-truth instances $G(b_i)$。这可以归结为 set distance measurement 问题。因此我们设计 EMD loss 以最小化两个几何间的 Earth Mover‘s Distance：

<img src="https://i.loli.net/2020/04/24/UAMQDyGHm5Tz4pk.png" alt="image-20200424141412615" style="zoom:50%;" />

其中 $\pi$ 表示 $(1,2,...,K)$ 的一种具体排列。我们假设 $|G(b_i)|=K$，否则添加 dummy boxes（标签是背景，无回归损失）。

直觉上，要探索预测与真值之间所有可能的一对一匹配以找到最佳匹配。

### Set NMS

为原始 NMS 添加小补丁：每当一个框抑制另一个框之前，我们插入一个额外的测试，判断这两个框是否来自同一个 proposal。如果是，则跳过抑制。

### Refinement module

我们的算法可能导致更多的 false positives，因为我们产生了更多的预测。我们的 refine module 将预测与 proposal feature 作为输入，进行再次预测。