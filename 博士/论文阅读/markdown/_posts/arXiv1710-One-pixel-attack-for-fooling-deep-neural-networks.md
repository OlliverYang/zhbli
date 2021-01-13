---
title: '[arXiv1710] One pixel attack for fooling deep neural networks '
date: 2020-08-23 12:50:58
tags:
- Adversarial Attack
mathjax: true
---

## METHODOLOGY

### Problem Description

$f$ 是图像分类器, 输入为用 $n$ 维向量表示的图片. $x=(x_1,...,x_n)$ 是被正确分为类别 $t$ 的原始图像. $x$ 属于类别 $t$ 的概率为 $f_t(x)$. 向量 $e(x) =(e_1,...,e_n)$ 是对抗扰动, 目标类别是 $adv$。优化问题为：

<img src="https://i.loli.net/2020/08/23/Fv2SqBQAkrwEHD6.png" alt="image-20200823130108759" style="zoom:50%;" />

本文的优化问题略有不同：

<img src="https://i.loli.net/2020/08/23/HU1Xehkf3TRGjYm.png" alt="image-20200823130157790" style="zoom:50%;" />

在单像素约束的情况下，$d=1$。