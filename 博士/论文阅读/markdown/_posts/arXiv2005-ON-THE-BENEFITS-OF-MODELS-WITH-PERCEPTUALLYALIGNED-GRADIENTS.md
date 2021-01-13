---
title: '[arXiv2005] ON THE BENEFITS OF MODELS WITH PERCEPTUALLY-ALIGNED GRADIENTS'
date: 2020-05-07 13:25:39
tags:
mathjax: true
---

## Abstract

Adversarial robust models 比标准模型具有更强的鲁棒性和更多可解释性，比如，梯度与图像能很好地对齐。

我们的实验表明，即使模型对于对抗攻击没有高鲁棒性，也可以使梯度具有可解释性并能与图像对齐。

具体来说，我们针对不同的 max-perturbation bound 执行对抗训练。具有 low max-perturbation bound 的对抗训练可导致模型具有可解释的特征，而性能仅比使用 clean samples 训练的网络略有下降。

## Introduction

通过向 clean inputs 上添加视觉上难以察觉的扰动，可以获得对抗样本，从而使网络的预测发生重大变化。

使用 min-max objective 进行对抗训练的分类器，可以在对抗样本上实现较高准确性 [Madry et al. (2018b)]。

> Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. **Towards deep learning models resistant to adversarial attacks**. ICLR, 2018b.

最近，[Tsipras et al. (2018); Santurkar et al. (2019)] 证明了对抗训练的鲁棒网络可以和图像对齐，在梯度方向上更新图像使 target class 的得分最大化，可以改变图像以具有 target class 的视觉特征。

> Dimitris Tsipras, Shibani Santurkar, Logan Engstrom, Alexander Turner, and Aleksander Madry. **Robustness may be at odds with accuracy**. arXiv preprint arXiv:1805.12152, 2018.
>
> Shibani Santurkar, Dimitris Tsipras, Brandon Tran, Andrew Ilyas, Logan Engstrom, and Aleksander Madry. **Image synthesis with a single (robust) classifier**. arXiv preprint arXiv:1906.09453, 2019.

此外，[Kaur et al. (2019)] 将感知上有意义的属性扩展到 randomized smoothing robust models，并认为   perceptually-aligned gradients 可能是鲁棒模型的通用属性。

本文表明，即使是在较低的 max-perturbation bound 上执行对抗训练，也具有 perceptually-aligned 的可解释特征。尽管这些模型没有显示出很高的对抗鲁棒性，但是准确性可与标准模型相媲美。

## EXPERIMENTS AND RESULTS

本文使用 FSGM 或 PGD [Madry et al. (2018b)] 进行 adversarial training (AT)。

<img src="https://i.loli.net/2020/05/07/nfwg5DbMm6RykLd.png" alt="image-20200507161959068" style="zoom:50%;" />

上图可视化了 image level gradients。可以看出，natural model 的梯度没有与图像对齐，而经对抗训练的梯度可以与图像对齐。