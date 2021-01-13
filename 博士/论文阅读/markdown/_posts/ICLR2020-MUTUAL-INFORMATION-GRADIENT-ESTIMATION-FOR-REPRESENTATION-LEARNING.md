---
title: '[ICLR2020] MUTUAL INFORMATION GRADIENT ESTIMATION FOR REPRESENTATION LEARNING'
date: 2020-05-09 11:12:25
tags:
- ICLR2020
mathjax: true
---

## Abstract

Mutual Information (MI) 在 representation learning 中起着重要作用。但是，MI 在连续和高维环境中难以处理。最近的方法建立了易于处理且可扩展的 MI estimators，以发现有用的 representation。

然而，当 MI 较大时，大多数现有方法不能以低方差准确估计 MI。我们认为，直接估计 MI 的梯度比估计 MI 本身更有利于 representation learning。

为此，本文基于 implicit distributions 的 score estimation，提出 Mutual Information Gradient Estimator (MIGE)，用于 representation learning。MIGE 在高维和 large-MI 的情况下显示出紧密平滑的 MI 梯度估计。

我们扩展了 MIGE 在如下两方面的应用：

1. 基于 InfoMax 的 deep representations 的 无监督学习。
2. Information Bottleneck method。

## Introduction

Mutual information (MI) 是一种广泛应用于信息论和机器学习的度量标准，用于量化一对随机变量之间的共享信息量。具体来说，给定一对随机变量 $\mathbf x, \mathbf y$，表示为 $I(\mathbf x;\mathbf y)$ 的互信息定义为：

<img src="https://i.loli.net/2020/05/09/zoIy2s581qckhax.png" alt="image-20200509114509182" style="zoom:50%;" />

其中 $\mathbb E$ 是给定分布的期望。由于 MI 对于可逆且平滑的变换具有不变性，因此可以捕获变量之间的非线性统计依存关系。这些特性使其称为对 true dependence 的基本度量。

最近，基于 MI 的 unsupervised representation learning 方法得到复兴。一项具有开创性的工作是 InfoMax principle，给定 input instance $x$，InfoMax principle 的目标是，通过最大化输入与其表示之间的 MI，学习 representation $E_{\psi}(x)$。越来越多的近期研究表明，基于 MI maximization 的无监督歇息表现出有希望的性能。

另一个密切相关的工作是 Information Bottleneck method，其中 MI 用于限制 representations 的内容。具体而言，通过从原始数据中提取与任务相关的信息来学习 representations，同时丢弃与任务无关的内容。

最近的研究表明，通过控制 learned representations 与原始数据之间的信息量，可以调整训练模型的 desired characteristics，如泛化误差/鲁棒性/out-of-distribution data 的检测等。

尽管 MI 很重要，但是难以处理。精确的计算仅适用于离散变量或已知概率分布的部分问题。对于更一般的问题，MI 很难从样本中进行分析计算或估算。

多年来，已经开发了多种 IM estimators，如 likelihood-ratio estimators，binning，k-nearest neighbors，kernel density estimators 等。然而，这些 mutual information estimators 很少随维度和样本大小进行很好的缩放。

本文提出 MIGE，在高维和 large-MI 的情况下显示出紧密平滑的 MI 梯度估计。