---
title: >-
  [CVPR2020] Transferable, Controllable, and Inconspicuous Adversarial Attacks
  on Person Re-identification With Deep Mis-Ranking
date: 2020-08-17 10:26:28
tags:
- ReID
- CVPR2020
- Adversarial Attack
mathjax: true
---

## Methodology

### Overall Framework

我们希望使用生成器 $G$ 为每个输入图像 $I$ 产生扰动 $P$，以获得对抗样本 $\hat I$，从而攻击 ReID 网络 $T$。使用对抗生成网络实现这些 ，包括生成器 $G$ 和判别器 $D$。

### Learning-to-Mis-Rank Formulation For ReID

本文提出 mis-ranking loss，最小化不匹配的对的距离，最大化匹配的对的距离。

<img src="https://i.loli.net/2020/08/17/sO7xpgba8fMHCDV.png" alt="image-20200817104504437" style="zoom:50%;" />

