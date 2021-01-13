---
title: >-
  [arXiv2005] IterDet: Iterative Scheme for Object Detection in Crowded
  Environments
date: 2020-05-13 11:31:56
tags:
- Object Detection
mathjax: true
---

## Abstract

代码：https://github.com/saic-vul/iterdet

## Introduction

类似的拥挤检测算法：

> [4] Zheng Ge, Zequn Jie, Xin Huang, Rong Xu, and Osamu Yoshie. **Ps-rcnn: Detecting secondary human instances in a crowd via primary object suppression**. arXiv preprint arXiv:2003.07080, 2020.
>
> [6] Eran Goldman, Roei Herzig, Aviv Eisenschtat, Jacob Goldberger, and Tal Hassner. **Precise detection in densely packed scenes**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 5227–5236, 2019.
>
> [8] Han Hu, Jiayuan Gu, Zheng Zhang, Jifeng Dai, and Yichen Wei. **Relation networks for object detection**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 3588–3597, 2018.
>
> [19] Russell Stewart, Mykhaylo Andriluka, and Andrew Y Ng. **End-to-end people detection in crowded scenes**. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 2325–2333, 2016.

## Proposed method

### Inference process

设原始的目标检测器为 $D$。对于一组边框 $B$，定义 history image $H$，与输入图像尺寸相同，每个像素表示已检测到的覆盖该像素的检测框的数量。如果我们将 history $H$ 和图像 $I$ 同时作为输入，则可设计对历史敏感的跟踪器 $D'$。

给定图像 $I$，以迭代方式产生一组边框 $B$。

第一次迭代：$t=1$，history $H$ 为空，$D'$ 将 $I$ 和 $H_0$ 映射为一组边框 $B_1$。

第二，$B_1$ 映射到历史 $H_2$，然后在迭代 $t=2$ 时映射到 $B_2$。直到 $|B_m|=0$ 停止迭代。

该方案需要考虑以下两点：

1. 如何将检测器 $D$ 修改成 $D'$。
2. 如何在每次迭代 $t$ 上强制 $D'$ 预测不同的目标 $B_t$。

### Architecture of a history-aware detector

History 被送入一个卷积层，与 backbone 的第一个卷积层输出相加。

### Training procedure

随机划分 ground truth boxes $\hat B$ 为两个子集 $B_{old}$ 和 $B_{new}$。将 $B_{old}$ 映射为 history $H$，令 $D'$ 预测 $B_{new}$。