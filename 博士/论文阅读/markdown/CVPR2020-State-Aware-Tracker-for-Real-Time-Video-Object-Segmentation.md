---
title: '[CVPR2020] State-Aware Tracker for Real-Time Video Object Segmentation'
date: 2020-07-17 10:21:08
tags:
- CVPR2020
- Video Object Segmentation
- Inter-Frame Consistency
mathjax: true
---

## Abstract

本文提出 `State Aware Tracker (SAT)`，利用了帧间一致性`inter-frame consistency`。

### 性能

DAVIS2017-Val：72.3% J&F mean

速度：39FPS

https://github.com/MegviiDetection/video_analyst

## Introduction

在VOS任务中，来自先前帧的信息可以被视为时间上下文，这可以为后续预测提供有用的提示。

<img src="https://i.loli.net/2020/07/17/az6fDo8QBM7s4eG.png" alt="image-20200717104519088" style="zoom: 33%;" />

### 先前算法的缺点

以前的方法[22,17,31,27,31]使用特征级联`feature concatenation`，相关`correlation`或光流`optical flow`将前一帧预测的mask或特征传播到当前帧，但是它们具有明显的缺点：

1. 先前的工作通常会在完整图像上传播信息，但目标通常会占据较小的区域。因此在全图上操作会造成计算冗余。
2. 目标在整个视频中可能会经历不同的状态，但是先前的方法使用固定的传播状态，没有进行自适应`adaptation`，容易使得在长序列上不稳定。
3. 仅从利用第一帧或前一帧进行目标建模`target modeling`，但这不足以进行`holistic representation`。

> [22] Paul Voigtlaender, Yuning Chai, Florian Schroff, Hartwig Adam, Bastian Leibe, and Liang-Chieh Chen. **Feelvos: Fast end-to-end embedding learning for video object segmentation**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 9481–9490, 2019.
>
> [17] Federico Perazzi, Anna Khoreva, Rodrigo Benenson, Bernt Schiele, and Alexander Sorkine-Hornung. **Learning video object segmentation from static images**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 2663–2672, 2017.
>
> [31] Linjie Yang, Yanran Wang, Xuehan Xiong, Jianchao Yang, and Aggelos K Katsaggelos. **Efficient video object segmentation via network modulation**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 6499–6507, 2018.
>
> [27] Huaxin Xiao, Jiashi Feng, Guosheng Lin, Yu Liu, and Maojun Zhang. **Monet: Deep motion exploitation for video object segmentation**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 1140– 1148, 2018.

### 本文的解决方法

本文将VOS重新定义为状态估计`state estimation`和`target modeling`的连续过程，其中分割是状态估计的一部分。

SAT利用帧间一致性，将每个目标视为一个小轨迹`tracklet`。

为了构建可靠的信息流，提出估计反馈机制`estimation-feedback mechanism`，使算法了解当前状态并针对不同状态进行自适应。

SAT使用时间上下文动态构建全局表示`global representation `，用于在整个视频序列中提供可靠的视觉引导`visual guidance`。

![image-20200717112006016](https://i.loli.net/2020/07/17/Vb3HcliN8oTFO16.png)

#### 推理过程

分为如下三步：

1. **Segmentation**：SAT在目标周围裁剪搜索区域，并将每个目标作为小轨迹。联合分割网络` Joint Segmentation Network`可预测每个小轨迹的mask。
2. **Estimation**：状态估计器`State Estimator`评估分割结果并产生状态得分以表示当前状态。
3. **Feedback**：基于状态估计结果，设计了两个反馈回路` feedback loops`。
   1. **Cropping Strategy Loop**：自适应地选择不同的方法来预测目标的边界框。然后，我们根据预测框裁剪下一帧的搜索区域。这种切换策略`switching strategy`使跟踪过程随着时间的推移更加稳定。
   2. **Global Modeling Loop**：使用状态估计结果动态更新全局特征。全局特征可以协助联合分割网络生成更好的分割结果。

## Related Work

[17] 将前一帧预测的mask与当前帧的图像连接起来，以提供空间引导。

[22] 提出逐像素相关性，以在连续帧上传递位置敏感的嵌入。

> [22] Paul Voigtlaender, Yuning Chai, Florian Schroff, Hartwig Adam, Bastian Leibe, and Liang-Chieh Chen. **Feelvos: Fast end-to-end embedding learning for video object segmentation**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 9481–9490, 2019.

## Method

![image-20200723132410035](https://i.loli.net/2020/07/23/cbknRIUXP83wOd2.png)

### Segmentation

#### 显著性编码器

输入：以目标为中心的图像块。

#### 相似性编码器

输入：当前帧的搜索区域和第一帧的目标区域。

通过逐元素相加将如下三个特征进行融合：

1. 显著性编码器的特征
2. 相似性编码器的特征
3. 全局特征

### Estimation

通过手工设置的规则，为预测的模板打分。

## Experiments

### Network Training

训练分为两个阶段：

1. 在目标跟踪数据集上训练 similarity encoder 和 regression head。
2. 固定 similarity encoder 和 regression head 的权重，训练整个网络。Saliency encoder 的 backbone 和 Global  Modeling Loop 的特征提取器在 ImageNet 上进行预训练。

训练集包括 COCO，DAVIS2017 training set 和 YouTube-VOS training set。

训练时，在一段视频中随机选择一张 target image 和 一张 search image。Saliency encoder 将 cropped search image 作为输入，而 Global  Modeling Loop 将 cropped target image 作为输入。使用 ground truth mask 过滤 target image 的背景，以训练 Global Modeling Loop 的特征提取器。

其他参数：

- batch size = 16
- gpu_num = 8
- 训练时间 = 8h
- epoch = 20