---
title: '[CVPR2020] X3D: Expanding Architectures for Efficient Video Recognition'
date: 2020-04-20 16:23:58
tags:
- CVPR2020
mathjax: true
---

## Abstract

本文提出 X3D，在多个 network axes 上（space/time/width/depth），逐渐扩展 2D 图像分类网络。受机器学习中特征选择方法的启发，提出 stepwise network expansion 方法，在每个 step 扩展一个 single axis。为了将 X3D 扩展到指定的 target complexity，我们执行 progressive forward expansion 和 backward contraction。

我们最惊奇的发现是，具有高时空分辨率的网络性能很好，同时网络宽度和参数很小。

性能：

- https://github.com/facebookresearch/SlowFast
- 在达到最优性能的同时，加/乘法运算少了 4.8倍，参数少了 5.5 倍。

## Introduction

网络的深度指网络层数，宽度指通道数。

沿如下轴扩展网络：

- temporal duration $\gamma_t$
- frame rate $\gamma_\tau$
- spatial resolution $\gamma_s$
- width $\gamma_w$
- bottleneck width $\gamma_b$
- depth $\gamma_d$

2D 基础结构是 MobileNet。每次扩展一个轴，训练并验证，选择实现最佳计算量与性能折中的轴。重复执行这一操作以达到想要的 computational budget。