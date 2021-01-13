---
title: '[CVPR2020] Siam R-CNN: Visual Tracking by Re-Detection'
date: 2020-04-18 17:58:47
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Architecture]
---

## Abstract

SiamRCNN 具有以下特点：

- 充分发挥两阶段检测器的作用。
- 提出 tracklet-based 动态传播算法，利用第一帧模板和先前帧预测信息，建模目标与干扰物的完整历史。这有利于更好的跟踪决策，并有利于在长期遮挡后重新跟踪物体。
- 提出难例挖掘，用于训练提出的 re-detector，以区分近似物体。

性能：

- https://github.com/VisualComputingInstitute/SiamR-CNN
- 速度：4.7 FPS。
- GOT-10k：0.649。

## Method

<img src="https://i.loli.net/2020/04/18/yvmBka258xpGCif.png" alt="image-20200418201225192" style="zoom:50%;" />

###  Siam R-CNN

Siam R-CNN 是基于两阶段检测器的 Siamese re-detector。检测器采用 coco 预训练的 80 类 faster rcnn。我们固定特征提取器和 RPN 参数，并用我们的 re-detection head 代替 category-specific detection。

为 re-detection head 准备输入：

1. 来自 RPN 的 proposed region，经过 RoI Align 得到固定尺寸的特征。
2. 得到第一帧 gt 目标的RoI Aligned features。

3. 将上述两个特征串接送入 $1\times 1$ 卷积，将通道数减半，作为 re-detection head 的输入。

Re-detection head 使用三级级联，不共享权重。结构与 faster rcnn 的 detection head 相同。输出类别数为 2。仅训练 re-detection head。

### Video Hard Example Mining

在常规的 Faster R-CNN 训练期间，从目标图像中 RPN 提出的区域中采样第二阶段的负样本。但是，在许多图像中，只有很少的负样本。为了最大程度地提高 re-detection head 的判别能力，我们需要在更难得负样本上进行训练。

我们没有选择用于检测的 general hard examples，而是通过检索其他视频的目标，选择相对 reference object 的困难样本。

#### Embedding Network

选择难例的直接方法是寻找相同类别。但这有三个问题：

1. 类别信息不总是可用。
2. 同类物体可能易于区分。
3. 不同类物体可能不易于区分。

我们受 reid 网络启发，提出 embedding network，从每个目标的 gt box 中提取嵌入向量，用于表示该目标的表观。我们使用 PReMVOS [60] 网络, 使用三元组损失，先在 coco 上训练以区分不同类别，后再 youtube_vos 上训练以区分不同实例。

> [60] J. Luiten, P. Voigtlaender, and B. Leibe. PReMVOS: Proposal-generation, refinement and merging for video object segmentation. In ACCV, 2018.

#### Index Structure

通过在嵌入空间查询与目标最接近的物体来寻找难例。

#### Training Procedure

每训练一帧时，在其他视频上运行

我们为训练集中的每个 gt box 预先计算 RoI-aligned 特征。

使用 index structure 选择目标的 10000 个最近邻，再从中选择 100 分作为额外的负样本。注意，这些负样本是 RoI-aligned 的特征，与目标特征串接并送入 $1\times 1$ 卷积后，作为 re-detection head 的输入。

###  Tracklet Dynamic Programming Algorithm

我们的 TDPA 利用时空信息，不仅跟踪目标，同时跟踪近似物体。

TDPA 维护一组 tracklets，即几乎肯定属于同一物体的短的检测序列。设计基于动态规划的评分算法，在第一帧到当前帧之间，选择最好的 `tracklets 序列`。

每个 detection 都是一个 tracklet 的一部分，由一个边框，重检测得分和 RoI-Aligned 特征组成。

一个 tracklet 由一组 detections 组成，每个 time step 对应一个 detection。

#### Tracklet Building

利用第一帧的边框初始化一个 tracklet。

对于新一帧，以如下方式更新一组 tracklets：

1. 运行网络的 backbone 和 RPN 获得 RoIs。
2. 为了补偿潜在的 RPN false negatives（当前帧的 RPN 网络没能检测出物体），通过前一帧输出的边框来扩展 RoIs。-> 目的：获取当前帧中所有候选目标。
3. 在这些 RoIs 上运行针对于第一帧模板的 re-detection head。
4. 在当前检测上重新运行 re-detection head 的分类部分，但这次以前一帧的检测作为参考，而不是第一帧。计算每对检测的相似性。-> 目的：将当前帧目标与上一帧目标进行配对。
5. 仅对空间距离小于 $\gamma$ 的检测对计算相似度。
6. 当新检测的得分高且没有歧义（没有其他检测具有同样高的相似性）时，将 tracklet 从上一帧扩展到当前帧。
7. 只要有任何歧义，就使用该检测初始化一个新的 tracklet。
8. 歧义通过 tracklet 评分步骤解决。

#### Scoring

一个 track $A=(a_1, ,,, a_N)$ 指 $N$ 个**不重叠**的 `tracklets 序列`。

一个 track 的总分包括：

- unary score，用于评估每个 tracklets 的质量。
- loc_score，惩罚 tracklets 间的空间跳跃。

<img src="https://i.loli.net/2020/04/20/RBVkCqAneQZLvUG.png" alt="image-20200420114730875" style="zoom:50%;" />

<img src="https://i.loli.net/2020/04/20/notCe13ySiscv6l.png" alt="image-20200420115107155" style="zoom:50%;" />

其中 $\text{ff_score}$ 指使用第一帧作为参考的 redetection reference。

#### Online Dynamic Programming

通过维护一个数组 $\theta$ 来有效找到具有最高总分的 `tracklets 序列`。对每个 tracklet $a$，$\theta [a]$ 保存了从第一帧开始，以 $a$ 结束的最优 `tracklet 序列`的总分。

一旦一个 tracklet 不再扩展，则将终止。因此对于每个新帧，仅需重新计算扩展的或新的 tracklets 的得分。

对于新的 time-step，首先为第一帧的 tracklet $a_{ff}$ 设置 $\theta[a_{ff}] = 0$，因为所有的 tracks 都必须以该 tracklet 开始。

之后，对于每个被更新的或新创建的 tracklet $a$，$\theta[a]$ 被计算为：

<img src="https://i.loli.net/2020/04/19/OSJIAB71PUma4uD.png" alt="image-20200419142508930" style="zoom: 50%;" />

其中，$\tilde a$ 指在 $a$ 开始前就结束的 tracklet（即无重叠）。

在更新当前帧的 $\theta$ 之后，选择具有最高动态规划得分的 tracklet $\hat a = \arg \max_a\theta[a]$。如果在当前帧中选择的 tracklets 不包含检测，则说明目标不存在。对于帧都需要预测框的数据集，使用上一帧的框代替，并赋得分为 0。