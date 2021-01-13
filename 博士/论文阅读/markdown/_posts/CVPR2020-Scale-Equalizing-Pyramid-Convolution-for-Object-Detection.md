---
title: '[CVPR2020] Scale-Equalizing Pyramid Convolution for Object Detection'
date: 2020-05-09 13:21:40
tags:
- CVPR2020
- Object Detection
mathjax: true
---

## Abstract

Feature pyramid 已经成为提取不同尺度特征的有效方法。该方法可以聚集不同 levels 的上下文信息，但很少涉及特征金字塔中的 inter-level correlation。

早期的计算机视觉方法通过在空间和尺度维度上定位 feature extrema 以提取 scale-invariant features。

受此启发，本文提出跨 pyramid level 的卷积，称为 pyramid convolution，这是一种改进的 3D 卷积。

Stacked pyramid convolutions 可以直接提取 3D（scale 和 spatial）特征，并胜过其他精心设计的特征融合模块。

基于 3D 卷积的观点，在 pyramid convolution 之后插入一个 integrated batch normalization，用于从整个特征金字塔中收集统计信息。

性能：

- https://github.com/jshilong/SEPC

<img src="https://i.loli.net/2020/05/09/i4hOgC5yXvqpLIc.png" alt="image-20200509133412684" style="zoom:50%;" />

> Performance on COCO-minival dataset of pyramid convolution in various single-stage detectors including RetinaNet [20], FCOS [38], FSAF [48], Reppoints [44], FreeAnchor [46]. Reference points of two-stage detectors such as Faster R-CNN (Faster) [31], Libra Faster R-CNN (L-Faster) [29], Cascade Faster R-CNN (C-Faster) [1] and Deformable Faster R-CNN (D-Faster) [49] are also provided. All models adopt ResNet-50 backbone and use the 1x training strategy.