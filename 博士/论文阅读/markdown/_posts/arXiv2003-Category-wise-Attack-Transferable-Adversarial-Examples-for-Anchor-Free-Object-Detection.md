---
title: >-
  [arXiv2003] Category-wise Attack: Transferable Adversarial Examples for Anchor
  Free Object Detection
date: 2020-08-19 21:02:30
tags:
- Adversarial Attack
- Object Detection
mathjax: true
---

## Approach

### Problem Formulation

$C_k$ 表示一个类别，总共有k类。在图像x中所有类别$C_k$实例的像素集合为$P_k$。p表示目标区域的一个像素。

优化问题如下：

<img src="https://i.loli.net/2020/08/19/oA3cndLDbNBEt1R.png" alt="image-20200819210731272" style="zoom:50%;" />

r为对抗扰动，f(x+r,p)表示分类得分向量(logistic)，$f_n(x+r,p)$表示向量的第n个值。$\arg\max_n(f_n(x+r,p))$表示在对抗样本$x+r$的像素p的预测的类别。$t_{\min}, t_\max$ 表示扰动范围。

本文中，将$P_k$近似为由CenterNet生成的类别$C_k$的heatmap。

### Category-wise Target Pixel Set Selection

第一步要做的是生成要攻击的target pixel set。

我们把overall heatmap上的detected pixels划分为target pixel set $\{P_1,P_2,...,P_k\}$。

通过设置 attack threshold $t_{attack}$ 来决定 target pixel set $P_k$，从而使得 $P_k$ 既包含 detected pixels，又包含 potential pixels：

<img src="https://i.loli.net/2020/08/19/gJIC2KFNw4WLG1n.png" alt="image-20200819212527678" style="zoom:50%;" />