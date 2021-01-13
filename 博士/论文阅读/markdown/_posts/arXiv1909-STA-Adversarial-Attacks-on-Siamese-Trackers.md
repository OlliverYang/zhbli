---
title: '[arXiv1909] STA: Adversarial Attacks on Siamese Trackers'
date: 2020-08-15 16:20:18
tags:
- Tracking
- Adversarial Attack
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## Generating Adversarial Example

### Siamese Tracker Attack

<img src="https://i.loli.net/2020/08/15/CGzKtJWwQsiVd2S.png" alt="image-20200815162307872" style="zoom:50%;" />

其中R(o;p)表示可微分的渲染过程。$o=(o_s,o_t)$表示3D目标。$o_s$表示 3D mesh，$o_t$ 表示纹理。p表示a collection of viewing parameters，包括相机距离，光照，视角，背景颜色等。

### Attack RPN-based Trackers

优化目标为：

<img src="https://i.loli.net/2020/08/15/PdhMZVk1Fvo6yr8.png" alt="image-20200815163309146" style="zoom:50%;" />