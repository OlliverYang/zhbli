---
title: '[CVPR2017] Universal adversarial perturbations'
date: 2020-08-21 17:34:07
tags:
- CVPR2017
- Adversarial Attack
mathjax: true
---

## Universal perturbations

令 $\mu$ 表示图像的分布。$\hat k$ 是分类函数，为图片 $x\in R^d$ 预测标签 $\hat k(x)$。本文的目的是寻找扰动向量 $v\in R^d$ 愚弄从 $\mu$ 中采样的大多数数据点：

<img src="https://i.loli.net/2020/08/21/miYAChT2HUtyz6n.png" alt="image-20200821174537099" style="zoom:50%;" />

需满足如下两点约束：

<img src="https://i.loli.net/2020/08/21/3QSlXn6ONLhRJ1m.png" alt="image-20200821174636205" style="zoom:50%;" />

### Algorithm

令 $X=\{x_1,...,x_m\}$ 是从 $\mu$ 中采样的数据集，本算法寻找通用扰动 v。算法在X上迭代运行，逐渐找到v。在每次迭代时，计算最小扰动$\Delta v_i$ 。该最小扰动将当前的 pertubed point $x_i+v$发送到分类器的决策边界：

<img src="https://i.loli.net/2020/08/23/dltp91SHjDBGhvE.png" alt="image-20200823123716583" style="zoom:50%;" />

更新规则是：

<img src="https://i.loli.net/2020/08/23/BnMCKHagjrh618T.png" alt="image-20200823123826183" style="zoom:50%;" />

算法终止条件：

<img src="https://i.loli.net/2020/08/23/UqTodmEDraxWpez.png" alt="image-20200823123935733" style="zoom:50%;" />