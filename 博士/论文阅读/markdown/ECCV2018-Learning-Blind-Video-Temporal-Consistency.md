---
title: '[ECCV2018] Learning Blind Video Temporal Consistency'
date: 2020-07-19 15:59:11
tags:
- ECCV2018
- Inter-Frame Consistency
mathjax: true
---

## Learning Temporal Consistency

<img src="https://i.loli.net/2020/07/19/uZB8OyWV7NQDkvT.png" alt="image-20200719164119255" style="zoom:50%;" />

###  Recurrent network

网络的输入包括：

- 原始视频 $\{I_t|t=1...T\}$
- 逐帧处理的视频 $\{P_t|t=1...T\}$

网络的输出是：

- 时间一致（`temporally consistent`）的输出视频 $\{O_t|t=1...T\}$。

为了有效处理任意长度的视频，开发了 image transformation network 作为 recurrent convolutional network，用于在线生成 output frames。

在每个 time step，网络学习生成与 $O_{t-1}$ 在时间上一致的 $O_t$。$O_t$ 在下一个 time step 中成为网络的输入。

为了捕获视频的时空信息，我们在 image transformation network 中引入一个 ConvLSTM 层。

###  Loss functions

#### Content perceptual loss

该损失定义为：

<img src="https://i.loli.net/2020/07/19/ikxlsGoNeZfqgJA.png" alt="image-20200719162452347" style="zoom:50%;" />

$N$ 是一帧中的像素总数。

$\phi_l(\cdot)$ 是 VGG19 第 $l$ 层的特征激活。

$O_t^{(i)}\in \mathbb R^3$ 表示输入图像 $O_t$ 在位置 $i$ 的像素值。

#### Short-term temporal loss

该损失定义为：

<img src="https://i.loli.net/2020/07/19/4NlfK1wQH7ipJVg.png" alt="image-20200719163107691" style="zoom:50%;" />

其中 $\hat O_{t-1}$ 利用光流 $F_{t->t-1}$ 对 $O_t$ 进行 warp 得到。

$M^{(i)}_{t->t-1} = \exp(-\alpha||I_t-\hat I_{t-1}||_2^2)$ 是 visibility mask。

在训练时，使用 FlowNet2 计算光流。

使用双线性采样层 [22] 来 warp frames。

> [22] Jaderberg, M., Simonyan, K., Zisserman, A., Kavukcuoglu, K.: Spatial transformer networks. In: NIPS (2015)

#### Long-term temporal loss

该损失定义为：

<img src="https://i.loli.net/2020/07/19/tHD5v8COfLXiNaT.png" alt="image-20200719164025298" style="zoom:50%;" />

###  Image transformation network

由于 $O_t$ 和 $P_t$ 看起来会非常相似，因此预测残差而不是实际像素值：

<img src="https://i.loli.net/2020/07/19/6d2GuvhWyjXKF9i.png" alt="image-20200719164342897" style="zoom:50%;" />

该网络由 2 个卷积层，B 个残差块，1 个 ConvLSTM 层，和两个反卷积层构成。