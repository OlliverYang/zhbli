---
title: >-
  [AAAI2020] Real-Time Object Tracking via Meta-Learning: Efficient Model
  Adaptation and One-Shot Channel Pruning
date: 2020-05-07 09:50:20
tags:
- AAAI2020
- Tracking
mathjax: true
categories:
- [Tracking, Model Update]
- [Tracking, Meta-Learning]
---

## Abstract

本文提出用于实时目标跟踪的元学习框架，用于 model adaptation 和 channel pruning。

给定一个目标跟踪器，该框架在跟踪过程中学习仅通过几次梯度下降来迭代微调模型参数，同时在第一帧使用 ground-truth 对网络通道进行修剪。

这样的学习问题被表述为元学习任务。通过精心设计的跟踪模拟，更新 meta-parameters 的初始权重、学习率和 pruning masks 来训练 meta-tracker。

Meta-tracker 通过加快在线学习的收敛速度，以及减少特征计算的成本，提高了跟踪的性能。

## Introduction

元学习通过对大量 episodes 进行 evaluation，可以自动对学习问题进行优化。它有助于探索大的假设空间，并使学习算法拟合特定的任务集。

考虑到目标跟踪算法旨在专门针对特定视频学习 parameterized target appearance model，因此采用元学习来有效优化跟踪算法是自然的。

在基于 CNN 的目标跟踪中，episode 对应于：基于一段视频序列的 parameterized model 的目标跟踪的 realization。

Episode 的 execution 在计算上是昂贵耗时的，这使得将元学习纳入目标跟踪变得很困难，因为需要对大量的 learning episodes 进行优化。

Meta-Tracker (Park and Berg 2018) 通过在单帧中模拟 tracking episode 来克服此问题。但是，在这种方法中，元学习仅限于使用第一帧对网络进行初始化，用于目标表观建模。这是因为 Meta-Tracker 仅依赖准确的 ground-truth 进行 meta-learning。

> [Park and Berg 2018] Park, E., and Berg, A. C. 2018. MetaTracker: Fast and Robust Online Adaptation for Visual Object Trackers. ECCV.

本文提出了的元学习框架着重于快速进行 model adaptation，将 model adaptation 分成两部分来模拟 model adaptation：

1. initial adaptation：在第一帧针对 one-shot target ground-truth 进行模型优化。
2. online adaptation：使用先前帧的跟踪目标进行模型更新。

这种细粒度的模拟能够捕获两种情况的不同属性，并使 meta-learned model 的泛化性更强。

在本文应用于跟踪的 meta-learning 中，通过使用 hard examples 模拟各种挑战性场景，根据 expected accuracy 评估学习算法。

此外，本文通过基于第一帧的 single ground-truth target annotation 的元学习，开发了one-shot channel pruning 技术。

## Meta-learning for Fast Adaptation

<img src="https://i.loli.net/2020/05/07/ZRVcHYlPQeEht6q.png" alt="image-20200507110448328" style="zoom:50%;" />

### Objective

`Model adaptation` 的训练数据收集自先前帧的跟踪结果。

公式 1：

<img src="https://i.loli.net/2020/05/07/exbnEck1lFiXW6J.png" alt="image-20200507113410960" style="zoom:50%;" />

### Tracking Simulation

由于超参数是基于 tracking simulation 进行元学习的，因此在训练时构造 realistic simulations 对于元学习算法的泛化至关重要。

典型的目标跟踪算法考虑两种类型的 model adaptation：

1. initial adaptation：在第一帧针对 one-shot target ground-truth 进行模型优化。
2. online adaptation：使用先前帧的跟踪目标进行模型更新。

这两者的主要区别在于学习过程中使用的 ground-truth labels。本文在 tracking simulation 中考虑了这一点，并在元学习期间为每个 adaptation 使用不同的数据集。

令 $\Gamma$ 为 training video set，$\mathcal V\in \Gamma$ 是一段具有  tracking ground-truth 的 annotated video。

将 tracking aimulation 定义为，针对 $\mathcal V$ 中被标注的目标，在元学习中的 initial adaptation、online adaptation、test dataset construction 序列。

