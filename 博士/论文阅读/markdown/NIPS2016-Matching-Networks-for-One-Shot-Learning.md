---
title: '[NIPS2016] Matching Networks for One Shot Learning'
date: 2020-04-19 17:41:18
tags:
- NIPS2016
- One Shot Learning
mathjax: true
---

## Abstract

本文的框架学习一个网络，该网络将一个小的`有标签支持集`和一个`无标签样本`映射到它的标签，无需微调以适应新的 `class types`。

然后，本文定义了视觉和语言任务上的 one-shot learning 问题。

## Introduction

One shot learning 指：使用一个有标签样本学习一个类别。

我们希望同时整合 parametric models 和 non-parametric models 的最佳特性，即可以快速获取 new examples，同时对 common examples 泛化良好。

## Model

我们的非参数化方法包括两个组件：

1. 给定小的支持集 $S$，我们的模型为每个 $S$ 定义一个函数（分类器） $c_S$，即一个映射 $S \rightarrow c_S(\cdot)$。
2. 设计了学习策略，专用于从支持集 $S$ 中进行 one-shot learning。 

### Model Architecture

我们希望建立从小的支持集（具有 $k$ 个样本的 input-label 对）$S=\{(x_i,y_i)\}_{i=1}^k$ 到分类器 $c_S(\hat x)$ 的映射。该分类器给定一个 test example $\hat x$，定义输出 $\hat y$ 的概率分布。其中，$\hat x$ 是一幅图像，$\hat y$ 是图像类别的分布。我们将映射 $S \rightarrow c_S(\hat x)$ 定义为 $P(\hat y|\hat x, S)$，其中 $P$ 由神经网络进行参数化。当给出新的支持集 $S'$ 进行 one-shot learning 时，只需使用由神经网络定义的 $P$ 来为每个测试样本 $\hat x$ 预测近似标签分布 $\hat y$：$P(\hat y|\hat x,S')$。我们的模型以最简单的方式计算 $\hat y$ 的概率分布：

<img src="https://i.loli.net/2020/04/19/6lC5VkLwouOxTcR.png" alt="image-20200419210932733" style="zoom:50%;" />

其中 $x_i,y_i$ 是来自支持集 $S=\{(x_i,y_i)\}_{i=1}^k$ 的输入和标签分布。$a$ 是 attention 机制。注意，该公式的本质是将新类别的输出描述为支持集中标签的线性组合。

#### The Attention Kernel

注意力机制 $a(\cdot, \cdot)$ 的最简单形式是在余弦距离上使用 softmax：

<img src="https://i.loli.net/2020/04/19/tfde1WaclBpEjXk.png" alt="image-20200419211508786" style="zoom:50%;" />

其中，$f$ 和 $g$ 分别用于编码 $\hat x$ 和 $x_i$。

#### Full Context Embeddings

我们认为，$g(x_i)$ 不应该仅依赖 $x_i$ 而于支持集 $S$ 的其他元素无关。因此我们提出 $g$ 不仅要依赖 $x_i$，还要依赖 $S$：因此有 $g(x_i, S)$。这在有些元素 $x_j$ 与 $x_i$ 非常接近时会有用，此时会以更好的方式编码 $x_i$。我们用双边 LSTM 在支持集 $S$ 的上下文中嵌入 $x_i$。

同时我们认为，$f$ 应该同时依赖 $f$ 和 $S$。可以设计一个在整个支持集 $S$ 上具有 read-attention 的 LSTM 来实现。