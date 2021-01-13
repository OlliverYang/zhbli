---
title: '[CVPR2020] A Transductive Approach for Video Object Segmentation'
date: 2020-04-16 16:24:17
tags:
- CVPR2020
- Video Object Segmentation
mathjax: true
---

## Abstract

现有半监督视频分割方法的缺点：使用在其他领域（如光流和实例分割）训练的额外模块的信息进行视频目标分割，因此这些方法无法与其他方法在同一个公平的基础上进行比较。

本文的解决方案：提出了简单而强大的 transductive method，不需要额外的模块，数据集和复杂的结构设计。

本文采用标签传播方法，像素标签根据嵌入空间的特征相似性向前传递。与其他的传播方法不同，我们以整体方式传播时间信息，这考虑了长时间的目标表观。

性能：

- 本文的方法需要很少的额外计算，速度约为 37 FPS。
- 使用 vanilla ResNet50 的单一模型在 DAVIS2017 验证集上的 $\mathcal{J}$&$\mathcal{F}$ 得分为 72.3%，测试集上的 $\mathcal{J}$&$\mathcal{F}$ 得分为 63.1%。
- 代码：https://github.com/microsoft/transductive-vos.pytorch

## Introduction

由于光流、跟踪、实例分割、ReID 等任务与视频目标分割任务具有相似点，先前的工作 [29] [30] 尝试将为这些任务训练的模块转移到视频目标分割算法中：

- 光流和跟踪通过估计附近帧中的位移来捕获  local dependencies 。
- 实例分割和 ReID 通过学习对剧烈表观变化的不变性来捕获 global dependencies 。

> [29] X. Li and C. Change Loy. Video object segmentation with joint re-identification and attention-aware mask propagation. In Proceedings of the European Conference on Computer Vision (ECCV), pages 90–105, 2018.
>
> [30] J. Luiten, P. Voigtlaender, and B. Leibe. Premvos: Proposalgeneration, refinement and merging for video object segmentation. arXiv preprint arXiv:1807.09190, 2018.

捕获 local 和 global dependencies 一直是半监督学习的中心课题，这又被称作 transductive inference。其基本假设是：

1. 附近的样本往往具有相同的标签。
2. 位于同一流形的样本应该具有相同标签。

Local 和 global dependencies 描述了足够平滑的亲和分布，因此能够可靠地估计无标签数据的标签传播。这启发我们探索半监督视频目标分割的统一方法，无需整合其他领域的模块：

- 通过空间先验和运动先验来建模 local dependency。它基于这样的假设：空间上邻近的像素可能具有相同的标签，而时间间隔较远的帧会削弱这种空间连续性。
- 通过在训练集上学习的视觉表观建模 global dependency。

该推论遵循正则化框架，该框架在构造的时空依赖图中传播标签。尽管最近的在最近的视频目标算法中被使用，但他们学习和传播亲和力的方式是稀疏和局部的，即，要么在相邻帧之间，要么在第一帧与较远帧之间学习像 pixel affinities。我们观察到在 temporal volume 中存在很多平滑的无标签结构未被充分利用，这可能导致处理形变和遮挡时失败。相比之下，我们的标签传播方法尝试捕获从第一帧到当前帧之前的整个视频序列的所有帧。为了限制计算开销，我们在较近的历史中密集采样，而在较远的历史中稀疏采样，使得我们的模型考虑目标表观变化的同时减少了时间冗余。

我们的模型不依赖任何其他模块、数据集，也不依赖基于在 ImageNet 上预训练的 ResNet50 的复杂架构。测试时，逐帧预测仅涉及基本网络的前馈以及与预测历史的内积。因此，推理速度很快，并且不受目标数量的影响。

## Approach

与先前在单个注释帧上微调模型或从其他相关任务中转移知识的工作相反，我们的方法着重于充分利用视频序列中未标记的结构，从而构建一个简单、强大、快速的模型。我们首先描述通用半监督分类框架，再将其应用到在线视频目标分割。

### A Transductive Inference Framework

考虑通用半监督分类问题，设有数据集 $\mathcal{D} = \{(x_1,y_1), (x_2, y_2), (x_l, y_l), x_{l+1}, ..., x_n\}$，具有 $l$ 个已标记的数据对，和 $n-l$ 个未标记的数据点。任务是基于观测 $\mathcal{D}$ 为无标签数据 $\{x_{l+1}, ..., x_n\}$ 推断标签 $\{\hat y_i\}_{i=l+1}^n$。无标签数据的推断在以前的工作中被形式化为 transductive regularization 框架：

<img src="https://i.loli.net/2020/04/16/wPLlhgM12XmHfYK.png" alt="image-20200416175436284" style="zoom:33%;" />

其中 $w_{ij}$ 编码了数据点 $(x_i, x_j)$ 的相似性，$d_i$ 表示像素 $i$ 的 degree：$d_i = \sum_j w_{ij}$。第一项是平滑约束，强制相似的点具有相同标签。第二项是 fitting 约束，偏离初始观测的解。参数 $\mu$ 平衡两项。半监督分类解决如下优化问题：

