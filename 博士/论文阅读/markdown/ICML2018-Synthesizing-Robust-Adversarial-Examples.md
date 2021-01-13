---
title: '[ICML2018] Synthesizing Robust Adversarial Examples'
date: 2020-08-25 14:21:23
tags:
- ICML2018
- Adversarial Attack
mathjax: true
---

## Approach

本文介绍了 Expectation Over Transformation (EOT) 算法，这是一个通用的构建对抗样本的方法。使用该方法构建的对抗样本在 a chosen transformation distribution $T$ 上仍能保持对抗性。

###  Expectation Over Transformation

假设我们预先知道一组可能的类别 $Y$，以及分类器的输入空间 $X$，我们可以访问函数 $P(y|x)$ 和梯度 $\nabla_xP(y|x)$，对于任意类别 $y$ 和输入 $x$。在标准情况下，通过最大化目标类别 $y_t$ 的对数似然来产生对抗样本：

<img src="https://i.loli.net/2020/08/25/78WtMcqrVz1FZ6s.png" alt="image-20200825153412797" style="zoom:50%;" />

这种方法在现实世界中，由于角度或视角的变化，对抗样本无法保持对抗性。

为了解决这一问题，我们提出了 Expectation Over Transformation (EOT)。EOT 的关键在于在优化过程中建模这种扰动。