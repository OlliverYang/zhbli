---
title: '[CVPR2020] Video Panoptic Segmentation'
date: 2020-07-17 16:21:14
tags:
- CVPR2020
- Video Panoptic Segmentation
mathjax: true
---

## Introduction

提出 video panoptic segmentation network (VPSNet)。VPSNet基于UPSNet（最好的图像全景分割算法之一）。

VPSNet采用一个额外帧作为参考，以关联时间信息。

提出基于flow的特征图对齐模块，以及非对称attention block。用于计算target和reference特征的相似性。

align模块学习flow warping，用于对齐target和reference特征。

align模块的输入是由flownet2计算的光流。

attend模块的输入是串接的对齐特征。