---
title: >-
  [CVPR2020] Bridging the Gap Between Anchor-based and Anchor-free Detection via
  Adaptive Training Sample Selection
date: 2020-05-11 13:25:47
tags:
- CVPR2020
- Object Detection
mathjax: true
---

## Difference Analysis of Anchor-based and Anchor-free Detection

本文采用 anchor-based RetinaNet 和 anchor-free FCOS 进行对比。

### Essential Difference

<img src="https://i.loli.net/2020/05/11/Y9NhOIdXCUL4G1u.png" alt="image-20200511133103158" style="zoom:50%;" />

两个本质区别：分类和回归。

#### 分类

- RetinaNet 利用 IoU 将不同金字塔级别的 anchors 分为正或负。$\text{IoU} > \theta_p$ 时为正，$\text{IoU} < \theta_n$ 时为负。其他 anchors 训练期间被忽略。
- FCOS 使用空间和尺度约束从不同的 pyramid levels 中划分 anchor points。首先将位于 ground-truth box 内的 anchor points 视为候选正样本（空间约束）。然后根据在每个 pyramid level 上定义的 scale range 选择最终的正样本（尺度约束）。

<img src="https://i.loli.net/2020/05/11/NJAYHuoeL7gp4Tb.png" alt="image-20200511134636102" style="zoom:50%;" />

由上图可知：

1. 对于 RetinaNet 使用 spatial and scale constraint 代替 IoU，性能从 37.0 提高到 37.8。
2. 对于 FCOS 使用 IoU 代替 spatial and scale constraint，性能从 37.8 下降到 36.9。

这一结果表明，正负样本的定义是 anchor-based 与 anchor-free 检测器的本质区别。

#### 回归

RetinaNet 回归的起始状态是一个框，而 FCOS 回归的起始状态是一个点。但实验表明这是无关紧要的区别，而不是本质差别。

## Adaptive Training Sample Selection

由之前的结论可知，anchor-free 改善了对正负样本的定义。受此启发，我们深入研究了目标检测中的基本问题：如何定义正/负训练样本，并提出 Adaptive Training Sample Selection (ATSS)。

### Description

ATSS 根据目标的统计特征自动划分正负样本。步骤如下：

1. 对于图像中的每个 ground-truth box $g$，首先找出候选正样本：在每个 pyramid level 上，基于 L2 距离选择接近于 $g$ 的中心选择 $k=9$ 个 anchor boxes。假设有 $\mathcal L$ 个 pyramid levels，ground-truth box $g$ 有 $k\times \mathcal L$ 和候选正样本。
2. 计算候选样本与 $g$ 的 IoU ，并计算均值与标准差。
3. 该 ground-truth $g$ 的 IoU 阈值为均值与标准差之和：$t_g=m_g+v_g$。
4. 选择大于阈值的候选框为正样本，同时要求正样本的中心点位于 ground-truth box 内。
5. 如果将一个 anchor box 分配给多个 ground-truth box，则选择具有最高 IoU 的 anchor box。
6. 负样本 $\mathcal{N=A-P}$。

这一方法的动机解释如下：

- 根据 anchor box 和 object 之间的中心距离选择 candidates。
- 使用均值和标准差之和作为 IoU 阈值。
- 正样本的中心点位于 ground-truth box 内。
- 维护不同目标间的公平性。相反，RetinaNet 和  FCOS 的策略对较大的目标有更多正样本。
- 几乎不适用超参数。