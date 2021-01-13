---
title: '[ICCV2019] GradNet: Gradient-Guided Network for Visual Object Tracking'
date: 2020-05-04 15:52:10
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Template Update]
---

## Abstract

现有跟踪算法的问题：孪生跟踪器的模板是固定的，无法捕获目标随时间的变化或 background clutter。

本文的解决方案：提出 gradient-guided network，利用梯度的判别信息，通过前向传播和反向传播操作，更新孪生网络中的模板。

此外，提出 template generalization training method，以更好地利用梯度信息，避免过拟合。

性能：

- https://github.com/LPXTT/GradNet-Tensorflow
- 在四个数据库上进行实验：OTB-2015、TC-128、VOT-2017、LaSOT。
- 速度：80 FPS。

## Introduction

对于孪生跟踪器，有些方法 [16] [45] [40] 提出了更新 template features 的不同机制。

> [16] Qing Guo, Wei Feng, Ce Zhou, Rui Huang, Liang Wan, and Song Wang. **Learning dynamic siamese network for visual object tracking**. In ICCV, 2017.
>
> [45] Zheng Zhu, Wei Wu, Wei Zou, and Junjie Yan. **End-to-end flow correlation tracking with spatial-temporal attention**. In ECCV, 2018.
>
> [40] Tianyu Yang and Antoni B. Chan. **Learning dynamic memory networks for object tracking**. In ECCV, 2018.

然而，这些方法仅专注于组合先前的目标特征，而忽略了 background clutter 中的判别信息。这导致孪生跟踪器与其他在线更新的跟踪器之间存在很大的准确性差距。

通常来说，梯度是通过通过考虑正负候选的最终损失来计算的。因此，梯度包含判别信息以反映目标变化并与 background clutter 区分开。当物体被遮挡或在目标附近存在近似物体时，这些位置处的梯度幅值常常较高。梯度中较高的值可能会迫使模板专注于这些区域并捕获关键的判别性信息。

为了减少迭代次数，极端情况是仅迭代一次，但没有合适的学习率使得仅通过一次迭代就能收敛。即使具有最佳补偿，一次迭代也无法收敛，因为基于常规梯度的优化也无法正确更新模板，因为基于常规梯度的优化是一个非线性过程。

另一方面，我们可以通过 CNN 学习非线性函数，该函数通过探索梯度中的丰富信息来模拟基于梯度的非线性优化。因此我们提出了 gradient-guided network (GradNet) 在目标跟踪中执行  gradient-guided adaptation。GradNet 整合了由两个前向传播和一个后向传播组成的自适应过程，从而简化了基于梯度的优化过程。

训练鲁棒的 GradNet 的任务非常艰巨，原因有两个：

1. 网络倾向于使用模板的表观而不是梯度进行跟踪。因为学习使用梯度比学习使用表观更困难。
2. 网络易于过拟合。

为了解决这些问题，本文提出  template generalization 方法，可以有效探索梯度信息并避免过拟合。

## Related Work

### Model Updating in Tracking

模型更新有三种策略：template combination、gradient-descen based、correlation-based。

#### Template Combination

[16] 提出了 fast transformation learning model，利用先前帧进行有效的在线学习。

[45] 利用光流信息转换模板应根据权重进行整合。

然而，这些方法仅专注于组合先前的目标特征，而忽略了 background clutter 中的判别信息。

#### Gradient-descent based approaches

[36] 训练两个独立的卷积层，使用初始帧回归高斯图，并每隔几帧更新一次这些层。

> [36] Lijun Wang, Wanli Ouyang, Xiaogang Wang, and Huchuan Lu. **Visual tracking with fully convolutional networks**. In ICCV, 2015.

[32] 在初始化和在线更新过程中也使用了多次梯度下降进行迭代。

> [32] Yibing Song, Chao Ma, Lijun Gong, Jiawei Zhang, Rynson W. H. Lau, and Ming-Hsuan Yang. **CREST: convolutional residual learning for visual tracking**. In ICCV, 2017.

这些跟踪器需要进行多次训练迭代才能捕获目标表观的变化。

#### Correlation based Tracking

分类器的训练不能完全由深度网络模拟，因此大多数基于相关性的跟踪器仅利用深度网络来提取鲁棒的特征。

## Proposed Algorithm

