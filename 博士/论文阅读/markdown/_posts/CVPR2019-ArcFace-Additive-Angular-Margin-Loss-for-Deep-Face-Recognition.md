---
title: '[CVPR2019] ArcFace: Additive Angular Margin Loss for Deep Face Recognition'
date: 2020-04-21 13:45:14
tags:
- CVPR2019
- Face Recognition
mathjax: true
---

## Abstract

Centre loss 为实现类内紧凑型，在欧氏空间中惩罚特征到类中心的距离。

SphereFase 假定最后一个全连接层中的线性变换矩阵可以被作用角度空间中类中心的表示。因此以 multiplicative 方式惩罚特征和对应权重的角度。

最近，为了最大化人脸类别的可分离性，将 margins 整合到以后的损失中。

本文提出 Additive Angular Margin Loss（ArcFace）来获得高度判别行的特征。ArcFace 具有清晰的几何解释，因为它与超球上的测地距离具有确切的对应。

本算法取得了最好的性能，同时增加的计算量几乎可以忽略不计。

https://github.com/deepinsight/insightface

## Introduction

主要有两种方法训练人脸识别网络：

1. 使用 softmax 训练多类分类器。

   - softmax loss 的缺点：
     1. 线性变化矩阵的尺寸随类别数而增加。
     2. 难以适用于开集人脸识别任务。
   - 改进：
     - centre loss（ECCV2016）。缺点：训练时更新实际的中心很困难，因为人脸类别很多。
     - Sphereface（CVPR2017）。缺点：损失函数需要一系列近似，导致训练不稳定。为了稳定训练，与标准 softmax 混合训练。然而这又容易使 softmax 损失主导训练过程。
     - CosFace（CVPR2018）。

2. 直接学习 embedding（利用，使用 triplet loss）。triplet loss 的缺点：

   1. 大规模数据集中三元组数量会组合爆炸，导致更多的迭代次数。
   2. semi-hard sample mining 很困难。

本文方法的优点总结如下：

- Engaging：通过归一化超球面中角度和弧度之间的精确对应关系，直接优化了 geodesic distance margin。
- Effective：性能最优。
- Easy：仅需几行代码。不需要与其他损失函数整合以稳定训练，在任何训练集上都易于训练。
- Efficient：计算量很小，可以轻松对数百万个身份进行训练。

## Proposed Approach

### ArcFace

最常用的 softmax 分类损失定义如下：

<img src="https://i.loli.net/2020/04/21/M4UOceLat8jmFzA.png" alt="image-20200421151700044" style="zoom:50%;" />

其中，特征维度是 512。

softmax 的缺点：未明确优化 embedding，以使得类内样本更相似，类间样本更多样。从而导致当类内表观变化大或者测试集很大时性能不佳。

接下来对损失改进，使得学得的特征分布在半径为 $s$ 的超球上：

<img src="https://i.loli.net/2020/04/21/XfRs9zDEavAlSQo.png" alt="image-20200421151725782" style="zoom:50%;" />

进一步，我们通过添加 margin penalty 改善类内的紧凑性和类间的可分性。

<img src="https://i.loli.net/2020/04/21/qDaz3XLM9PTVIRY.png" alt="image-20200421151857337" style="zoom:50%;" />

### Comparison with SphereFace and CosFace

margin penalty 不同：

- multiplicative angular margin：SphereFace
- additive angular margin：ArcFace
- additive cosine margin：CosFase



