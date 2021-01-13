---
title: '[CVPR2019] Searching for A Robust Neural Architecture in Four GPU Hours'
date: 2020-05-09 19:43:54
tags:
- CVPR2019
mathjax: true
---

## Abstract

传统的 neural architecture search (NAS) 基于强化学习或进化策略，需要超过 3000 GPU 小时才能在 CIFAR-10 上找到好的模型。

本文提出一种有效的 NAS 方法，以学习通过梯度下降进行搜索。我们的方法将搜索空间表示为有向无环图（DAG）。该 DAG 包含数十亿个子图，每个子图表示一种神经体系结构。为了避免遍历子图的所有可能性，我们在 DAG 上开发了可微分的采样器。该采样器是可学习的，在 sampled architecture 上训练后，通过 validation loss 进行优化。通过这种方式，我们的方法可以通过梯度下降以端到端的方式进行训练，本文的方法称为 Gradient-based search using Differentiable Architecture Sampler (GDAS)。

性能：

- https://github.com/D-X-Y/NAS-Projects
- 在 CIFAR-10 上使用 4 个 GPU 小时完成 one searching procedure，所发现的模型测试误差为 2.82%，参数量仅为 2.5M，与最好水平相当。