![image-20200504170340199](https://i.loli.net/2020/05/04/H7RJunsNT4E9M6Z.png)

GradNet 由两个分支组成，一个分支提取搜索区域的特征，另一个分支分距目标信息和梯度生成模板。

模板生成过程包括 initial embedding、gradient calculation、template updating：

- 将浅层目标特征 $f_2(\mathbf Z)$ 发送到 subnet $\mathbf U_1$ 中，以生成 initial template $\beta$，用于计算 initial loss $L$。
- 浅层目标特征的梯度通过反传计算，并发送到另一个 subnet $\mathbf U_2$ 进行非线性变换以进行更好的梯度表示。
- 转换后的梯度添加到浅层目标特征中，以获得更新的目标表示。

### Basic Tracker

为了提高模板 $\beta$ 的判别能力，本文设计了 update branch $U(\alpha)$ 来探索梯度的丰富信息：

<img src="https://i.loli.net/2020/05/04/pL5PkgSOd8xQ97T.png" alt="image-20200504173116627" style="zoom:50%;" />

其中 $\alpha$ 是 update branch 的参数，不仅能够通过梯度捕获 $\mathbf Z$ 中的模板信息，还能捕获 $\mathbf X$ 中的背景信息。

### Template Generation

#### Initial Embedding

首先得到初始模板：

<img src="https://i.loli.net/2020/05/04/R2jFfAcG6oubvVX.png" alt="image-20200504173600916" style="zoom:50%;" />

然后计算 initial score map $\mathbf S$。

#### Gradient Calculation

计算梯度：

<img src="https://i.loli.net/2020/05/04/x43PqSEBKlow9f7.png" alt="image-20200504173851674" style="zoom:50%;" />

更新的目标特征为：

<img src="https://i.loli.net/2020/05/04/ns9OJp8duG2Z7RU.png" alt="image-20200504173946076" style="zoom:50%;" />

其中，$U_1$ 的梯度是 $U_2$ 的输入，以计算最终损失，因此在 $U_1$ 的训练中引入了  second-order guidance。

#### Template Update

最终的 score map 为：

<img src="https://i.loli.net/2020/05/04/yrVUgdnHwYNxq31.png" alt="image-20200504174332038" style="zoom:50%;" />

这项工作首次利用梯度的判别信息来更新 siamfc 的模板。

###  Template Generalization

#### Problem of Basic Optimization

训练鲁棒的 GradNet 的任务非常艰巨，原因有两个：

1. 网络倾向于使用模板的表观而不是梯度进行跟踪。因为学习使用梯度比学习使用表观更困难。
2. 网络易于过拟合。

为了解决这些问题，本文提出  template generalization 方法，可以有效探索梯度信息并避免过拟合。

#### Template Generalization

我们的目标是迫使 update branch 专注于学习梯度，并避免过拟合。因此我们提出 template generalization method。

我们采用来自不同视频（4个）的搜索区域，以获得通用模板，使得该通用模板在所有搜索区域上表现良好。

与传统方法的主要区别是，利用一个模板（而不是四个模板）来搜索来自不同视频的四个图像上的目标。

该策略强制网络在离线训练期间将注意力集中在梯度上。Subnet $U_1$ 和 $U_2$ 需要根据梯度矫正初始未对齐的模板，从而获得强大的能力来根据梯度更新模板。

## Experiment

### Ablation Analysis

#### Self-comparison

设计了几种变体：

1. Ours w/o M：没有 template generalization 训练过程。
2. Ours w/o MG：没有 template generalization 训练过程和 gradient application。
3. Ours w/o U：没有 template update。
4. Ours w 2U：两次用到的自网络 $U_1$ 不共享参数。
5. Ours-baseline：siamfc。

<img src="https://i.loli.net/2020/05/04/ojSsNGyTH8pd9RV.png" alt="image-20200504191423375" style="zoom:50%;" />

#### Training Analysis

为了进一步分析 template generation，可视化了在两种训练方法下（有/无 template generation）的 initial score map 和 optimal score map。

<img src="https://i.loli.net/2020/05/04/W3hecmKENVT1Dni.png" alt="image-20200504192304218" style="zoom:50%;" />

由 (a) (c) 对比可知，(a) 更嘈杂，而 (c) 直接就在目标位置具有高响应。因此，通过 template generalization 训练的模型在 initial embedding 期间学习了不同的任务，得到了用于检测目标和 background clutter 的通用模板。这种方式为模型提供了更大的判别性梯度。