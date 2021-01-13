---
title: >-
  [CVPR2017] Plug & Play Generative Networks: Conditional Iterative Generation
  of Images in Latent Space
date: 2020-05-09 10:17:32
tags:
- CVPR2017
mathjax: true
---

## Abstract

生成高分辨率，逼真的图像一直是机器学习的长期目标。最近，[37] 提出了一种有趣的方式来合成图像，方法是在 generator network 的 latent space 中执行 gradient ascent，以最大化分类网络中的一个或多个神经元的激活。

> [37] A. Nguyen, A. Dosovitskiy, J. Yosinski, T. Brox, and J. Clune. **Synthesizing the preferred inputs for neurons in neural networks via deep generator networks**. In Advances in Neural Information Processing Systems, 2016.

本文通过在 latent code 上引入额外先验来扩展该方法，改善了样本的质量和多样性。

另外，本文为这类 activation maximization methods 提供了统一的概率解释，称这类模型为 “Plug and Play Generative Networks”。

PPGNs 由两部分组成：

1. 能够绘制各种 image types 的 generator network G。
2. 告诉 generator 绘制什么的 "condition" network C。