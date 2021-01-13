---
title: >-
  [AAAI2020] SPSTracker: Sub-Peak Suppression of Response Map for Robust Object
  Tracking
date: 2020-05-06 10:36:47
tags:
- AAAI2020
- Tracking
mathjax: true
categories:
- [Tracking, Feature Extraction]
---

## Abstract

现有跟踪器的问题：通常在如下假设下构建  online learning models——特征响应是以目标为中心的高斯分布。然而，当存在其他物体或背景噪声的干扰时，这种假设是不合理的，这些干扰会在 跟踪响应图上产生 sub-peaks 并导致模型漂移。

本文的解决方案：提出 rectified online learning approach，用于抑制 peak response，并处理 progressive interference。

本文的方法称为 SPSTracker，应用简单高效的 Peak Response Pooling (PRP) 来聚合和对齐 discriminative features，同时利用 Boundary Response Truncation (BRT) 以减少特征响应的方差。通过多尺度特征融合，SPSTracker 将多个 sub-peaks 的 response distribution 聚集到一个最大峰值，这增强了特征的判别能力。

性能：

- https://github.com/TrackerLB/SPSTracker
- 在如下数据集进行实验：OTB2013，OTB2015，OTB50，VOT2016，VOT2018 和 NFS。

## Introduction

现有方法忽略了来自  context area 的 gressive interference。如何直接建模 interference，并调整跟踪的 response distribution，仍是开放性问题。

本文认为，大多数跟踪错误是由于目标周围的 intereference 造成的。这种 interference 会产生 multi-peak tracking response，sub-peak 可能会逐渐 “增长” 并最终导致模型漂移。因此本文提出抑制 sub-peaks，以得到 single-peak response，从 tracking response regularization 的角度阻止模型漂移。

具体来说，本文引入了 Peak Response Pooling (PRP) 模块，该模块将跟踪响应的最大值集中到目标的几何中心。通过对 tracking response maps 有效地执行 maximization 和 substitution 操作，实现池化过程。

在网络前传过程中，PRP 将多个 sub-peaks 的 response distribution 聚集到一个 centered peak 进行跟踪。在网络反向传播过程中，具有单峰的响应图指导在线学习。

基于 PRP，本文进一步提出 Boundary Response Truncation (BRT) 来裁剪响应图——将远离峰值的像素值设为 0。这一操作减小了特征相应图的方差 ，同时进一步聚合了 singlepeak response。

如果将响应图近似为高斯分布，则 PRP 的作用是聚合均值，BRT 的作用是减少方差。

SPSTracker 基于 CNN 构建，在卷积层顶部具有目标分类分支和目标定位分支。配备有 PRP 和 BRT 模块的分类网络可识别粗略位置（边界框）。将这些粗略位置进一步馈送到目标定位分支，以估算精确的目标位置。

## Methodology

![image-20200506151252554](https://i.loli.net/2020/05/06/ntLSqXBEMP9r5zj.png)

### Tracking Response Prediction

公式 1：

<img src="https://i.loli.net/2020/05/06/weDZVrkPOfv2X7Q.png" alt="image-20200506143405641" style="zoom:50%;" />

公式 2：

<img src="https://i.loli.net/2020/05/06/qblUiQV1CDSvPT3.png" alt="image-20200506143422287" style="zoom:50%;" />

### Sub-Peak Response Suppression

公式 3/4：

<img src="https://i.loli.net/2020/05/06/vVJFpQID7gqRmAG.png" alt="image-20200506143301651" style="zoom:50%;" />

其中 $P$ 指应用于每个 sampled response map 的 Peak Response Pooling，$g(x_j)$ 指经过 BRT 操作后的特征。

通过最小化公式 1，可以强制响应图近似高斯先验 $y_j$。然而对于部分遮挡或有背景噪声的目标，$f(x_j,w)$ 可能不是高斯分布。公式 3/4 可以使 $f'(x_j,w)$ 更接近高斯先验。

### Peak Response Pooling (PRP)

在分类分支输出的响应图上，首先执行 horizontal PRP，将响应图集中到 horizontal pooling map 上：通过在响应图的每一行找到最大响应并为该行的所有像素分配最大最大响应值以完成该过程。

类似地，在响应图的每一列执行 vertical PRP，以获得 vertical pooling map。

因此，经过 PRP 操作的响应图中的每个元素计算如下：

<img src="https://i.loli.net/2020/05/06/REFAGLDK8BdNuso.png" alt="image-20200506144953572" style="zoom:50%;" />

其中 $x_{pq}$ 指原始响应值。

将 horizontal/vertical pooling maps 相加以获得 rectified response map，该响应图倾向于将大的响应值聚合到目标中心。在多次**迭代学习**后，目标将响应图近似于高斯分布。

<img src="https://i.loli.net/2020/05/06/SYTU6R9yfj4D5gn.png" alt="image-20200506150224415" style="zoom:33%;" />

由上图可知，双峰变成了单峰。

PRP 受目标检测中的 center/corner pooling 所启发。

> Duan, K.; Bai, S.; Xie, L.; Qi, H.; Huang, Q.; and Tian, Q. 2019. **Centernet: Keypoint triplets for object detection**. In CVPR.
>
> Law, H., and Jia, D. 2018. **Cornernet: Detecting objects as paired keypoints**. International Journal of Computer Vision 1–15.

### Boundary Response Truncation (BRT)

PRP 模块可以将目标响应集中到目标中心，但不考虑目标响应的方差。在复杂的场景中，目标边界响应可能具有较大的方差，这称为边界效应。考虑到方差小的单峰响应图可以减轻边界效应并提高跟踪的鲁棒性，本文进一步提出 BRT 操作。

BRT 是一种简单的 clip operation，将远离峰值响应的像素设为 0。

## Experiment

### Ablation Study

<img src="https://i.loli.net/2020/05/06/Yaht8gmkEHVxFqS.png" alt="image-20200506151528717" style="zoom:50%;" />