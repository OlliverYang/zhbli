---
title: '[ICCV2019] Learning the Model Update for Siamese Trackers'
date: 2020-04-18 12:43:54
tags:
- ICCV2019
- Tracking
mathjax: true
categories:
- [Tracking, Model Update]
---

## Abstract

现有算法的问题：孪生跟踪器中，当前帧模板与先前帧累积的模板线性组合，导致信息随时间指数衰减。尽管这种方式可以改善跟踪结果，但其简单性限制了潜在性能。

本文的解决方案：通过学习如何更新来代替手工设计的更新方法。提出 UpdateNet：

- 结构：卷积网络，易于集成到现有孪生跟踪器中。
- 输入：
  - 初始模板
  - 累积模板
  - 当前模板
- 输出：
  - 针对下一帧的最优模板，即新的累积模板。

性能：

- https://github.com/zhanglichao/updatenet
- ~50 FPS
- baseline：DaSiamRPN
- VOT2016_EAO：0.439 $\rightarrow$ 0.481
- VOT2018_EAO：0.383 $\rightarrow$ 0.393
- LaSOT_Precision：0.538 $\rightarrow$ 0.560
- TrackingNet_Precision：59.1 $\rightarrow$ 62.5

## Introduction

传统孪生跟踪器

- 方案：模板通过第一帧初始化，并在跟踪中保持固定。
- 缺点：难以适应物体的表观变化。

线性更新模板的跟踪器

- 假定表观变化率恒定。
- 缺点：
  - 实际上，模板的更新因跟踪条件的不同而有很大差异，这取决于外部因素（例如运动，模糊或背景混乱）的复杂组合。因此，简单的线性更新难以应对不断变化的更新需求，也不足以概括所有可能遇到的情况。
  - 此外，这种更新方式在所有空间维度上也是恒定的，这不允许 localized partial updates。这在部分遮挡等情况下尤其有害，在这种情况下，仅模板的特定部分需要更新。
  - 最后，过度依赖初始模板可能会遭受灾难性的漂移以及无法从跟踪失败中恢复过来。

本文的 UpdateNet

- 方案：学习模板更新。学习的更新策略利用目标和图像信息，因此可以适应每种具体情况。
- 新的累积模板包含目标当前表观有效的 historical summary，因为它会使用最新信息不断更新，同时利用初始目标表观信息保证鲁棒性。

## Related work

线性更新导致模板更集中于最近的帧而忘记历史表观。

为了解决这一问题，[10] [11] 提出在计算相关滤波器时，选择历史帧的子集作为训练样本。然而将多个样本保存起来导致内存和计算量增加。

> [10] Martin Danelljan, Gustav Hager, Fahad Shahbaz Khan, and Michael Felsberg. Adaptive decontamination of the training set: A unified formulation for discriminative visual tracking. In CVPR, 2016. 2
> [11] Martin Danelljan, Andreas Robinson, Fahad Shahbaz Khan, and Michael Felsberg. Beyond correlation filters: Learning continuous convolution operators for visual tracking. In ECCV, 2016.

ECO [7] 试图将训练样本的分布建模为混合高斯模型来缓解此问题，每个分量表示一个独特的表观。

> [7] Martin Danelljan, Goutam Bhat, F Shahbaz Khan, and Michael Felsberg. Eco: efficient convolution operators for tracking. In CVPR, 2017.

[45] 采用长短期记忆（LSTM）通过在线跟踪过程中将先前的模板存储在存储器中来估计当前模板，然而计算量过高且算法复杂。

> [45] Tianyu Yang and Antoni B Chan. Learning dynamic memory networks for object tracking. In ECCV, 2018.

[6] 也使用模板存储器，但是使用强化学习来选择存储的模板之一。但此方法无法从多个帧中累积信息。 

> [6] Janghoon Choi, Junseok Kwon, and Kyoung Mu Lee. Visual tracking by reinforced decision making. CoRR, abs/1702.06291, 2017.

[33] 的元跟踪器通过预训练的方法对第一帧中目标的模型进行更好的初始化，但仍需要在线跟踪中进行线性更新。

> [33] Eunbyung Park and Alexander C Berg. Meta-tracker: Fast and robust online adaptation for visual object trackers. In ECCV, 2018.

[46] 建议离线使用 SGD 学习 CF 跟踪器的更新系数。然而相关滤波器的求解是手工设计的，并且这些系数是固定的，在跟踪过程中不会更新。

