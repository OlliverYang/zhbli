---
title: '[arXiv2005] One-Shot Object Detection without Fine-Tuning'
date: 2020-05-11 10:46:34
tags:
---

## Method

### Model

#### Matching-FCOS

![image-20200511111250368](https://i.loli.net/2020/05/11/QpSTwAOl4qLJP98.png)

步骤如下：

1. Support instance patch 和 query image 以 siamese 方式送入共享权重的特征金字塔网络，以生成 support feature 和 query feature。
2. 对每个尺度上 support feature map 进行全局平均池化，得到 support instance patch 的 global representation。
3. Average-pooled support features 和 query features 都送入 heads 中以进行匹配。
4. 每个 head 计算 query features 中的每个像素与 global support feature 之间的 cosine similarity，得到 similarity map。
5. 将原始的 FCOS head 应用到 similarity map 上，得到 box proposals。

#### Structure-Aware Relation Module

![image-20200511113614914](https://i.loli.net/2020/05/11/5NmYuBIavMlrUPT.png)

由于第一阶段的 Matching-FCOS 的目标是高召回率，因此 support features 被全局平均池化了，损失了 support instance patches 的空间和结构信息。

SARM 的步骤如下：

1. 通过 ROI  Align，将 support features 和 query features 转变为 $N\times M$ 的特征图。
2. 添加一系列 pixel-wise 卷积块，强制网络比较 support feature map 和 query feature map 的局部特征。
3. Combined feature map 通过全连接层进行分类和回归。