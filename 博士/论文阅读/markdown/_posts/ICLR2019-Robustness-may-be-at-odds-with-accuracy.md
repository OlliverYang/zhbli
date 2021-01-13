---
title: '[ICLR2019] Robustness may be at odds with accuracy'
date: 2020-05-07 19:18:48
tags:
- ICLR2019
mathjax: true
---

## Abstract

本文认为，adversarial robustness 和 standard generalization 之间存在 inherent tension。具体而言，训练 robust models 可能不仅会消耗更多资源，还会导致准确性下降。我们证明在模型的准确性和对 adversarial perturbations 的鲁棒性之间的折衷可能存在于相当简单和自然的环境中。这些发现也证实了在更复杂的环境中凭经验观察到的类似现象。此外，我们认为造成这种现象的原因是 robust classifiers 与 standard classifiers 学习到不同的特征表示的结果。这些差异带来了意想不到的好处——通过 robust models 学习的表示倾向于与  salient data characteristics 和 human perception 能够更好地对齐。

## On the Price of Adversarial Robustness

在传统的分类中，目的是训练 expected loss/population risk 低的模型（公式 1）：

<img src="https://i.loli.net/2020/05/08/k6KurILd3fROUcv.png" alt="image-20200508113009574" style="zoom:50%;" />

#### Adversarial robustness

希望模型是 adversarially robust 的，因此目的是训练 expected adversarial loss 低的模型（公式 2）：

<img src="https://i.loli.net/2020/05/08/IpeG4KU1PzLZTB6.png" alt="image-20200508113431847" style="zoom:50%;" />

其中，$\Delta$ 表示可引起分类错误的对抗扰动。本文重点关注 $\Delta$ 是 $\ell_p$-bounded perturbations 的集合的情况：$\Delta=\{\delta\in \mathbb R^d|\ ||\delta||\le\varepsilon\}$。

#### Adversarial training

迄今为止，建立 adversarially robust models 的最成功的方法是对抗训练。对抗训练的动机是将公式 2 视为统计学习问题，因此需要解决相应的 (adversarial) empirical risk minimization 问题：

<img src="https://i.loli.net/2020/05/08/s4WKal7TiRbmLtY.png" alt="image-20200508114507694" style="zoom:50%;" />

虽然对抗训练很有效，但也存在一些缺点：

- 训练时间增加：需要在每个参数更新步骤中计算新的扰动。
- 需要更多训练数据。

然而本文发现，robust classifiers 还存在另一个缺点：精度不如 standard classifiers。

#### Adversarial Training as a Form of Data Augmentation

我们的出发点是，对抗训练是数据增强的 “终极形式”。然而实验证明，经过对抗性的网络，准确性会降低。本文的目的是说明和解释这种现象的根源。特别是，我们想了解，为什么在对抗性和精度之间要进行取舍？

本文证明，这可能是 adversarial robustness 和 standard generalization 的目标不同所导致的必然结果。

### Adversarial robustness might be incompatible with standard accuracy

略。

### The importance of adversarial training

略。

## Unexpected benefits of adversarial robustness

和 robust models 一样，对于人类而言，同样对小的扰动不敏感，因此 robust models 比 standard models 更符合人类视觉。

#### Loss gradients in the input space align well with human perception

通过可视化损失相对于像素的梯度，发现经过对抗训练的网络的梯度与输入图像的 perceptually relevant features（如边缘）对齐得很好。而 standard networks 的梯度对人类来说非常复杂。

![image-20200508123448564](https://i.loli.net/2020/05/08/mk4BYVGsgQ3b2p8.png)

#### Adversarial examples exhibit salient data characteristics

现在研究 robust/standard models 的对抗样本在视觉上是什么样的。

使用 PGD 生成对抗样本。

![image-20200508123233911](https://i.loli.net/2020/05/08/7iZazK4MmfIr5UN.png)

如上图所示，robust models 的对抗样本，具有另一类别的显著特征，而 standard models 的对抗样本仅比输入图像更加嘈杂。

#### Smooth cross-class interpolations via gradient descent

通过在原始图像和 PGD 生成的图像之间进行线性插值，可以得到两类直接平滑的，感觉上合理的插值。这种插值往往仅通过 GAN 还能实现。我们推测本文的插值方法和基于 GAN 的插值方法的相似性不是巧合，鞍点问题可能是这种现象的根源。

![image-20200508123923889](https://i.loli.net/2020/05/08/8TKqAF1NvGQnwID.png)