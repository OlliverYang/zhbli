---
title: '[CVPR2020] Temporally Distributed Networks for Fast Video Segmentation'
date: 2020-07-30 17:12:27
tags:
- Video Semantic Segmentation
- CVPR2020
mathjax: true
---

## Abstract

作者观察到，可以将若干较浅子网的特征进行组合，以近似一个 deep CNN 的高层特征。

利用视频中固有的时间连续性，作者将这些子网分布到连续的帧上。

因此，在每个 time step 上，只需执行轻量级计算，即可从单个子网中提取一个 sub-features group。

用于分割的 full features 由一个注意力传播模块得到，该模块的作用是对帧间的几何形变进行补偿。

另外，还引入了知识蒸馏损失，以进一步提高 full features 和 sub-features 的表示能力。

<img src="https://i.loli.net/2020/07/30/WzG4AfpaBd97YFI.png" alt="image-20200730173633845" style="zoom:50%;" />

## Introduction

进行视频语义分割最直接的方法是在每帧独立应用图像语义分割算法，但这样就无法利用视频中的时间信息。

一种解决方案是添加额外的层来建模时间上下文，以提取更好的特征 [11,20,23,35]。由于必须在每一帧重新计算所有特征，因此这些方法效率较低。

> [11] *R. Gadde, V. Jampani, and P. V. Gehler (2017)* **Semantic video cnns through representation warping**. In CVPR
>
> [20] *X. Jin, X. Li, H. Xiao, X. Shen, Z. Lin, J. Yang, Y. Chen, J. Dong, L. Liu, Z. Jie, et al. (2017)* **Video scene parsing with predictive feature learning**. In ICCV
>
> [23] *A. Kundu, V. Vineet, and V. Koltun (2016)* **Feature space optimization for semantic video segmentation**. In CVPR
>
> [35] *D. Nilsson and C. Sminchisescu (2018)* **Semantic video segmentation by gated recurrent flow propagation**. In CVPR

为了减少冗余计算，一种合理的方法是仅在关键帧上应用图像分割模型，然后在其他帧中复用高层特征[19,27,31,60]。关键帧与其他帧

> [19] *S. Jain, X. Wang, and J. E. Gonzalez (2019)* **Accel: a corrective fusion network for efficient semantic segmentation on video**. In CVPR
>
> [27] *Y. Li, J. Shi, and D. Lin (2018)* **Low-latency video semantic segmentation**. In CVPR
>
> [31] *B. Mahasseni, S. Todorovic, and A. Fern (2017)* **Budget-aware deep semantic video segmentation**. In CVPR
>
> [60] *X. Zhu, Y. Xiong, J. Dai, L. Yuan, and Y. Wei (2017)* **Deep feature flow for video recognition**. In CVPR

