---
title: >-
  [IJCAI2019] Transferable adversarial attacks for image and video object
  detection
date: 2020-08-20 17:06:18
tags:
- IJCAI2019
- Adversarial Attack
- Object Detection
mathjax: true
---

<img src="https://i.loli.net/2020/08/21/csU5w1u8gdG26zP.png" alt="image-20200821105203742" style="zoom:50%;" />

## Methodology

### Problem Definition

给定图像I，目的是生成对抗图像$\hat I$，以攻击检测器Dt。对于图像中的ground truth object $(B_i,C_i)$, $B_i$是边框，$C_i$是标签。

假设检测器成功检测到该目标并输出$(b_i,c_i)$，其中$B_i$和 $b_i$的IoU大于0.5，而且$C_i=c_i$。

定义$(\hat b_i,\hat c_i)$为该对象在$\hat I$上的检测结果。如果$\hat b_i$和$B_i$的IoU小于0.5，或者$\hat c_i\ne C_i$，就认为攻击成功。

### Unified and Efficient Adversary

条件GAN的目标函数为：

<img src="https://i.loli.net/2020/08/20/CZvWtjqVUyA5H3G.png" alt="image-20200820194105289" style="zoom:50%;" />

G用于生成对抗样本，D区分对抗/干净样本。

### Network Architecture

pix2pix

### Loss Functions

分类损失：

<img src="https://i.loli.net/2020/08/20/NOJtQ8a2Dfoy1wY.png" alt="image-20200820194705620" style="zoom:50%;" />

X是检测器在图像I上提取的特征图，$\tau=\{t_1,t_2,...,t_N\}$是X上所有候选区域的集合。$t_n$是来自RPN的第n的候选区域。$l_n$是$t_n$的真实标签，$\hat l_n$是错误标签，从其他类中随机选择。$f_{l_n}(X,t_n)\in R^C$是候选区域$t_n$的分类得分向量（softmax之前）。实验时，选择得分大于0.7的候选框，以构成$\tau$。

本文还提出了 multi-scale attention feature loss：

<img src="https://i.loli.net/2020/08/20/HOAjx5e8hMZPuzK.png" alt="image-20200820195745848" style="zoom:50%;" />

$X_m$是第m层的特征图。$R_m$是一个随机的、固定的特征图。$A_m$是attention weight。

用 $s_n$ 表示 $t_n$ 的得分。

总损失为：

<img src="https://i.loli.net/2020/08/20/jvkEygSJTm7wLFf.png" alt="image-20200820204209507" style="zoom:50%;" />

