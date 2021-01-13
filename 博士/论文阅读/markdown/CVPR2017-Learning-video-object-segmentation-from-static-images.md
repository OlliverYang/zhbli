---
title: '[CVPR2017] Learning video object segmentation from static images'
date: 2020-07-17 11:37:04
tags:
- CVPR2017
- Video Object Segmentation
mathjax: true
---

## Abstract

离线学习和在线学习相结合

- 离线学习：根据上一帧预测的mask，生成当前帧的mask。具体而言，对图片的mask进行变形/粗化`coarsening`，再对网络进行训练，从而利用不精确的mask预测精确的mask。
- 在线学习：捕获特定目标的表观。

## Introduction

先前的算法通过 CRF-like 或 GrabCut-like 等技术传播第一帧的分割结果。

> [26] N. Maerki, F. Perazzi, O. Wang, and A. Sorkine-Hornung. **Bilateral space video segmentation**. In CVPR, 2016. 1, 2, 5, 6, 7, 11, 12, 13
>
> [44] Y.-H. Tsai, M.-H. Yang, and M. J. Black. **Video segmentation via object flow**. In CVPR, 2016. 1, 2, 5, 6, 7, 11, 12, 13

对于每一帧，利用上一帧预测的mask，将网络引向感兴趣的目标。

## Method

<img src="https://i.loli.net/2020/07/17/MQx9JmzZlf8eoIa.png" alt="image-20200717142022144" style="zoom: 33%;" />

### Learning to segment instances offline

将分割网络输入从RGB扩展到RGB + mask通道（4个通道）。额外的mask通道为上一帧的分割结果，用于估计当前帧中目标的大概位置和形状。

分割过程包括两个步骤：粗化先前帧的mask，送入训好的网络以估计当前帧的mask。

### Learning to segment instances online

利用第一帧产生约1000个训练样本，然后继续微调先前离线训练的模型。