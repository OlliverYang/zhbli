---
title: >-
  [CVPR2019] Joint Discriminative and Generative Learning for Person
  Re-identification
date: 2020-04-21 15:57:21
tags:
- CVPR2019
- Person Re-Identification
mathjax: true
---

## Abstract

首次提出，将 reid 学习和数据生成整合到一个端到端框架中，名为 GD-Net。

https://github.com/NVlabs/DG-Net

## Method

### Generative Module

generative module：

- 输入：训练集中的两幅真实图像。其中一幅真实图像用于提供 appearance code，另一幅真实图像用于提供 structure code。structure code 的空间分辨率更高，以保留几何和位置属性。
- 输出：新的行人图像。
- 结构
  - appearance encoder $E_a:x_i \rightarrow a_i$
  - structure encoder $E_s:x_j \rightarrow s_j$
  - decoder $G: (a_i,s_j)\rightarrow x_j^i$
  - discriminator $D$：用于区分图像是生成的还是真实的。
- objectives
  - self-identity generation，用于规范 generator。
  - cross-identity generation，是生成的图像可控并匹配帧数数据分布。

#### Self-identity generation

给定个一幅图像，generative module 首先学习如何重构这幅输入图像。这在整个生成过程中起到了重要的正则化作用。同身份、同图像重构损失如下：

<img src="https://i.loli.net/2020/04/21/2GyKsJvF8EXZm3w.png" alt="image-20200421162403905" style="zoom:50%;" />

我们还假设对于同一类别的两个行人图像 $x_i,x_t$，使用 $x_i$ 的结构信息以及 $x_t$ 的表观信息就能重构 $x_i$ 的表观信息。同身份、跨图像重构损失如下：

<img src="https://i.loli.net/2020/04/21/D9BnNU4V7iqwvXz.png" alt="image-20200421162704711" style="zoom:50%;" />

为了保证不同图像的 appearance code 不同，使用 identification loss 区分不同身份：

<img src="https://i.loli.net/2020/04/21/g5yzAWNhDrcbJQs.png" alt="image-20200421163100753" style="zoom:50%;" />

其中 $p(y_i|x_i)$ 是基于 appearance code 预测的 $x_i$ 输入 ground truth class $y_i$ 的概率。

#### Cross-identity generation

使用不同身份生成图像。因此没有 pixel-level 的监督信号。相反，我们引入 latent code reconstruction，基于 appearance code 和 structure code 来控制图像生成。我们希望生成的图像 $x^i_j=G(a_i,s_j)$ 具有 $x_i$ 的表观和 $x_j$ 的结构。因此我们在得到生成图像后重构 appearance code 和 structure code：

<img src="https://i.loli.net/2020/04/21/QiHmtA2DjERqfPT.png" alt="image-20200421163855378" style="zoom:50%;" />

此外，为了保持身份一致性，使用生成图像的 appearance code 计算 identification loss：

<img src="https://i.loli.net/2020/04/21/Kl4vXuZLVkbpm7c.png" alt="image-20200421164219836" style="zoom:50%;" />

另外，我们还用对抗损失使得生成图像与真实图像的分布相同：

<img src="https://i.loli.net/2020/04/21/Wx1mhf4gBctA5Ly.png" alt="image-20200421164342052" style="zoom:50%;" />

###  Discriminative Module

#### Primary feature learning

我们最小化如下两者的 KL 散度：

1. 由 discriminative module 预测的概率分布 $p(x^i_j)$
2. 由 teacher 预测的概率分布 $q(x^i_j)$

<img src="https://i.loli.net/2020/04/21/LKe1QjYX3HcyTaV.png" alt="image-20200421165125391" style="zoom:50%;" />

### Fine-grained feature mining

<img src="https://i.loli.net/2020/04/21/PmBgW2JFAvQux9K.png" alt="image-20200421165610583" style="zoom:50%;" />