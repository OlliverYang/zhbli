---
title: '[CVPR2020] Revisiting the Sibling Head in Object Detector'
date: 2020-05-04 12:05:36
tags:
- CVPR2020
- Object Detection
mathjax: true
---

## Abstract

现有目标检测算法的问题：由 Fast RCNN 首先提出的 “shared head for classification and localization (sibling head)” 一直是目标检测的主流。但本文认为，在 sibling head 中的两个目标函数的 spatial misalignment 会严重损害训练过程。

本文的解决方案：使用非常简单的操作 task-aware spatial disentanglement (TSD) 解决 spatial misalignment。TSD 通过如下方式将分类和回归在空间维度上解耦：生成两个由共享的 proposal 估计的disentangled proposals。

合理性：对于一个 instance，在某些 salient area 的特征可能具有丰富的分类信息，而边界附近的特征有利于边框回归。该模块可以将检测性能一致提高约 3% mAP。

此外，本文提出 progressive constraint，以扩大 disentangled proposals 与 shared proposals 之间的 performance margin。该模块可将检测性能继续提高约 1% mAP。

性能：

- https://github.com/Sense-X/TSD
- ResNet-101 mAP=49.4
- SENet154 mAP=51.2

## Introduction

检测网络的分类头和回归头是两个不同的任务，但共享几乎相同的参数。因此一些工作意识到 sibling head 中两个目标函数之间的冲突，并试图找到一种折衷的方法。

IoU-Net [15] 是第一个研究此问题的工作。该文发现产生良好分类得分的特征可能对应着不太精确的边框。为了解决这一问题，引入一个额外的 head 来预测 IoU 作为 localization confidence。然后将 localization confidence 和 classification confidence 汇总起来作为最终的 classification score。这种方法的确减少了 misalignment 问题，但仍是一种折衷的方式，其背后的原理是相对提高 tight bounding box 的得分，并降低 bad bounding box 的得分。然而，在每个空间点，仍然存在 misalignment。

> [15] Borui Jiang, Ruixuan Luo, Jiayuan Mao, Tete Xiao, and Yuning Jiang. **Acquisition of localization confidence for accurate object detection**. In Proceedings of the European Conference on Computer Vision (ECCV), pages 784–799, 2018.

沿着这一研究方向，Double-Head R-CNN [35] 提出将 sibling head 分解成两个分支，分别用于分类和定位。然而，送入两个分支的特征是由同一 proposal 经过 ROI Pooling 产生的特征，因此两个任务之间仍然存在冲突。

> [35] Yue Wu, Yinpeng Chen, Lu Yuan, Zicheng Liu, Lijuan Wang, Hongzhi Li, and Yun Fu. Rethinking classification and localization in r-cnn. arXiv preprint arXiv:1904.06493, 2019.

本文重新审视了 misalignment 的本质，在 FPN 特征金字塔的每一层的输出特征图上探索分类和回归的空间敏感性。可以看出，在某些 salient area 的特征可能具有丰富的分类信息，而边界附近的特征有利于边框回归。这种空间维度上的 essential tasks misalignment 限制了性能提升。换句话说，如果检测器试图从相同的 spatial point/anchor 推断分类得分和回归结果，则总会得到不完美的权衡结果。

因此，本文提出 TSD 解决这一问题。TSD 的目标是在空间上分解分类和回归的梯度流。TSD 基于原始的分类头的 proposal，分别为两个任务生成两个 proposals。这允许两个任务自适应地寻找空间中的最优位置，而不会互相影响。

本文还提出了 progressive constraint，以扩大 disentangled proposals 与 shared proposals 之间的 performance margin。