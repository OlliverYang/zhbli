---
title: '[arXiv2005] Subdomain Adaptation with Manifolds Discrepancy Alignment'
date: 2020-05-09 14:39:00
mathjax: true
---

## Abstract

现有迁移学习算法的问题：减少 domain divergence 是迁移学习的关键步骤。现有工作往往最小化 global domain divergence。但是，两个域可能由几个共享子域组成，并且在每个子域中彼此不同。

本文的解决方案：在迁移时考虑了子域的局部差异。

具体来说，使用低维流形表示子域，并在跨域的每个流形中对齐局部数据分布差异。Manifold Maximum Mean Discrepancy (M3D) 用于测量每个流形中的局部分布差异。

然后，本文提出了一个通用框架，称为 Transfer with Manifolds Discrepancy Alignment (TMDA)，将数据流形的发现与 M3D 的最小化相结合。

该工作是发表在 CIKM2019 上的会议论文 [19] 的扩展。

> [19] P. Wei and Y. Ke, “**Knowledge transfer based on multiple manifolds assumption**,” in Proceedings of the 28th ACM International Conference on Information and Knowledge Management. ACM, 2019, pp. 279–287.

## PROBLEM SETTING

$\mathbf X=[\mathbf X_s,\mathbf X_t]\in \mathbb R^{d\times n}\ (\text n=\text n_s+\text n_t)$，其中 $\mathbf x_i\in\mathbb R^{d\times 1}$，表示数据。

## A GENERAL TRANSFER FRAMEWORK WITH MANIFOLDS DISCREPANCY ALIGNMENT

### A General Framework

为了减少子域差异，关键是发现低维流形。流形发现，或称为流形聚类，是一个被广泛研究的话题。

本文对 spectral clustering-based methods 感兴趣，这种方法探索 $\mathbf X$ 上的 spectral graph $\mathcal G$。通过在 $\mathcal G$ 上应用 ncut 聚类算法，可以获得多个流形。为了将流形发现与局部差异最小发耦合在一起，本文提出了通用框架 TMDA：

<img src="https://i.loli.net/2020/05/09/mlcfiSdWragZyth.png" alt="image-20200509150343813" style="zoom:50%;" />

其中 $\mathcal{MD}$ 是 manifold discovery term，$\hat d'$ 是 manifold discrepancy term，$\mathcal R$ 是正则项，$\phi(\cdot)$ 是要学习的特征映射。