---
title: '[ICCV2019] Graph Convolutional Tracking'
date: 2020-05-02 16:15:13
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Architecture]
---

##  Graph Convolutional Tracking

<img src="https://i.loli.net/2020/05/13/wOBJ7QAbomSsq3x.png" alt="image-20200513183345624" style="zoom:50%;" />

定义 $z$ 为尺寸是 $127\times 127$ 的 exemplar image，$x$ 为尺寸是 $255\times 255$ 的 search image。本文将 graph convolutional transformation 和孪生跟踪器结合到一起：

<img src="https://i.loli.net/2020/05/02/DxowNZF1dGCHVJ3.png" alt="image-20200502161844838" style="zoom:50%;" />

本文将 $\psi_{GCN}$ 分解为：

- Spatial-Temporal GCN (ST-GCN) $\psi_1$
- ConText GCN (CT-GCN) $\psi_2$

可得：

<img src="https://i.loli.net/2020/05/02/rLUEOPdyAZgQRYa.png" alt="image-20200502162452244" style="zoom:50%;" />

### Preliminary: Graph Convolutional Networks

设图有 $M$ 个节点，adjacency matrix 为 $\mathbf A\in \mathbb {R}^{M\times M}$，degree matrix 为 $\mathbf \Lambda_{ii}=\sum_j \mathbf A_{ij}$。图卷积的线性变化指 graph signal $\mathbf X\in\mathbb R^{D\times M}$ 与 filter $\mathbf W\in \mathbb R^{D\times C}$ 相乘：

<img src="https://i.loli.net/2020/05/02/Gy5worNVpHvQAlR.png" alt="image-20200502163142599" style="zoom:50%;" />

其中 $\mathbf X_{i\cdot}\in \mathbb{R}^D$ 是第 $i$ 个节点的特征表示。$\hat{\mathbf A} = \mathbf A + \mathbf I$。 $\hat{\mathbf \Lambda}_{ii}=\sum_j \hat{\mathbf A}_{ij}$。

输出是尺寸为 $C\times M$ 的矩阵 $\mathbf V$。

补充：图卷积的输出和输出，节点数不变，都是 $M$。

### Target Appearance Modeling via ST-GCN

设 exemplar images 的 embeddings 为 $\{\mathbf Z_i\}_{i=t-1}^{t-T}$，其中 $\mathbf Z_i\in \mathbb R^{D_1\times M_z}$，$D_1$ 表示特征维度，$M_z$ 表示 parts 的数量。我们将特征图 $\mathbf Z_i$ 中每个 $D_1\times 1\times 1$ 的向量看作一个 target part。

构造无向图 $\mathcal{G_1=(V_1,E_1)}$。

节点集合 $\mathcal V_1 = \{v_{ij}|i=t-1,...,t-T,j=1,...,M_z\}$。

包括两种形式的边：

1. Spatial edges $\mathcal E^S_1$ 表示每帧中的 intra-exemplar connection：$\mathcal E_1^S = \{v_{ij}v_{ik}|1 \le j,k\le M_z,j \ne k\}$。这是全连通图。
2.  Temporal edges $\mathcal E_1^T = \{v_{ij}v_{i+1,j}\}$：相邻帧中，连接同一位置的 parts。 

ST-GCN 为：

<img src="https://i.loli.net/2020/05/02/jtn2TOPv9dJBoD7.png" alt="image-20200502164050191" style="zoom:50%;" />

其中，$\hat{\mathbf{Z}}_i\in \mathbb R^{D_2\times M_z}$，$\mathbf{V}_1\in \mathbb R^{D_2\times M_z}$。

### Target Feature Adaption via CT-GCN

作用：整合当前搜索图像的上下文信息。

得到 搜索图像的特征 $\mathbf X_t\in \mathbb R^{D_1\times M_x}$ 后，为了获得全局信息，对其进行卷积后全局池化得到向量 $\mathbf x_t$，再做反卷积得到 $\hat{\mathbf X}_t$，与 $\mathbf{V}_1$ 尺寸相同，并通过逐元素相加融合两者：

<img src="https://i.loli.net/2020/05/02/z4GvTpXyadiOmeN.png" alt="image-20200502181142152" style="zoom:50%;" />

邻接矩阵为：

<img src="https://i.loli.net/2020/05/02/dbrjkyXocBUVwRQ.png" alt="image-20200502181249012" style="zoom:50%;" />