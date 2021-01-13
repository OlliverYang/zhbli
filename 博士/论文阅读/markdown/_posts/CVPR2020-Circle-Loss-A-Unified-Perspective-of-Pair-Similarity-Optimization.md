---
title: '[CVPR2020] Circle Loss: A Unified Perspective of Pair Similarity Optimization'
date: 2020-04-22 12:52:22
tags: CVPR2020
mathjax: true
---

## Abstract

本文针对深度特征学习提出了两个相似性优化视角，旨在最大化类内相似度 $s_p$ 并最小化类间相似度 $s_n$。

我们发现大多数损失函数，包括 triplet loss 和 softmax+cross-entropy loss，将 $s_n$ 和 $s_p$ 嵌入到 similarity pairs 并减少 $(s_n-s_p)$。这种优化方式是不灵活的，因为对每个相似度得分的惩罚被限制为相等。

我们的直觉是，如果相似性得分距离最优值很远，则应予以强调。为此，我们只需对每个相似度重新加权，以强调未优化的相似度得分。这就是 circle loss，因为决策边界是圆形的。

circle loss 为两种基本的深度特征学习方法构建了统一的公式：

- learning with class-level labels
- learning with pair-wise labels

## Introduction

无论是 triplet loss 还是 softmax+cross-entropy loss，都致力于减少 $(s_n-s_p)$。在 $(s_n-s_p)$ 中，增加 $s_p$ 相当于减少 $s_n$。我们认为这种对称优化方式容易导致以下两个问题：

1. 缺乏优化灵活性。对 $s_n$ 和 $s_p$ 的惩罚力度是相等的，它们的梯度幅度相同。特殊情况下，如 $s_p$ 很小，而 $s_n$ 早已是 0，此时仍然会以大的梯度惩罚 $s_n$。这是低效且不合理的。
2. 收敛状态不明确。优化 $(s_n-s_p)$ 通常导致决策边界 $s_n-s_p = m$，$m$ 是 margin。

我们认为，不同的相似性得分应该具有不同的惩罚力度。如果一个相似性得分远未被优化，应该具有更强的惩罚。反之亦然。因此我们将 $(s_n-s_p)$ 推广为 $(\alpha_n s_n-\alpha_p s_p)$。这导致优化边界是 $(\alpha_n s_n-\alpha_p s_p) = m$，这是在 $(s_n-s_p)$ 空间种的一个圆，因此称作 circle loss。

虽然很简单，circle loss 从本质上重塑了深度特征学习，体现在如下方面：

1. 统一的损失函数：我们为两种基本的学习方法（使用 class-level labels 和 pair-wise labels）提出了统一的损失函数。
2. 灵活的优化：不同的相似性得分具有不同的惩罚力度。
3. 确定的收敛状态：确立了明确的优化目标并有利于可分性。

## A Unified Perspective

在 cosine 相似性度量下，我们希望 $s_p \rightarrow 1$，$s_n \rightarrow 0$。

给定 class-level labels，常用的方法有：L2-Softmax，Large-margin Softmax，Angular Softmax，NormFace，AM-Softmax，CosFace，ArcFace。

给定 pair-wise labels，常用的方法有：constrastive loss，triplet loss，Lifted-Structure loss，N-pair loss，Histogram loss，Angular loss，Margin based loss，Multi-Similarity loss。

给定特征空间的一个样本 $x$，假设有 $K$ 个类内相似度得分和 $L$ 个类间相似度得分，分别定义为 $\{s^i_p\}(i=1,2,...,K)$ 和 $\{s^j_n\}(j=1,2,...,L)$。

为了最小化每个 $s^j_n$ 同时最大化每个 $s^i_p$，我们提出了统一的损失函数：<img src="https://i.loli.net/2020/04/22/Js9CdyA5hfRU8ic.png" alt="image-20200422135329596" style="zoom:50%;" />

该函数通过简单修改就能退化成 triplet loss 或 classification loss。