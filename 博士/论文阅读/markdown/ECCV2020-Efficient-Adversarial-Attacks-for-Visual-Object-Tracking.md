---
title: '[ECCV2020] Efficient Adversarial Attacks for Visual Object Tracking'
date: 2020-08-14 10:08:40
tags:
- Tracking
- ECCV2020
- Adversarial Attack
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## Introduction

Targeted Attack: embedded feature loss.

Untargeted Attack: drift loss.

generator: 用于生成对抗扰动。

## Related Work

###  Iterative and Generative Adversary

现有的对抗攻击主要基于**优化算法**和**生成算法**。

- 基于优化的对抗攻击通过计算DNN的梯度发现噪声的方向。
- 基于generator的对抗攻击包括GAP、UEA等。

## Generating Adversarial Examples

<img src="https://i.loli.net/2020/08/14/ZEr2qMc1aI4HoKy.png" alt="image-20200814125115034" style="zoom:50%;" />

### Problem Definition

$V=\{I_1,...,I_i,...,I_n\}$ 是具有 $n$ 帧的一段视频。$B^{gt}=\{b_1,...,b_i,...,b_n\}$ 是对应的 ground truth。预测的边框记为 $B^{pred}$。

$f_\theta(\cdot)$ 为跟踪器，$I_R$ 为 reference frame，$b^{init}$ 为第一帧的边框，$z=\tau(I_R,b^{init})$ 是 exemplar region; $I_C$ 为 candidate frame，$x=\tau(I_C,b^{search})$ 为 candidate region。

$\hat V=\{\hat I_1,...,\hat I_i,...,\hat I_n\}$ 是对抗视频。**生成器的作用是：攻击 candidate region** $\hat x_i = \tau(\hat I_i,b_i^{search})$。

#### 攻击类型定义

**Targeted Attack**：对抗视频引导跟踪器沿指定轨迹$C^{spec}$跟踪目标。

**Untargeted Attack**：对抗视频导致跟踪轨迹偏离真实目标。当 IoU 为 0 时，认为跟踪成功。	

### Drift Loss Attack

我们提出 drift loss，用于生成对抗扰动，使得孪生网络的响应图发生偏移。

首先定义

<img src="https://i.loli.net/2020/08/14/vGAmyM8lJopWSUa.png" alt="image-20200814105339752" style="zoom:50%;" />

其中 $s$ 表示 response score，$y$ 表示对应的 label。

<img src="https://i.loli.net/2020/08/14/ojbaHcY2ZQd8R5U.png" alt="image-20200814111624217" style="zoom:50%;" />

其中 $\mathcal G$ 指的是 generator。

上述公式的含义为：希望非中心区域的最大响应比中心区域的最大响应大。（公式中的min可能写错了）

<img src="https://i.loli.net/2020/08/14/xaEjvy23c1owSrO.png" alt="image-20200814111413309" style="zoom:50%;" />

上述公式的含义为：希望非中心区域的最大响应位置距离中心区域的最大相应位置更远。

<img src="https://i.loli.net/2020/08/14/qaoWkJwDYt7Vfbg.png" alt="image-20200814111442203" style="zoom:50%;" />

上述公式的含义为：求中心/非中心区域的最大响应位置。

<img src="https://i.loli.net/2020/08/14/tn4KruPacCpm5e7.png" alt="image-20200814111341425" style="zoom:50%;" />

### Embedded Feature Loss Attack

我们希望获得对抗性的 exemplar，并最小化其与特定轨迹区域之间的L2距离。因此，我们提出 embedded feature loss，以生成**对抗图像** $\hat z$ 和 $\hat x_{R+1}$。对抗样本的特征与 embedded image $e$ 接近：

<img src="https://i.loli.net/2020/08/14/Yih7UTFdl9BD1k5.png" alt="image-20200814123403528" style="zoom:50%;" />

其中，$e$ 表示指定的轨迹区域，$q\in \{z,x_{R+1}\}$ 分别表示 exemplar frame 和需要跟踪的 $R+1$ 帧。$\varphi$ 表示特征函数，$\mathcal G$ **表示对抗扰动。**

训练时，embedded images 的选择非常重要。

### Unified and Real-time Adversary

使用 GAN 生成对抗样本，具体来说，使用 cycle GAN 学习从图像到对抗扰动的映射。

对于判别器，使用 PatchGAN，损失函数为：

<img src="https://i.loli.net/2020/08/14/BhWkM1ouptO4e6C.png" alt="image-20200814124938815" style="zoom:50%;" />

为了使生成器生成的图像更加真实，生成器的损失可以表示为：

<img src="https://i.loli.net/2020/08/14/LfEkDRI2ciKmqVw.png" alt="image-20200814125404494" style="zoom:50%;" />

另外，使用L2距离作为损失，使得对抗图像与原始图像尽量相似：

<img src="https://i.loli.net/2020/08/14/YRKO4ehUgjF5HJ1.png" alt="image-20200814125548908" style="zoom:50%;" />

生成器的完整损失函数为：

<img src="https://i.loli.net/2020/08/14/F5ZigmRwTQEcdzy.png" alt="image-20200814125635173" style="zoom:50%;" />