---
title: >-
  [CVPR2020] Cooling-Shrinking Attack: Blinding the Tracker with Imperceptible
  Noises
date: 2020-05-03 09:20:33
tags:
- CVPR2020
- Tracking
- Adversarial Attack
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## Abstract

本文利用 cooling-shrinking attack method 攻击孪生网络跟踪器。

性能：

- https://github.com/MasterBin-IIAU/CSA

- 在三个数据库上进行攻击：OTB100、VOT2018、LaSOT。

## Introduction

`Adversarial attack` 常分为两类：

1.  iterative-optimization-based atracks：进行梯度上升，最大化 adversarial objective function。
2. deep-network-based attacks：使用大量数据训练 adversarial perturbation-generator。

本文提出的 cooling-shrinking attack method 学习有效的 perturbation generator，通过如下方式使跟踪失败：

- 冷却 heatmap 中存在目标的 hot regions。
- 缩小目标边框。

## Cooling-Shrinking Attack

本文提出 adversarial perturbation-generator 来欺骗 siamrpn++ 跟踪器，设计两种 perturbation-generator 分别攻击 search regions 和 template。

### Overall Pipeline

<img src="https://i.loli.net/2020/05/03/TltiZcINpuAxDG3.png" alt="image-20200503093629859" style="zoom:50%;" />

由于攻击 template 和攻击 search regions 的过程非常相似，因此仅讨论攻击搜索区域：

1. 在训练过程中，首先将 $N$ 个预先裁剪好的未被扰动的搜索区域送入 perturbation-generator，从而向搜索区域添加难以察觉的噪声。

2. 然后，将 perturbed search regions 与 clean template 送入 siamrpn++，生成 adversarial classification/regression maps。

3. Adversarial heatmaps 中的目标区域希望有较低的响应值。

4. 为了得到这些区域，将 unperturbed search regions 送入网络，得到 clean heatmaps。

5. 通过 adversarial cooling-shrinking loss 和 L2 loss 训练 perturbation-generator。

### Cooling-Shrinking Loss

Cooling-shrinking loss 包括两部分：

1. cooling loss $L_C$：用于  heatmaps $M_H$。冷却 heatmap 中存在目标的 hot regions。导致跟踪器丢失目标。
2.  shrinking loss $L_S$：用于 regression maps $M_R$。缩小目标边框，引起累计误差，导致跟踪失败。

为了确定目标的位置，引入 clean heatmaps $M^c_H$。

为了便于计算，将 heatmaps 转换成二维矩阵：

1. clean heatmaps $M^c_H\rightarrow \widetilde{M^c_H}\in \mathbb R^{N\times2}$。
2. adversarial heatmaps $M^a_H\rightarrow \widetilde{M^a_H}\in \mathbb R^{N\times2}$。
3. adversarial regression maps $M^a_R\rightarrow \widetilde{M^a_R}\in \mathbb R^{N\times4}$。

对 clean heatmaps 进行 softmax 并使用阈值得到 binary attention maps $\mathcal A$ 用于确定前景和背景。

算法流程为：

<img src="https://i.loli.net/2020/05/03/WXc13NhlDATfyKw.png" alt="image-20200503102021919" style="zoom:50%;" />

### Implementation Details

#### Network Architectures

Perturbation-generator 采用 U-Net 架构。

网络通过 cooling loss、shrinking loss 和 L2 loss 训练，权重分别为 0.1，1 和 500。

## Experiments

### Adversarial Attack to SiamRPNpp

进行如下三组实验：

1. 仅攻击 search region
2. 仅攻击 template
3. 同时攻击 search region 和 template

### Ablation Study

#### Influence of Shrinking Loss

进行三组对比试验：

1. G-Template vs. G-Template-Regress
2. G-Search vs. G-Search-Regress
3. G-Template-Search vs. GTemplate-Search-Regress

结论：shrinking loss 有助于攻击 search regions，但对攻击 template 可能有害。

#### Influence of a Discriminator

并未进行实验，只是说明，不使用 discriminator，对抗样本的扰动也是难以察觉的。

### Further Discussions

#### Noise Pattern

如图 10 所示，扰动主要集中在被跟踪的目标上，而其他区域几乎不受扰动。

<img src="https://i.loli.net/2020/05/03/ALdcw79a1touTHe.png" alt="image-20200503101605838" style="zoom:50%;" />