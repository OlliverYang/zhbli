---
title: '[CVPR2020] Deformable Siamese Attention Networks for Visual Object Tracking'
date: 2020-04-16 11:01:31
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Architecture]
---

## Abstract

本文指出，孪生跟踪器存在的问题有：

1. target template 不会在线更新。
2. target template  和 search image 的特征是独立计算的。

本文提出了 SiamAttn（Deformable Siamese Attention Networks），通过引入新的孪生注意力机制，来计算 deformable self-attention 和 cross-attention：

1. self-attention 通过空间注意力学习上下文信息，并使用通道注意力选择性地强调互相依赖的 channel-wise features。
2. cross-attention 能够聚合 target template 和 search image 之间丰富的 contextual interdependencies, 从而隐式地自适应更新 target template。

此外，本文提出了 region refinement module，用于计算 attentional features 之间的逐通道互相关，从而实现更准确的跟踪。

主要实验结果：

1. VOT2016：0.537（SiamRPN++：0.464）。
2. VOT2018：0.470（SiamRPN++：0.415）。

## Introduction

孪生跟踪器中，target template 不会在线更新，导致的问题是：难以准确跟踪具有较大表观变化、剧烈形变或遮挡的目标，增加了跟踪漂移的风险。

孪生跟踪器中，target template  和 search image 的特征是独立计算的，导致的问题是：target features 中的背景上下文信息被完全丢弃了，但这种信息对于区分目标和相邻干扰物或复杂背景具有重要作用。最近的工作 [41] [14] 尝试通过整合先前目标的特征来增强目标表示，但是忽略了来自背景的具有判别力的上下文信息。

> [41] Tianyu Yang and Antoni B. Chan. Learning dynamic memory networks for object tracking. In ECCV, 2018.
>
> [14] Qing Guo, Wei Feng, Ce Zhou, Rui Huang, Liang Wan, and Song Wang. Learning dynamic siamese network for visual object tracking. In ICCV, 2017.

本文引入了新的孪生注意力机制，通过计算孪生网络中的 cross-attention，将丰富的背景上下文编码到目标表示中。

最近，注意力机制被引入到跟踪任务中，然而在这些方法中，target template/search image 的注意力和深层特征被分别计算，这限制了孪生架构的潜在性能。

本文提出了 Deformable Siamese Attention Networks（SiamAttn），来提高孪生跟踪器的特征学习能力。

## Deformable Siamese Attention Networks

