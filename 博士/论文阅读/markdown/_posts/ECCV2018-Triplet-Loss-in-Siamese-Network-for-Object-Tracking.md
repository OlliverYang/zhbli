---
title: '[ECCV2018] Triplet Loss in Siamese Network for Object Tracking'
date: 2020-05-02 10:27:50
tags:
- ECCV2018
- Tracking
mathjax: true
categories:
- [Tracking, Loss]
---

## Abstract

现有跟踪算法的问题：孪生网络仅用了样本的成对关系，忽略了三元组关系。

本文的解决方案：将 triplet loss 应用到 3 个孪生跟踪器（SiamFC、CFnet2 和 SiamImp），验证了有效性。

性能：

- https://github.com/shenjianbing/TripletTracking

- 在 3 个数据集上进行实验： OTB-2013，OTB-100 和 VOT-2017。

## Siamese network with triplet loss

可以将 SiamFC 中的  instances set（即 instance input）$\mathcal X$ 拆分成 positive instances set $\mathcal X_p$ 和 negative instances set $\mathcal X_n$。

类似地，将  exemplar-instance pairs 的 similarity score set $V$ 划分成 positive score set $\mathcal V_p$ 和 negative score set $\mathcal V_n$。

<img src="https://i.loli.net/2020/05/02/3U51STD7iB9tC8w.png" alt="image-20200502104928802" style="zoom:50%;" />

其中 $vp$ 表示 exemplar-positive pair 的 similarity score，$vn$ 表示 exemplar-negative pair 的 similarity score。

本文提出的 triplet loss 定义如下：

<img src="https://i.loli.net/2020/05/02/t9Hm4VrbXUyxWDQ.png" alt="image-20200502104953478" style="zoom:50%;" />

## Relationship between logistic loss and triplet loss

两种损失的区别为：

<img src="https://i.loli.net/2020/05/02/2OVcmUKo9xTAQb4.png" alt="image-20200502105951152" style="zoom:50%;" />

### Comparison on the gradients

对于 logistic loss，梯度为：

<img src="https://i.loli.net/2020/05/02/L3fa4WvtgDCXRu5.png" alt="image-20200502110138148" style="zoom:50%;" />

对于 triplet loss，梯度为：

<img src="https://i.loli.net/2020/05/02/AWtNxcUeI8kudYo.png" alt="image-20200502110212416" style="zoom:50%;" />

这意味着 logistic term 不能充分利用 $vp$ 和 $vn$ 提供的信息。
换句话说，$\partial T_l/\partial v_p$ 无法利用来自 $vn$ 的信息，$\partial T_l/\partial v_n$ 无法利用 $vp$ 的信息。

## Experimental results

### Experiments on baseline trackers

对三种变体进行对比实验：SiamFC，SiamFC-init，SiamFC-tri。其中 SiamFC-tri 指 在 SiamFC 基础上加了 triplet loss 后继续训练，siamFC-init 指仍使用原始损失继续训练。