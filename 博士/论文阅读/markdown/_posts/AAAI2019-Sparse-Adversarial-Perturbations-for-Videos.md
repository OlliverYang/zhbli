---
title: '[AAAI2019] Sparse Adversarial Perturbations for Videos'
date: 2020-08-20 14:07:49
tags:
- AAAI2019
- Adversarial Attack
mathjax: true
---

## Methodology

定义$X\in R^{T\times W\times H\times C}$为干净视频。$\hat X$ 为对抗样本。$E=\hat X-X$为扰动。目标函数是：

<img src="https://i.loli.net/2020/08/20/Gcv28nbdBqRxHZy.png" alt="image-20200820141242837" style="zoom:50%;" />

l是损失函数，用于衡量prediction和gt的差距。本文中使用交叉熵损失：$l(u,v)=log(1-uv)$。J是网络。$1_y$是标签y的onehot编码。

为了获得应用于整个视频的通用对抗扰动，需要求解以下问题：

<img src="https://i.loli.net/2020/08/20/QS1GRVgcrUpE5f6.png" alt="image-20200820141719546" style="zoom:50%;" />

为了更好的控制稀疏程度，并研究跨帧的扰动传播，我们在视频上添加了时间掩码，使得某些帧不进行扰动：

<img src="https://i.loli.net/2020/08/20/xCgOaEkoPQBjL2u.png" alt="image-20200820142117569" style="zoom:50%;" />

其中$M\in \{0,1\}^{T\times W\times H\times C}$为 temporal mask。

令$\theta=\{1,2,...,T\}$表示帧的下标，$\Phi$是$\theta$的子集，有K个元素。如果$t\in \Phi$，则$M_t=0$，否则为1。S=K/T为稀疏度。

如果是targeted攻击，则目标函数为：

<img src="https://i.loli.net/2020/08/20/dGW5qtKjnbBFmvE.png" alt="image-20200820142754075" style="zoom:50%;" />

其中$y_i^*$是 targeted label。

注意此公式中符号为加号。

