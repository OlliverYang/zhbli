---
title: '[CVPR2020] D3S – A Discriminative Single Shot Segmentation Tracker'
date: 2020-05-11 19:05:52
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Segmentation]
---

## Discriminative segmentation network

https://github.com/alanlukezic/d3s

<img src="https://i.loli.net/2020/05/11/a7XFcudUSVCEQMl.png" alt="image-20200511200403334" style="zoom:50%;" />

### Geometrically invariant model pathway

本文的 geometrically invariant model (GIM) 由两组特征向量组成，分别表示目标和背景：$\mathbf X_{\text{GIM}}=\{\mathbf X^F,\mathbf X^B\}$。

将 backbone 的特征送入 $1\times 1$ 卷积，将维数降为 64，然后再进行 $3\times 3$ 卷积。在网络训练时调整这两个层，以产生用于分割的最佳特征。

在第一帧中的目标/背景对应的空间位置上提取 segmentation feature vectors，以创建 target/background models。

跟踪期间，将搜索区域的 pixel-level features 与 $\mathbf X_{\text{GIM}}$ 进行比较，用于计算 foreground/background similarity channels $\mathbf {F/B}$。

具体而言，为了计算 $\mathbf F$，在像素 $i$ 处提取的特征 $\mathbf y_i$ 通过计算 normalized dot product 与特征 $\mathbf x^F_j\in \mathbf X^F$ 进行比较：

<img src="https://i.loli.net/2020/05/11/bDywk3gI1Ua46hm.png" alt="image-20200511192825639" style="zoom:50%;" />

像素 $i$ 的 foreground similarity $\mathbf F_i$ 通过计算该像素的 topk 相似性的均值来计算：

<img src="https://i.loli.net/2020/05/11/4J6fcLosIHXkjAF.png" alt="image-20200511193410723" style="zoom:50%;" />

同理，可计算 $\mathbf B$。

对 $\mathbf F$ 和 $\mathbf B$ 进行 softmax 以获得 target posterior channel $\mathbf P$。

### Geometrically constrained model pathway

尽管 GIM 很好地将目标和背景分离开，但无法区分近似目标。

因此，我们在 geometrically constrained Euclidean model (GEM) pathway 中使用了 ATOM 提出的 DCF。

具体而言，backbone features 通过 $1\times 1$ 卷积降至 64 维，降维后的特征与 64 channel DCF 进行相关。Redcution layer 和 DCF 通过 backprop 进行训练。

Correlation response 的最大值被认为是目标位置。然而分割需要在每个像素位置输出目标置信度。因此以如下方式得到 target location channel：计算从 correlation map 中的最大值位置到搜索区域中其余像素位置的欧氏距离。

## Experiments

### Implementation details

仅需使用 Youtube-VOS 进行训练。在单卡上训练 20 小时。