<img src="https://i.loli.net/2020/04/17/ZgQ6Spsyw8C2VhE.png" alt="image-20200416175527352" style="zoom:33%;" />

上述能量最小化问题可以被迭代求解（公式3）：

<img src="https://i.loli.net/2020/04/16/buBA2EyGKk3hcVm.png" alt="image-20200416181008060" style="zoom:43%;" />

其中 $\mathbf{S} = \mathbf{D}^{-1/2}\mathbf{W}\mathbf{D}^{-1/2}$ 是由 $w_{ij}$ 构建的归一化相似性矩阵。$\alpha = \mu/(\mu+1)$，$\mathbf{y}(0) = [y_1, y_2, ..., y_n]^T$ 是标签的初始观测，clamped with 有监督的标签。$\alpha$ 常为 0.99。这一 transduction 模型来自于 globalized model 上，而 globalized model 建立在无监督数据的密集结构上。

### Online Video Object Segmentation

基于上述框架，为半监督视频目标分割建立 transductive model，负责 dense long-range interaction。

这带来了三个挑战：

1. 模型必须以在线方式工作，即不能依赖未来帧推断当前帧。
2. 视频中的像素数可达数千万，难以计算所有像素的相似性矩阵。
3. 需要学习像素间有效的相似性表示 $W$.

为了使算法在线运行，假定当运行到 $t$ 帧时，已经确定了所有先前帧的预测。因此通过时间来扩展推断过程，从而近似公式3，得到公式4：

<img src="https://i.loli.net/2020/04/17/PouckI592LRhBTi.png" alt="image-20200417132705360" style="zoom: 41%;" />

$\mathbf{S}_{1:t \rightarrow t+1}$ 表示在从第一帧到第 $t$ 帧的像素，和第 $t+1$ 帧像素之间构建相似性矩阵。由于除了第一帧外没有标签，因此先验项 $\mathbf{y}(0)$ 被忽略。

对于第 $t+1$ 帧，上述传播过程等价于最小化一组 spatio-temporal volume 的平滑项：

<img src="https://i.loli.net/2020/04/17/PLC7wFtRyUY1pm4.png" alt="image-20200417133432383" style="zoom:41%;" />

$i$ 为 $t+1$ 帧中的像素下标，$j$ 为从第一帧到第 $t$ 帧的像素下标。

###  Label Propagation

给定第一帧标签，利用公式4将标签传播到每一帧。视频目标割的质量在很大程度上取决于相似度 $\mathbf{S}$，其核心是相似度矩阵 $\mathbf{W}$。

#### Similarity metric

为了构建平滑的 classification function，相似性度量应考虑全局高级语义和局部低级空间连续性。我们的相似性度量 $w_{ij}$ 包含表观项和空间项：

<img src="https://i.loli.net/2020/04/17/WOdYctQXn6wRpNJ.png" alt="image-20200417134039782" style="zoom:41%;" />

$f_i, f_j$ 是像素 $p_i, p_j$ 的特征嵌入，由卷积网络计算。$\text{loc}(i)$ 是像素 $i$ 的空间位置。

#### Frame sampling

由于长视频可能有数百帧，在所有先前帧计算相似度矩阵 $S$ 是不可行的。因此通过观察视频中的时间冗余对少数帧进行采样——在前 40 帧中采样 9 帧：

1. 采样目标帧之前的连续 4 帧，对局部运动进行建模。
2. 从其余 36 帧中稀疏采样 5 帧进行长期建模。

#### A simple motion prior

在时域中较远的像素具有较弱的空间依赖性。因此在参考帧在局部密集采样时，使用较小的 $\sigma = 8$，在参考帧较远时使用较大的 $\sigma = 21$。这一简单的运动模型对于发现长期依赖是有效的。

### Learning the appearance embedding

使用数据驱动的方式在 2D 卷积网络中学习表观嵌入。表观嵌入旨在捕获由于运动，缩放和变形而引起的短期和长期变化。训练视频中每帧都标注了目标的分割和 identity。

对于每个 target pixel $x_i$，考虑先前帧的所有像素作为 references。定义像素 $x_i$ 的特征嵌入是 $f_i$，参考像素 $x_j$ 的特征嵌入是 $f_j$，那么 $x_i$ 的预测标签 $\hat{y_i}$ 为：

<img src="https://i.loli.net/2020/04/17/d8Etjs79BRXohYg.png" alt="image-20200417135918319" style="zoom:41%;" />

通过对目标帧中所有像素计算标准交叉熵损失来优化特征嵌入：

<img src="https://i.loli.net/2020/04/17/chFNUmrfHnLJzMZ.png" alt="image-20200417135930405" style="zoom:41%;" />

## Results

<img src="https://i.loli.net/2020/04/17/mydOXQAtrkWPo2u.png" alt="image-20200417141416449" style="zoom:41%;" />