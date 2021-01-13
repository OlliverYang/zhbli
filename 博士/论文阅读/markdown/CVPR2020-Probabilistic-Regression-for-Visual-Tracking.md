---
title: '[CVPR2020] Probabilistic Regression for Visual Tracking'
date: 2020-04-24 19:28:44
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Loss]
---

## Abstrat

https://github.com/visionml/pytracking

现有跟踪算法的问题：表示目标估计的不确定性很重要。现有算法虽然估计了 confidence score，但是缺少清晰的概率解释。

本文的解决方案：提出 probabilistic regression formulation，为目标状态估计 `conditional probability density`。我们的方法可以建模标签噪声。网络通过最小化 KL 散度进行训练。

## Introduction

目标跟踪可以建模为一个回归问题。这些跟踪算法的共同做法是：对于`一幅图像` $x$，给定任意状态 $y$，预测一个 confidence value $s(y,x)$，target state 通过最大化 predicted confidence 来获得：$y^* = \arg\max_ys(y,x)$。

上述提及的 `confidence-based regression` 方法被 DCF 和孪生跟踪器所共享，这两种方法都在每个**空间位置** $y$ 上执行卷积操作来获得 target confidence $s(y,x)$ 以定位目标。也有些方法进行边框回归：预测 entire target box $y$ 的 confidence $s(y,x)$。

`confidence-based regression` 的一个优点是可以建模不确定性。相反，对于直接回归方法，$y=f(x)$ 让网络做出 single prediction $y$，无法提供其他信息。

然而，confidence value $s(y,x)$ 没有清晰的解释，因为仅仅用于求最大化。因此，取值范围和 predicted confidence 的特性在很大程度上取决于损失函数和用于训练的 `pseudo labels`。

### Contributions

我们提出学习预测 `conditional probability density` $p(y|x)$。与 confidence value $s(y,x)$ 不同，density  $p(y|x)$ 具有清晰直接的解释，允许计算绝对概率。

## Regression by Confidence Prediction

### General Formulation

在计算机视觉中，回归是一个基本的问题，用于学习从输入空间 $\mathcal{X}$ 到连续输出空间 $\mathcal{Y}$ 的映射 $f_\theta : \mathcal{X \rightarrow Y}$。

在计算机视觉的一些任务中，会采用直接回归的方法。但是在另一些工作中，网络会预测一个 confidence score。这种 confidence prediction 相比于直接回归由两个好处：

1. confidence prediction 可以捕获输出空间 $\mathcal Y$ 中的不确定性、多假设和歧义。
2. 网络可以利用 $\mathcal{X}$ 和 $\mathcal{Y}$ 共享的对称性，如平移不变性。

定义 $\mathcal X$ 为图像空间。

定义 `confidence-based regression` 为学习一个函数 $s_\theta: \mathcal{Y\times X}\rightarrow \mathbb{R}$，用于预测一个标量置信度得分 $s_\theta (y,x)\in \mathbb{R}$。$(y,x)$ 为 input-output pair。Final estimation $f(x) = y^*$ 通过下式计算：

<img src="https://i.loli.net/2020/04/24/p9kYaRDuE5s3UKW.png" alt="image-20200424193424270" style="zoom:50%;" />

这时，回归问题就转变成了从数据 $\{(x_i,y_i)\}_i$ 中学习函数 $s_\theta$。这通常需要定义一个 `pseudo label` $a(y,y_i), a:\mathcal{Y\times Y}\rightarrow\mathbb{R}$，作为 prediction $s_\theta (y,x_i)$ 的 ground-truth confidence value。注意，此处的 $y_i$ 表示图像 $x_i$ 的 ground truth，是一个固定值。而 $y$ 表示空间上的任意位置。

<img src="https://i.loli.net/2020/04/24/l1DGzs5ARI2uYVn.png" alt="image-20200424193438062" style="zoom:50%;" />

