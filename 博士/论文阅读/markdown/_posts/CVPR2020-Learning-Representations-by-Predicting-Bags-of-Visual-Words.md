---
title: '[CVPR2020] Learning Representations by Predicting Bags of Visual Words'
date: 2020-04-20 14:38:42
tags:
- CVPR2020
- Self-Supervised Learning
mathjax: true
---

## Abstract

提出基于 spatially dense image descriptions 的自监督方法，编码了离散的视觉概念（visual words）。

为了建立这种离散表示，我们通过基于词表的 k-means，对预训练的自监督网络的特征图进行量化。然后我们自监督训练另一个网络，预测图像的 visual words 的直方图（Bags-of-Words），该网络的输入是经过扰动的图像。

## Introduction

## Approach

![image-20200420144105047](https://i.loli.net/2020/04/20/se2IuhaMJ438yHL.png)

我们的目的是，以无监督形式训练网络 $\Phi(\cdot)$，使得为图像产生“好”的特征表示。“好”指的是，有利于图像分类，目标检测等视觉任务。

我们假设有一个可用的初始自监督预训练网络 $\hat \Phi(\cdot)$，即 RotNet。

算法流程：

1. 我们利用 $\hat \Phi(\cdot)$ 创建基于 visual words 的 spatially dense descriptions。
2. 将这些 descriptions 聚合为 BoW representations。
3. 训练模型 $\Phi(\cdot)$ 以重构 BoW，输入为扰动的图像。
4. 注意，训练 $\Phi(\cdot)$ 时，$\hat \Phi(\cdot)$ 保持冻结。
5. 训练了 $\Phi(\cdot)$ 之后，设置 $\hat \Phi(\cdot) \leftarrow\Phi(\cdot)$ 并重复训练过程。

### Building spatially dense discrete descriptions

给定一幅训练图像 $\mathbf{x}$，算法第一步是使用 $\hat \Phi(\cdot)$创建 spatially dense visual words-based description $q(\cdot)$。

设 $\hat \Phi(\mathbf{x})$ 是特征图，通道为 $\hat c$，空间分辨率为 $\hat h \times \hat w$。$\hat \Phi^u(\mathbf{x})$ 是位于位置 $u$ 的特征向量。$U=\hat h \times \hat w$。

为了得到 description $q(\mathbf{x}) = [q^1(\mathbf{x}), ..., q^U(\mathbf{x})])$，我们使用预定义词表 $V=[\mathbf{v}_1, ..., \mathbf{v}_K]$ 对 $\hat \Phi(\mathbf{x})$ 执行密集量化。该词表包含 $\hat c$ 维的 visual word embeddings，$K$ 是词表尺寸。

具体而言，为每个特征向量 $\hat \Phi^u(\mathbf{x})$ 根据最近的欧氏距离分类一个 visual word embedding $q^u(\mathbf{x})$：

<img src="https://i.loli.net/2020/04/20/nSV7EXKhcomHTgA.png" alt="image-20200420144132506" style="zoom:50%;" />

注意，$q^u(\mathbf{x})$ 是一个标量。

词表 $V$ 的学习：在数据集 $X$ 的特征图的集合上，应用 k-means 算法，clusters 为 $K$：

<img src="https://i.loli.net/2020/04/20/38BUWAQ6DcSsgGf.png" alt="image-20200420153412621" style="zoom:50%;" />

其中 visual word embedding $\mathbf{v}_k$ 是 $k$-th cluster 的中心。

### Generating Bag-of-Words representations

得到 discrete description $q(\mathbf{x})$ 后，下一步是创建它的 BoW representation $y(\mathbf{x})$。这是一个 $K$ 维向量，元素 $y^k(\mathbf{x})$ 要么表示 $k-th$ visual word 出现的次数：

<img src="https://i.loli.net/2020/04/20/MQvL2Pzxc5ugieI.png" alt="image-20200420144219450" style="zoom:50%;" />

要么表示 $k$-th visual word 是否在图像中出现：

<img src="https://i.loli.net/2020/04/20/9e6xdLshky2IJ4Q.png" alt="image-20200420154442474" style="zoom:50%;" />

为了将 $y^k(\mathbf{x})$ 转为 visual words 上的概率分布，使用 $L_1$ 正则化：

<img src="https://i.loli.net/2020/04/20/MOgzVDr3djlSIQa.png" alt="image-20200420154610839" style="zoom:50%;" />

因此 $y(\mathbf{x})$ 可以解释为 $K$ 个 visual words 的 soft categorical label。

### Learning to "reconstruct" BoW

基于上述的 BoW representation，我们提出如下自监督任务：给定输入图片 $\mathbf{x}$，执行扰动操作 $g(\cdot)$，得到扰动的图像 $\tilde{\mathbf{x}} = g(\mathbf{x})$，然后训练模型来预测/重构原始图像 $\mathbf{x}$ 的 BoW representation $y(\mathbf{x})$。

我们希望通过特征向量 $\Phi(\tilde{\mathbf{x}}) \in \mathbb{R}^c$ 预测  BoW representation $y(\mathbf{x})$。

为此，我们定义 prediction layer $\Omega(\cdot)$，将 $\Phi(\tilde{\mathbf{x}})$ 作为输入，输出 BoW representatoin 的 $K$ 个 visual words 的 $K$ 维 softmax distribution。具体而言，prediction layer 是通过线性层加 softmax 层实现的：

<img src="https://i.loli.net/2020/04/20/R7OT2m9hIHKXalr.png" alt="image-20200420144337253" style="zoom:50%;" />

#### Self-supervised training objective

损失函数为交叉熵损失：

<img src="https://i.loli.net/2020/04/20/LJkFxOuiZ9hYUKt.png" alt="image-20200420144407297" style="zoom:50%;" />

#### ## 分析

Q：如何保证经过训练的 $\Phi(\cdot)$ 的特征表示，比 $\hat \Phi(\cdot)$ 更好呢？

A：关键在于图像扰动。也就是说，如果没有图像扰动，无法让 $\Phi(\cdot)$ 的特征比 $\hat \Phi(\cdot)$ 更好，而倾向于使 $\Phi(\cdot)$ 与 $\hat \Phi(\cdot)$ 恒等。