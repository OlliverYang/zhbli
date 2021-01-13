---
title: '[ICCV2019] Learning Discriminative Model Prediction for Tracking'
date: 2020-05-11 15:55:59
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Loss]
---

## Method

### Discriminative Learning Loss

本文提出的 model predictor $D$ 的输入是 $S_{train} = \{(x_j, c_j)\}_{j=1}^n$。$x_j \in \mathcal{X}$ 是 deep feature maps。$c_j \in \mathbb{R}^2$ 是 target center coordinate。我们的目标是预测 target model $f = D(S_{train})$。Model $f$ 是卷积层的滤波器权重，用于区分特征空间 $\mathcal X$ 中的的目标/背景外观。损失函数为：
$$
L(f) = \frac{1}{|S_{train}|}\sum_{(x,c)\in S_{train}}||r(x * f, c)||^2 + ||\lambda f||^2
$$
其中 $r(s,c)$ 在每个空间位置，基于 target confidence scores $s=x*f$ 和 ground-truth target center coordinate $c$ 计算残差。最常见的选择 $r(s,c)=s-y_c$，其中 $y_c$ 是每个位置的 desired target scores，通常是以 $c$ 为中心的高斯。

然而这样做的缺点是：

1. 所有负样本的置信都为0, 使得网络不得不更加关注负样本, 而不是获得更好的判别能力。解决方案：设计空间权重函数 $v_c$。
2. 未解决正负样本不均衡问题。在 $r$ 中采用 hinge-like loss，将背景区域中的得分裁剪为 0：$\max(0,s)$。含义是，如果背景的预测得分小于 0，则不需要计算 loss。因此，模型可以在背景中自由预测大的负值（easy samples），而不会增加损失。

为了兼顾最小二乘和 hinge loss 的优点，定义 residual function 为：
$$
r(s, c) = v_c \cdot (m_cs + (1 - m_c)\max(0, s) - y_c) 
$$
Target region 定义为 $m_c$，在每个空间位置 $t \in \mathbb{R}^2$ 中，$m_c(t) \in [0,1]$。

注意，target mask $m_c$，spatial weight $v_c$，regularization factor $\lambda$，和 regression target $y_c$ 都是可学习的。