![image-20200416115716119](https://i.loli.net/2020/04/16/jhH4l5pL2yUoT1k.png)

本文提出的跟踪器包括三个组件：

1. deformable Siamese attention (DSA) module
2. Siamese region proposal networks (Siamese RPN)
3. region refinement module

### Deformable Siamese Attention Module

![image-20200416115958941](https://i.loli.net/2020/04/16/9l6hwUdYpFKkq3P.png)

DSA 模块的输入与输出：

- 输入——由孪生网络计算的一对卷积特征
- 输出——由孪生注意力机制调制的特征

DSA 模块包括两个组件：

1. self-attention 子模块
2. cross-attention 子模块

#### Self-Attention

self-attention 包含两个方面：

1. 通道 attention
2. 空间 attention

如 [24] 所示，高级卷积特征的每个 channel map 通常针对特定的目标类别产生响应。均等对待所有通道的特征将妨碍表示能力。类似地，受感受野的限制，特征图的每个位置只能感受局部空间信息。因此，从整幅图像中学习全局上下文至关重要。

> [24] Bo Li, Wei Wu, Qiang Wang, Fangyi Zhang, Junliang Xing, and Junjie Yan. Siamrpn++: Evolution of siamese visual tracking with very deep networks. In CVPR, 2019.

具体而言，自注意力（包括通道/空间自注意力）分别在 target branch 和 search branch 上计算。

以空间注意力为例，计算流程为：

1. 输入特征：$\mathbf{\text{X}} \in \mathbb{R}^{C \times H \times W}$。

2. 在 $\mathbf{\text{X}}$ 上应用 $1 \times 1$ 卷积，得到 query features $\mathbf{\text{Q}} \in \mathbb{R}^{C' \times H \times W}, C' = \frac{1}{8}C$。

3. 在 $\mathbf{\text{X}}$ 上应用 $1 \times 1$ 卷积，得到 key features $\mathbf{\text{K}} \in \mathbb{R}^{C' \times H \times W}$。

4. 对 $\mathbf{\text{Q}}$ 进行 reshape，得到 $\bar{\mathbf{\text{Q}}} \in \mathbb{R}^{C' \times N}, N = H \times W$。

5. 对 $\mathbf{\text{K}}$ 进行 reshape，得到 $\bar{\mathbf{\text{K}}} \in \mathbb{R}^{C' \times N}$。

6. 通过矩阵乘法和 column-wise softmax 得到 spatial self-attention map $\mathbf{A_s^s} \in \mathbb{R}^{N\times N}$：
   $$
   \mathbf{A_s^s} = \text{softmax}_{col}(\bar{\mathbf{\text{Q}}}^T\bar{\mathbf{\text{K}}})  \in \mathbb{R}^{N\times N}
   $$

7. 在 $\mathbf{\text{X}}$ 上应用 $1 \times 1$ 卷积和 reshape 操作，得到 value features $\bar{\mathbf{\text{V}}} \in \mathbb{R}^{C \times N}$。

8. 在 $\mathbf{\text{X}}$ 上应用 reshape 操作，得到 $\bar{\mathbf{\text{X}}} \in \mathbb{R}^{C \times N}$。

9. 得到 $\bar{\mathbf{X}}_s^s \in \mathbb{R}^{C \times N}$：
   $$
   \bar{\mathbf{\text{X}_s^s}} = \alpha \bar{\mathbf{\text{V}}}\mathbf{\text{A}_s^s} + \bar{\mathbf{\text{X}}} \in \mathbb{R}^{C \times N}
   $$
   其中 $\alpha$ 是标量参数。
   
10. 对 $\bar{\mathbf{X}}_s^s$ 进行 reshape 操作，得到 $\mathbf{\text{X}_s^s} \in \mathbb{R}^{C \times H \times W}$。

同理可计算通道自注意力 $\mathbf{\text{A}_c^s}$ 和 channel-wise attentional features $\mathbf{\text{X}_c^s}$. 注意计算时不进行 $1\times 1$ 卷积。将空间注意力特征和通道注意力特征逐元素相加的到最终的自注意力特征 $\mathbf{\text{X}^s}$。

#### Cross-Attention

孪生网络通常在最后一层进行预测，而来自两个分支的特征是分别计算的，但彼此的特征可能会互相补偿。跟踪时通常会出现多个目标，甚至在跟踪过程中可能出现遮挡。因此，让 search branch 学习目标信息非常重要，这使 search branch 能够生成更具辨别性的表示，有助于更准确地识别目标。同时对于 target branch 而言，当对来自 search image 的上下文信息进行编码时，目标表示可能更有意义。为此，我们提出了一个 cross-attention 子模块，从两个孪生分支学习这种互信息，使两个分支可以更加协同地工作。

以 search branch 为例，计算流程为：

1. 定义模板特征为 $\mathbf{Z} \in \mathbb{R}^{C \times h \times w}$，搜索特征为 $\mathbf{X} \in \mathbb{R}^{C \times H \times C}$。

2. 对模板特征进行 reshape 操作，得到 $\bar{\mathbf{Z}} \in \mathbb{R}^{C \times n}, n = h \times w$。

3. 从 target branch 计算 cross-attention：
   $$
   \mathbf{A}^{\text{c}} = \text{softmax}_{row}(\bar{\mathbf{Z}}\bar{\mathbf{Z}}^T) \in \mathbb{R}^{C\times C}
   $$

4. 将来自 target branch 的 cross-attention 编码到 search features 中：
   $$
   \bar{\mathbf{\text{X}}}^\mathbf{c} = \gamma \mathbf{\text{A}^c}\bar{\mathbf{\text{X}}} + \bar{\mathbf{\text{X}}} \in \mathbb{R}^{C \times N}
   $$
   
   其中 $\gamma$ 是标量参数。
   
5. 对 $\bar{\mathbf{\text{X}}}^\mathbf{c}$ 应用 reshape 操作，得到输出 cross-attentional features $\mathbf{\text{X}}^\mathbf{c} \in \mathbb{R}^{C\times H\times W}$。

6. 将自注意力特征和 cross-attentional 特征逐元素相加得到搜索图像的 attentional features。

同理可计算 target image 的注意力特征。

#### Deformable Attention

将  $3\times 3$ 可变形卷积进一步应用于计算出的注意力特征，从而生成最终的注意力特征。

#### Region Proposals

按照[24]，我们对从最后三个阶段计算出的 siamese features 应用三个 siamese RPN 块，生成三个 prediction maps，并通过加权和进行组合。Combined maps 的每个空间位置会预测一组 region proposals，将具有最高分类得分的 predicted proposal 选择为跟踪框。

### Region Refinement Module

该模块用于进一步提高预测的目标区域的定位精度。流程为：

1. 在每个 stage 中，对两个 attentional features 执行逐通道互相关，得到多个 correlation maps。
2. correlation maps 送入一个 fusion block，通过使用上/下采样与 $1\times 1$ 卷积，把不同特征图调整到相同尺寸。
3. 将对齐的特征使用逐元素相加进行融合。
4. 利用 RPN 阶段预测的跟踪框（注意仅此一个框），进行池化，再预测目标的边框和 mask。

在此基础上增加了两个额外操作：

1. 预测 mask 时，将前两阶段特征与 fused features 结合，用于编码细节信息。
2. 采用 deformable RoI pooling 使得预测更准确。

边框回归和 mask 预测需要不同级别的卷积信息，因此使用空间分辨率为 $64 \times 64$ 的特征预测 mask，使用 空间分辨率为 $25\times 25$ 的特征回归边框。

注意，该模块并没有预测分类任务。与 ATOM 和 SiamMask 等密集预测边框和 mask 的方法相比，该模块是轻量化的，仅为 1 个区域预测边框和 mask，计算更高效。