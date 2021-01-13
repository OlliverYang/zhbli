---
title: >-
  [CVPR2020] A Disentangling Invertible Interpretation Network for Explaining
  Latent Representations
date: 2020-05-02 09:36:08
tags: CVPR2020
mathjax: true
---

## Abstract

现有神经网络的缺点：是黑盒模型，其 hidden representations 缺乏可解释性。

本文的解决方案：将 interpretation 形式化为——从 hidden representation 到 semantic concepts 的转换。

本文提出的  invertible interpretation network 将 hidden representation 分解为单独的语义概念。

此外，本文提出的有效的方法定义语义概念，方法是仅绘制两个图像，同时提供一种无监督的策略。

## Approach

### Interpreting Hidden Representations

#### Invertible Transformation of Hidden Representations

定义 $f$ 为需要解释的神经网络。$f$ 将输入图像 $x\in \mathbb R^{h\times w\times 3}$ 映射到若干隐层，最终的输出为 $f(x)$。

一个隐层的  intermediate activations $E(x) \in \mathbb R^{H\times W\times C}$ 是图像 $x$ 的 task-specific representation。本文的目的是将这种 hidden representations 转换成人类可理解的表示。

我们定义 $z = E(x) \in \mathbb R^{H\cdot W\cdot C}$ 为需要解释的 hidden representation 的向量表示，长度为 $N=H\cdot W\cdot C$。

将生成 $z$ 之前的子网络定义为 $E$，将生成 $z$ 之后的自网络定义为 $G$：$f(x) = G\odot E(x)$。

为了将 $z$ 转换成 interpretable representation，我们将  distributed representation $z$ 转换成 factorized representation $\tilde z = (\tilde z_k)^K_{k=0} \in \mathbb R^N$。

$\tilde z_k \in \mathbb R^{N_k}, \sum_{k=0}^K N_k=N$，含义是 interpretable concept。

#### Disentangling Interpretable Concepts

$\tilde z_k$ 之间应该是相互独立的，这意味着 joint density 的分解：$p(\tilde z) = \Pi_{k=0}^K p(\tilde z_k)$。

本文指定每个 factor 为正态分布：

<img src="https://i.loli.net/2020/05/02/nFWTm4jxutYqfGb.png" alt="image-20200502101252495" style="zoom:50%;" />