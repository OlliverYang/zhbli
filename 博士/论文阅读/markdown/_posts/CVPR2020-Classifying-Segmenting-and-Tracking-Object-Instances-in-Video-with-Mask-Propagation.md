---
title: >-
  [CVPR2020] Classifying, Segmenting, and Tracking Object Instances in Video
  with Mask Propagation
date: 2020-07-17 14:43:49
tags:
- CVPR2020
- Video Instance Segmentation
mathjax: true
---

## Abstract

本文提出 MaskProp，通过添加一个`mask propagation`分支使Mask R-CNN适应视频任务。

https://gberta.github.io/maskprop/

## Introduction

VIS任务：在每个帧中分割一组预定义类别的所有实例，并在整个序列上链接各个实例。

## Mask Propagation

多任务训练：

$L_t = L^{cls}_t + L^{box}_t + L^{mask}_t + L^{prop}_t$

<img src="https://i.loli.net/2020/07/17/l4qv7LGJd6b2iFt.png" alt="image-20200717151552327" style="zoom: 33%;" />

$M$: 预测的mask。$\tilde M$：对应的 ground truth。

### Mask Propagation Branch

提出的 Mask Propagation Branch 分为三部分：

1. instance-specific feature computation
2. temporal propagation of instance features
3. propagated instance segmentation

#### Computing Instance Specific Features

输入为单帧图片，输出对应的mask，利用该mask计算目标的特征$f_t^i$：将二值mask$M_t^i$与特征$f_t$逐元素相乘。

#### Temporally Propagating Instance Features

输入为t时刻的目标i的特征$f_t^i$，对其进行warping，得到propagated instance feature tensor $g^i_{t,t+\delta}$。

Warping 方式的计算：

- 计算 $f_t$ 和 $f_{t+\delta}$ 的 elementwise difference。
- 送入一个残差块，用于预测 motion offsets $o_{t,t+\delta}\in \mathbb R^{2k^2\times H'\times W'}$。

传播过程有两个输入：

1. motion offsets $o_{t,t+\delta}$
2. the instance feature tensor $f_t^i$。

输出为$g^i_{t,t+\delta}$。

#### Segmenting Propagated Instances

使用$g^i_{t,t+\delta}$预测第$t+\delta$帧的mask。

为了实现这一目的，首先计算新的特征$\phi^i_{t,t+\delta}=g^i_{t,t+\delta}+f_{t+\delta}$。