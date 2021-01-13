---
title: '[CVPR2020] High-Performance Long-Term Tracking with Meta-Updater'
date: 2020-04-24 14:33:54
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Model Update]
- [Tracking, Meta-Learning]
---

## Abstract

性能：

- （待开源）https://github.com/Daikenan/LTMU
- 13 FPS

本文关注 long-term 跟踪问题, 作者认为, 在 long-term 跟踪中进行 online update 有利有弊, 在捕获目标/背景变化的同时, 容易引入噪声. 因此, 本文设计了一个 Meta-Updater, 使用该 Meta-Updater 输出一个二值得分, 用于指示跟踪器在当前帧是否进行更新.

所提出的跟踪框架包括四个部分:

1. online local tracker
2. online verifier
3. SiamRPN-based re-detector
4. meta-updater: 用于指导跟踪器的更新.

##  Meta-Updater

###  Sequential Information for Meta-Updater

给定 online tracker $\mathcal{T}$，在第 $t$ 帧，定义 output response map 为  $\mathbf{R}_t$，output bounding box 为 $\mathbf{b}_t$，根据 $\mathbf{b}_t$ 裁剪的图像为 $\mathbf{I}_t$。

#### Geometric Cue

在第 $t$ 帧，跟踪器输出边框 $\mathbf{b}_t=[x_t,y_t,w_t,h_t]$ 作为跟踪状态。该边框仅仅反映当前目标的几何信息，然而一系列连续帧的边框反映了目标重要的运动信息，如速度，加速度，尺度变化等。

#### Discriminative Cue

定义 response map $\mathbf{R}_t$ 的最大值为 confidence score $s^C_t$。然而得分在跟踪过程中并不稳定。因此本文使用卷积网络彻底挖掘相应图的信息，获得 response vector：

<img src="https://i.loli.net/2020/04/24/xndThqoV2kXZ8vj.png" alt="image-20200424152302740" style="zoom:50%;" />

其中 $f^R(.;.)$ 为 CNN。

#### Appearance Cue

我们采用模板匹配方法作为重要补充，定义了表观得分：

<img src="https://i.loli.net/2020/04/24/ZLhH8AcOUN54K2m.png" alt="image-20200424152900176" style="zoom:50%;" />

其中 $\mathbf{W}^A$ 是离线训练的参数。由 [33] 知，网络 $f^A$ 可以通过三元组损失和分类损失相结合进行训练。

> [33] Hao Luo, Youzhi Gu, Xingyu Liao, Shenqi Lai, and Wei Jiang. Bag of tricks and a strong baseline for deep person re-identification. In CVPR, 2019.

#### Sequential Information

定义 sequential matrix 为：

<img src="https://i.loli.net/2020/04/24/buZFPfKimqoxpac.png" alt="image-20200424180705549" style="zoom:50%;" />

其中 $\mathbf{x}_t \in \mathbb{R}^{d \times 1}$ 是由 $s_t^C, \mathbf{v}^R_t, s^A_t, \mathbf{b}_t$ 串接得到的列向量。$t_s$ 用于平衡历史经验和当前观测。这一序列信息通过如下的 cascade LSTM 进行处理。

### Cascaded LSTM

LSTM 的基本概念如下：

<img src="https://i.loli.net/2020/04/24/DOgAop9QJblTnKf.png" alt="image-20200424153926418" style="zoom:50%;" />

下标 $f,i,o,c$ 表示 forget gate，input gate，output gate 和 memory cell。其他变量的定义：

- $\mathbf{x}_t$：LSTM unit 的输入向量。
- $\mathbf{f}_t$：forget gate 的 activation vector。
- $\mathbf{i}_t$：input gate 的 activation vector。
- $\mathbf{o}_t$：output gate 的 activation vector。
- $\mathbf{h}_t$：hidden state vector。
- $\mathbf{c}_t$：cell state vector。

#### Three-stage Cascaded LSTM

获得了 sequential features $\mathbf{X}_t$ 后，将该特征送入三级级联 LSTM 模型中，输出是二值得分，表示是否在线更新。

### Meta-Updater Training

#### Sample Collection

在不同训练视频上运行 local tracker，在所有帧上记录跟踪结果。然后将这些结果划分成时间片段：

<img src="https://i.loli.net/2020/04/24/xcPfqt4mS7NEXij.png" alt="image-20200424180600925" style="zoom:50%;" />

其中 $v$ 是 video index，$V$ 是训练集中的视频数量。$t_v$ 是视频 $v$ 的总帧数：

<img src="https://i.loli.net/2020/04/24/u5ic1X6qp2S7PWs.png" alt="image-20200424173219841" style="zoom:50%;" />

每个 time slice  $\mathbf{y}^v_t$ 包括：

1. bounding box
2. response map
3. response score
4. 时刻 $t$ 的 predicted target image
5. corresponding target template

$\mathbf{Y}^v_t$ 的标签是：

<img src="https://i.loli.net/2020/04/24/LtPWjyhS5wGNrF6.png" alt="image-20200424173654508" style="zoom:50%;" />

其中 $\mathbf{b}^v_t$ 是视频 $v$ 在第 $t$ 帧的 output bounding box。$\mathbf{g}^v_t$ 是对应的 ground truth。

#### Model Training

$\{\mathcal{T,MU(T)}\}$ 表示带有 meta-updater $\mathcal{MU(T)}$ 的 local tracker。

<img src="https://i.loli.net/2020/04/24/lieVvkJ9xSa1NIW.png" alt="image-20200424174601127" style="zoom:50%;" />