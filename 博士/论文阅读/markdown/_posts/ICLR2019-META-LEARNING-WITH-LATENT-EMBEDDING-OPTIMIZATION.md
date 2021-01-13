---
title: ICLR2019 META-LEARNING WITH LATENT EMBEDDING OPTIMIZATION
date: 2020-05-02 13:43:49
tags:
- ICLR2019
- Meta-Learning
mathjax: true
---

## Abstract

现有 meta-learning 算法的问题：由于数据量极少，而参数空间维度很高，这使得算法性能受到影响。

本文的解决方案：学习 data-dependent latent generative representation。提出 latent embedding optimization (LEO)，将基于梯度的自适应过程与模型参数的高维空间解耦。

## Introduction

基于优化的元学习方法旨在找到一组模型参数，可以通过几步梯度下降来适应一个任务。

但是，仅使用几个样本类计算高位参数空间中的梯度会导致泛化困难。

本文提出 LEO，学习模型参数的低维潜在嵌入，并在此空间中执行基于优化的元学习。

## MODEL

### PROBLEM DEFINITION

每个 task instance $\mathcal T_i$ 是采样自  task distribution $p(\mathcal T)$ 的分类问题。任务划分 a training meta-set $\mathcal S^{tr}$ , validation meta-set $S^{val}$ 和 test meta-set $S^{test}$。每个 task instance $\mathcal T_i$ 由 training set $\mathcal D^{tr}$ 和 validation set $\mathcal D^{val}$ 组成。训练集2 $\mathcal D^{tr} = \{(\mathbf x^k_n, y^k_n)|k=1...K;n=1...N\}$。验证集包含相同类别的其他样本。

### MODEL-AGNOSTIC META-LEARNING

MAML 是与本文相关的方法。对于一个模型 $f_\theta$，目的是找到参数 $\theta$，经过几次优化便可适应采样自同一 `distribution` 的 `task`。通过可微分的函数，将参数调整为  task-specific model parameters $θ'_i$，通常的更新方式为（公式 1）：

<img src="https://i.loli.net/2020/05/02/MJaUvfgWGdsZmjN.png" alt="image-20200502143727821" style="zoom:50%;" />

其中，$\mathcal G$ 通常是在 few-shot training set $\mathcal D^{tr}$ 上执行一次梯度下降：$\theta'_i=\theta-\alpha \nabla_\theta\mathcal L^{tr}_{\mathcal T_i}(f_\theta)$。

在 meta-training 时，更新参数 $\theta$ 以降低在 validation set $\mathcal D^{val}$ 上的误差：

<img src="https://i.loli.net/2020/05/02/uYzHdO5qWR98c4A.png" alt="image-20200502144405743" style="zoom:50%;" />

这一方法描述了基于优化的元学习的主要内容：

- initialization
- adaptation procedure (inner loop)：公式 1。
- termination (outer loop)：公式 2。