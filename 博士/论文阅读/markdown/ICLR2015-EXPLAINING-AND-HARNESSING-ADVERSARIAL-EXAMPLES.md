---
title: '[ICLR2015] EXPLAINING AND HARNESSING ADVERSARIAL EXAMPLES'
date: 2020-04-25 12:56:08
tags: ICLR2015
mathjax: true
---

## ABSTRACT

https://raw.githubusercontent.com/pytorch/tutorials/master/beginner_source/fgsm_tutorial.py

对抗样本：通过对数据集中的样本进行小的、故意的、最坏情况的扰动，使得网络以告置信度输出错误答案。

以前对这种现象的解释集中于非线性和过度拟合。本文认为神经网络容易受到对抗干扰的原始是网络的线性特性。

本文提出了简单快速地生成对抗样本的方法。

## INTRODUCTION

[Szegedy et al. (2014b)] 提出，神经网络易受对抗样本的攻击。

> Szegedy, Christian, Zaremba, Wojciech, Sutskever, Ilya, Bruna, Joan, Erhan, Dumitru, Goodfellow, Ian J., and Fergus, Rob. **Intriguing properties of neural networks**. ICLR, abs/1312.6199, 2014b. URL http://arxiv.org/abs/1312.6199.

## THE LINEAR EXPLANATION OF ADVERSARIAL EXAMPLES

首先，我们解释线性模型中的对抗样本。在很多问题中，输入特征的精度是受限的。例如，如果像素是 8 位的，则图像会丢弃低于动态范围的 1/255 的所有信息。因为特征的精度有限，因此如果扰动的每个元素 $\pmb{\eta}$ 都小于特征精度，则分类器对于输入 $\pmb{x}$ 和对抗输入 $\tilde{\pmb{x}}=\pmb{x}+\pmb{\eta}$ 的响应不同，这是不合理的。我们希望分类器为 $\pmb{x}$ 和 $\tilde{\pmb x}$ 输出相同类别，只要 $||\pmb \eta||_{\infty}<\epsilon$。

考虑权重向量 $\pmb w$ 和对抗样本的 dot product：

<img src="https://i.loli.net/2020/04/25/fI2FBNwCMYEKbda.png" alt="image-20200425132139129" style="zoom:50%;" />

对抗扰动使得激活增加了 $\pmb w^{\mathsf T}\pmb \eta$。我们可以在 max norm 约束下，令 $\eta=\text{sign}(\pmb w)$ 从而最大化此增量。如果 $\pmb w$ 是 $n$ 维，weight vector 中元素的平均幅值是 $m$，激活将增加 $\epsilon mn$。

虽然 $||\pmb \eta||_{\infty}$ 不会随维数增长，但是由 $\eta$ 引起的扰动噪声的激活变化，会随着 $n$ 线性增加。因此对于高维问题，我们可以对输入进行小的变化，而对输入噪声大的更改。

我们可以将其视为 accidental steganography，其中线性模型被迫处理与其权重最接近的信号，即使存在多个信号，且其他信号具有更大的幅度。

## LINEAR PERTURBATION OF NON-LINEAR MODELS

对抗样本的线性解释，指出了生成对抗样本的快速方法。

设 $\pmb \theta$ 是网络参数，$\pmb x$ 是网络输入，$y$ 是对应的 targets，$J(\pmb \theta,\pmb x, y)$ 适用于训练网络的 cost。我们可以在 $\pmb \theta$ 的当前值进行线性化，获得 optimal max-morm constrained pertubation：

<img src="https://i.loli.net/2020/04/25/oHUBDlXVavyC3Ti.png" alt="image-20200425140448919" style="zoom:50%;" />

我们将其称为 `fast gradient sign method`，用于生成对抗样本。注意，梯度可以通过反向传播进行有效计算。这一简单的算法可以加速对抗网络的训练，或者作为分析神经网络的方法。