与标准的目标跟踪（旨在估计每帧中的目标）不同，tracking simulation 仅对从 $\mathcal V$ 中人工生成的数据集执行单词 initial adaptation 和单次 online adaptation。我们将 tracking simulation 称为 episode 或 simulated tracking episode。

Simulated tracking episode 的第一步是 initial adaptation。通过优化公式 1，使用 initial dataset $\mathcal D_{\text{init}}$ 学习模型参数，其中 $\mathcal D_{\text{init}}$ 来自于在从 $\mathcal V$ 中采样的帧的 target ground-truth annotation。

然后，使用更新后的模型参数估计从 $\mathcal V$ 中采样的 unseen frames 中的 target states。Estimated targets 用于构建用于 online model adaptation 的 online dataset $\mathcal D_{\text{on}}$。Online adaptation 使用 noisy labels 模拟 model adaptation。注意，在 initial/online adatations 中对公式 1 的优化是以在元学习中学习的超参数为指导的。

最后一步是收集测试数据集 $\mathcal D_\text{test}$ 进行元训练。定义 test loss 和 meta-optimization loss，这是我们的元学习的目标函数。注意，$\mathcal D_\text{test}$ 是从 $\mathcal V$ 中的 ground-truth annotations 中获得的，并用从训练集 $\Gamma-\{\mathcal V\}$ 中所有其他 annotated videos 中收集的负样本进行扩充。

一个 simulated tracking episode 产生一组 collected datasets 和与该 episode 有关的一系列中间模型参数。这种信息——数据集和参数——被称为 episode trajecory，用 $\tau^1$ 表示。元学习的目标函数定义为多个 episodes 的 trajectories，其中每个 episode 都基于一段 annotated video $\mathcal V\in \Gamma$。我们基于此目标函数优化超参数。

#### Meta-parameters

Meta-parameter $\mathcal M$ 是通过我们的元学习方法优化的一组超参数。元学习的主要目标是降低计算成本并保持准确性，$\mathcal M$ 通过对基于梯度的 model adaptation 过程进行复杂控制，以实现计算量和性能之间的平衡。

我们将 $\pmb \theta^0_\text{init}\in \mathbb R^d$ 视为超参数。此外，我们将传统的标量学习率扩展为 per-parameter 和 per-iteration 学习率向量，用于 initial adaptation $\mathcal A_\text{init}=\{\pmb \alpha^k_\text{init}\in \mathbb R^d\}^{K_\text{init}}_{k=1}$ 和 online adaptation $\mathcal A_\text{on}=\{\pmb \alpha^k_\text{on}\in \mathbb R^d\}^{K_\text{on}}_{k=1}$，从而将学习率视为超参数。其中 $K_\text{init}$ 和 $K_\text{on}$ 分别表示用于 initial/online adaptation 的梯度下降迭代次数。

Meta-parameter 是所有超参数的集合：$\mathcal M=\{\pmb \theta^0_\text{init}, \pmb A_\text{init}, \pmb A_\text{on}\}$。

#### Initial adaptation

Initial adaptaion 使用的数据集是 $\mathcal D_\text{init}$，该数据集基于从一段 annotated video $\mathcal V$ 中均匀采样的一帧及对应的 ground-truth annotation 创建。

$\mathcal D_\text{init}$ 包含与 ground-truth annotation 具有较高重叠的正样本，和没有较高重叠或不重叠的负样本。

我们使用 SGD 执行 $K_\text{init}$ 次迭代，使用公式 1 优化模型参数 $\pmb \theta^0_\text{init}$。

经过 initial adaptation 的模型参数为 $\pmb \theta^{K_\text{init}}_\text{init}$。

#### Online Adaptation

Online Adaptation 使用的数据集是 $\mathcal D_\text{on}$，数据集的收集策略与 $\mathcal D_\text{init}$ 相同，只是使用了 estimated targets。

我们使用 SGD 执行 $K_\text{on}$ 次迭代，使用公式 1 优化模型参数 $\pmb \theta^{K_\text{init}}_\text{init}$。

经过 online adaptation 的模型参数为 $\pmb \theta^{K_\text{on}}_\text{on}$。