> [46] Yingjie Yao, Xiaohe Wu, Lei Zhang, Shiguang Shan, and Wangmeng Zuo. Joint representation and truncated inference learning for correlation filter based tracking. In ECCV, 2018.

[15] 提出通过傅立叶域中的正则化线性回归来计算相对于初始模板的变换矩阵，从而为了适应物体的表观变化。由于在估计变换时仅考虑初始模板，因此该方法忽略了在跟踪过程中观察到的历史表观变化，这可能对更平滑地适配 exemplar template 非常重要。此外，他们将变换矩阵计算为傅立叶域上的形式解，这会遇到与边界效应有关的问题。

> [15] Qing Guo, Wei Feng, Ce Zhou, Rui Huang, Liang Wan, and Song Wang. Learning dynamic siamese network for visual object tracking. In ICCV, 2017.

我们的工作使用功能强大但易于训练的模型来更新对象模板，不仅基于第一帧，而且还使用观察到的训练数据，基于所有先前帧的累积模板，来更新目标模板。此外，我们的 UpdateNet 经过训练，可以根据观察到的训练跟踪数据学习如何有效地更新目标模板。

## Updating the object template

![image-20200418124944188](https://i.loli.net/2020/04/18/Y9eCiK2UqtDR6Tc.png)

### Standard update

模板通过 running average 进行更新，权重随时间指数下降：

<img src="https://i.loli.net/2020/04/18/ASBsKw6fMruzYUq.png" alt="image-20200418124720492" style="zoom:50%;" />

$i$：frame index。

$T_i$：使用当前帧计算的模板。

$\widetilde{T}_i$：accumulated template。

$\gamma$：update rate，常固定为 0.01。

该方法具有 4 个局限性：

1. 不同情况下更新的需求是不同的。
2. 在空间维度的更新是恒定的。
3. 无法访问初始表观，导致无法从漂移中恢复。
4. 过于简单。

### Learning to update

通过学习 generic function $\phi$ 来更新模板：

<img src="https://i.loli.net/2020/04/18/6eVvYgZwRT1IPaK.png" alt="image-20200418124657054" style="zoom:50%;" />

$T_0^{GT}$：初始帧的真正模板。

### Tracking framework with UpdateNet

$\widetilde{T}_{i-1}$ 用于预测当前帧的目标位置。

将 $T_0^{GT}$， $\widetilde{T}_{i-1}$与 $T_i$ 串接起来作为 UpdateNet 的输入。

由于 $T_0^{GT}$ 最可靠，采用残差学习，即 UpdateNet 学习如何为当前帧修改 $T_0^{GT}$。

### Training UpdateNet

最小化更新的模板与下一帧中真实模板的欧式距离：

<img src="https://i.loli.net/2020/04/18/tTbvhRXM91fKrAL.png" alt="image-20200418124758354" style="zoom:50%;" />

#### Training samples

训练时，对于当前帧模板 $T_i$，一种选择是使用真实位置，这意味着当前帧的预测非常准确。但是，在实际跟踪中很少遇到这种情况。这种不切实际的假设使更新偏向于期望相对于 $T_i$ 发生很小的变化，因此 UpdateNet 无法学习有用的 updating funtion。

因此，我们需要通过在第 $i$ 帧中使用不完美的定位来提取用于训练的 $T_i$ 样本。我们可以通过使用累积的模板 $\widetilde{T}_{i-1}$ 预测当前帧位置，来模拟这种定位不完美的情况，这与实际跟踪保持一致。

#### Multi-stage training

我们可以使用由 UpdateNet 输出的 $\widetilde{T}_{i-1}$。但是这将使训练递归执行，低效而麻烦。

因此我们将训练分为多个阶段顺序执行。在第一阶段，在训练集上运行原始跟踪器执行标准线性更新：

<img src="https://i.loli.net/2020/04/18/6VBvrpx5AydziFN.png" alt="image-20200418124837753" style="zoom:50%;" />

通过这种方式来获得 accumulated templates 和每帧的预测框。

对于后续的每个阶段，使用上一阶段的 accumulated templates 和每帧的预测框，来训练 UpdateNet：

<img src="https://i.loli.net/2020/04/18/goyKmzGTh3AWbVH.png" alt="image-20200418125408733" style="zoom:50%;" />

#### Implementation details

将所有模板保存在磁盘上。

UpdateNet 是两个卷积层。

采用多少历史帧？已将 $\widetilde T_{i-1}$ 保存在了磁盘上，而 $\widetilde T_{i-1}$ 表示从第一帧到当前帧的全部信息。

stage = 3。