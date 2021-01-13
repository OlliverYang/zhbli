---
title: '[NIPS2017] Adversarial Patch'
date: 2020-08-25 13:22:13
tags:
- NIPS2017
- Adversarial Attack
mathjax: true
---

## Approach

寻找对抗样本的传统方式如下：给定分类器 $P[y|x]$，输入为 $x\in R^n$，target class 为 $\hat y$，扰动为 $\varepsilon$，希望寻找 $\hat x$，最大化 $\log(P(\hat y|\hat x))$。

本文希望用图像块进行攻击，使用梯度下降进行优化。给定图像$x\in R^{w\times h\times c}$，patch $p$，patch location $l$，patch transformations $t$，我们定义 patch application operator $A(p,x,l,t)$。

为了获得 trained patch $\hat p$，我们使用 Expectation over Transformation (EOT) 的变种。具体来说，训练 patch 以优化如下目标函数：

<img src="https://i.loli.net/2020/08/25/QMpwKqsFERbr2vC.png" alt="image-20200825133041652" style="zoom:50%;" />

其中 $X$ 是图像训练集。

注意，本文的对抗补丁是通用的，即对任意图像都有效。