其中损失函数 $\ell:\mathbb{R\times R\rightarrow R}$ 表示 predicted confidence value $s_\theta(y,x_i)$ 和对应的 label value $a(y,y_i)$ 之间的差异。实际上，损失函数和 `pseudo label functions` $a$ 针对不同的任务有多种选择。

### In Visual Tracking

在目标跟踪中，需要回归的状态通常表示为边框 $y\in\mathbb R^4$。然而由于困难性，以前的方法常常回归边框中点 $y\in\mathbb R^2$。

DCF 跟踪器：

<img src="https://i.loli.net/2020/04/24/HEYuaziDn8xoZJ6.png" alt="image-20200424193451723" style="zoom:50%;" />

其中 $w_\theta$ 是卷积核，$\phi(x)$ 是图像特征。DCF 的损失函数为 $\ell(s,a)=(s-a)^2$。几乎所有的 DCF 方法的 pseudo label 为 $a(y,y_i)=e^{-\frac{||y-y_i||^2}{2\sigma^2}}$。

孪生跟踪器：

<img src="https://i.loli.net/2020/04/24/248BmdOJqrDCMaU.png" alt="image-20200424193502831" style="zoom:50%;" />

孪生跟踪器的损失函数通常为 `binary cross entropy loss`：

<img src="https://i.loli.net/2020/04/24/KwHlbf81npSrMqN.png" alt="image-20200424193511207" style="zoom:50%;" />

孪生网络的 pseudo label 为 $a(y,y_i)\in[0,1]$。

## Method

本文提出 `probabilistic regression model`，整合上述 `confidence-based regression` 的所有优点。与上述方法不同，我们的方法的输出是 `predictive probability distribution` $p(y|x_i,\theta)$。网络通过优化 predictive density $p(y|x,\theta)$ 和 `conditional ground-truth distribution` $p(y|y_i)$ 的 KL 散度来训练，这样可以建模标签噪声和任务歧义。$p(y|y_i)$ 取代了 $a$ 的作用。

### Representation

给定输入 $x$，预测输出 $y$ 的 `probability distribution` $p(y|x,\theta)$。

<img src="https://i.loli.net/2020/04/24/vig5G3JWL2URtTd.png" alt="image-20200424193530376" style="zoom:50%;" />

该公式通过取幂并除以归一化常数，将 $s_\theta$ 转化为 `probability density`。注意，上式是在任意输出空间 $\mathcal Y$ 上应用 SoftMax 的直接泛化。

给定训练样本对 $\{(x_i,y_i)\}_i$，最简单的训练方法是最小化 `negative log-likelihood`：

<img src="https://i.loli.net/2020/04/24/nZ2oYrqLU8MASju.png" alt="image-20200424193542299" style="zoom:50%;" />

接下来讨论该方法的缺点。

###  Label Uncertainty and Learning Objective

通常采用边框的中心点作为标签。但是有些边框的中心并不具有语义信息。因此使用边框中心点进行训练会产生歧义。另外，标注的边框有时不是特别准。然而这些因素在训练时常常不被考虑。为了解决这一问题，我们通过最小化 KL 散度来训练网络：

<img src="https://i.loli.net/2020/04/24/VtXgPEn5krApIlv.png" alt="image-20200424193601783" style="zoom:50%;" />

该公式描述了两个分布之间的 cross entropy。

补充：KL 散度是两个概率分布之间差别的非对称性度量。当且仅当两个分布相同时，kL 散度等于 0。

与 `pseudo label function` $a(y|y_i)$ 不同，$p(y|y_i)$ 具有明确的概率分布解释。在高斯模型 $p(y|y_i)=\mathcal N(y|y_i, \sigma^2)$ 的情况下，方差 $\sigma^2$ 可以轨迹为 annotations 的经验方差。本文仅将方差视为超参数。

补充：$p(y|y_i)=\mathcal N(y|y_i, \sigma^2) = \frac{1}{\sqrt{2\pi}\sigma}\exp(-\frac{(y_i-\mu)^2}{2\sigma^2})$。
