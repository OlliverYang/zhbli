---
title: >-
  [AAAI2020] Discriminative and Robust Online Learning for Siamese Visual
  Tracking
date: 2020-04-24 12:45:57
tags:
- AAAI2020
- Tracking
categories: 
- [Tracking, Template Update]
- [Tracking, Model Update]
mathjax: true
---

## Abstract

（待开源）https://github.com/shallowtoil/DROL

现有跟踪算法的问题：

- 对于 online-only 方法，学习的模型缺乏通用性，因此在目标回归方面性能较差。
- 对于 offline-only 方法，缺乏特定目标的上下文信息，因此难以区分相似物体，且对形变不够鲁棒。

本文的解决方案：

- 为离线训练的孪生网络设计基于注意力机制的 online module。
- 提出**滤波器更新**机制，用于抑制背景噪声。
- 提出**模板更新**策略，用于处理目标形变以提高鲁棒性。

## Introduction

跟踪器可分为判别式跟踪器和生成式跟踪器：

- 判别式跟踪器训练一个分类器来区分目标和背景。
- 生成式跟踪器通过计算目标和 search candidates 之间的联合概率密度来找到最佳匹配。

孪生网络的缺点：

1. 忽视背景信息，易受 distractors 影响。
2. 仅依赖第一帧进行作为模板，或仅仅依靠求平均来进行模板更新。

本文引入在线机制，该机制参考了 discriminative trackers，这些跟踪器通常具有判别性强的分类器和有效的在线更新策略。然而，直接在线更新孪生网络可能会引入噪声，从而破坏离线训练的特征。

基于以上分析，本文提出于孪生网络互补的 online subnet。该 online subnet 基于注意力机制设计，用于提取最有代表性的目标特征，并可以进行高效优化。在线模块的相应图分别用于前面提到的两个问题：

1. 通过融合 online response map 和 siamese classification score，可以解决问题 1。
2. 将高质量的帧用于模板更新，可以解决问题 2。

##  Proposed Method

<img src="https://i.loli.net/2020/04/24/EgpP8salzdIxrwm.png" alt="image-20200424134131312"  />

<img src="https://i.loli.net/2020/04/24/6dep8hbRV1a2BiN.png" alt="image-20200424132325992" style="zoom:50%;" />

> 本文提出的 online module 的结构。包括三部分：
>
> 1. compression module：仅在第一帧优化。
> 2. attention module：仅在第一帧优化。
> 3. filter module：在后续帧优化。

### Siamese Matching Subnet

设孪生网络的 embeddinig space 为 $\phi(\cdot)$，通过如下方式计算分类得分：

<img src="https://i.loli.net/2020/04/24/7EBwgfkNTo2G1bv.png" alt="image-20200424134452380" style="zoom:50%;" />

### Target-specific Features

我们提出以有监督的方式，利用 L2 损失，在孪生特征之上生成 target-specific features（公式 4）：

<img src="https://i.loli.net/2020/04/24/l4t5gGPqa37HEUN.png" alt="image-20200424131325052" style="zoom:50%;" />

其中 $f_C$ 是 expected output，表示每个位置的分类得分，$y_1$ 是给定目标边框的高斯。

受 [Li et al. 2019b] [Yang et al. 2019] 的启发，拟合所有背景像素会主导在线学习，因为只有少数卷积滤波器对构建目标表示是重要的。

> [Li et al. 2019b] Li, X.; Ma, C.; Wu, B.; He, Z.; and Yang, M.-H. 2019b. **Target-aware deep tracking**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, 1369–1378.
>
> [Yang et al. 2019] Yang, K.; Song, H.; Zhang, K.; and Liu, Q. 2019. **Hierarchical attentive siamese network for realtime visual tracking**. Neural Computing and Applications 1–12.

因此我们提出空间注意力和通道注意力来选择重要特征。

### Discriminative Learning via Filter Update

通过将公式 4 中的 $y_1$ 变成 $y_i$，可以在跟踪过程中一直优化 filter module。与 [Danelljan et al. 2019] 相同，采用共轭梯度下降以加快收敛速度。

> [Danelljan et al. 2019] Danelljan, M.; Bhat, G.; Khan, F. S.; and Felsberg, M. 2019. Atom: Accurate tracking by overlap maximization. In The IEEE Conference on Computer Vision and Pattern Recognition (CVPR).

使用 filter module 得到的 online classification score 与 siamese classification score 融合，得到 adaptive classification score：

<img src="https://i.loli.net/2020/04/24/tMkCFn9EgOPjHUi.png" alt="image-20200424132710818" style="zoom:50%;" />

### Robust Learning via Template Update

我们在孪生网络上设计了一个额外的 template branch，用于保留最近帧的目标信息。注意，取得良好性能的关键取决于模板质量。我们通过 online classifier 输出的最大得分来判断模板质量：

<img src="https://i.loli.net/2020/04/24/uNOUzgjyKedpc8S.png" alt="image-20200424133235601" style="zoom:50%;" />

通过如下方式选择模板：

<img src="https://i.loli.net/2020/04/24/gKu6GoecFkVZsyB.png" alt="image-20200424133353166" style="zoom:50%;" />

其中，$\hat f^{cls}_M$ 表示最大得分的位置，$\hat f^{reg}_M$ 表示对应的边框。当两个模板预测的边框相似，但分类得分差距大时，使用新的模板。