---
title: '[arXiv2005] How to Train Your Energy-Based Model for Regression'
date: 2020-05-06 15:58:43
tags: Tracking
mathjax: true
categories:
- [Tracking, Loss]
---

## Abstract

`Energy-based models` (EBMs) 在计算机视觉中越来越流行。尽管常用于 generative image modeling，但最近的工作将 EBMs 用于回归任务，并在目标检测和目标跟踪中达到了最好的性能。然而，训练 EBMs 具有挑战性。尽管已经探索了不同的技术来进行 generative modeling，将 EBM 应用于回归不是一个充分研究的问题，因此尚不清楚如何训练 EBMs 以获得最佳的回归性能。本文首次对该问题进行详细研究。

本文提出 noise contrastive estimation 的扩展方法，并与六个 1D 回归/目标检测方法进行了性能比较。比较结果表明，本文提出的训练方法最好。

性能：

- https://github.com/fregu856/ebms_regression

- LaSOT_AUC：63.7%。
- TrackingNet_Success：78.7%。

## Introduction

EBMs 通过参数化 scalar function $f_\theta(x)$ 来执行概率密度：

<img src="https://i.loli.net/2020/05/06/gPLJZYyFAuiQX4d.png" alt="image-20200506162716258" style="zoom:50%;" />

最近的工作探索了 conditional EBMs 用于回归的一般公式，在目标检测和目标跟踪上表现出色。

给定观测到的 input-target pairs，回归需要从 input $x$ 预测 continuous target $y$。

在 [15, 9] 中，通过学习 conditional EBM $p(y|x;\theta)$，在给定 input $x$ 的情况下捕获 target value $y$ 的分布，解决了这一问题。测试时，使用梯度上升最大化 $p(y|x;\theta)$ w.r.t. $y$，产生准确的预测。

> [15] Fredrik K Gustafsson, Martin Danelljan, Goutam Bhat, and Thomas B Sch¨on. **Learning deep conditional target densities for accurate regression**. arXiv preprint arXiv:1909.12297, 2019.
>
> [9] Martin Danelljan, Luc Van Gool, and Radu Timofte. **Probabilistic regression for visual tracking**. In The IEEE Conference on Computer Vision and Pattern Recognition (CVPR), June 2020.

本文详细研究使用 EBMs 进行回归，以进一步提高性能。

EBMs 的训练具有挑战性，因为计算 $p(x;\theta)$ 设计棘手的积分，这使得使用  standard maximum likelihood (ML) 的学习变得复杂。虽然在 generative modeling 中探索了多种技术，包括 alternative estimation methods 和 approximations based on Markov chain Monte Carlo (MCMC)。但是，EMBs 在回归中的应用并未深入研究。[15, 9] 都将  Monte Carlo importance sampling 应用于近似 intractable integrals，这种方法在数据维数方面很难扩展。因此，如何训练 EMSs $p(y|x;\theta)$ 以在计算机视觉的回归任务上获得最佳性能，是本文研究的内容。

本文的贡献是：提出了一种 noise contrastive estimation (NCE) 的扩展，以训练用于回归任务的 EBMs。本文提出的 NCE+ 可以理解为 NCE 的直接推广，考虑了真实数据集注释过程中的噪声。

本文将 NCE+ 应用于目标跟踪任务，取得了良好的性能。

## Energy-Based Models for Regression

###  Problem & Model Definition

在有监督回归问题中，定义 $\mathcal D$ 为独立同分布的 input-target pairs，$\mathcal D = \{(x_i,y_i)\}^N_{i=1}, (x_i,y_i) \sim p(x,y)$。给定输入 $x^*\in \mathcal X$，任务是学习如何预测 target $y^*\in \mathcal Y$。Target Space $\mathcal Y$ 是连续的，当 $K\ge1$ 时，$\mathcal Y\in\mathbb R^K$。输入空间 $\mathcal X$ 通常对应于图像空间。

与 [15, 9] 一样，我们通过创建 conditional target density $p(y|x)$ 的 `energy-based model` $p(y|x;\theta)$ 来解决这一问题。为此，本文使用模型参数 $\theta\in \mathbb R^P$ 来指定 DNN $f_\theta:\mathcal X\times\mathcal Y\rightarrow \mathbb R$。该 DNN 直接映射任何 input-target pair $(x,y)\in\mathcal X\times\mathcal Y$ 到 标量 $f_\theta(x,y)\in \mathbb R$。Conditional target density 的模型 $p(y|x;\theta)$ 定义为（公式 1）：

<img src="https://i.loli.net/2020/05/06/sjDdXwQvE5CRimL.png" alt="image-20200506205541087" style="zoom:50%;" />

### Training

为了训练 EBM $p(y|x;\theta)$ 中的 DNN $f_\theta(x,y)$，可采用不同的技术将 density $p(y|x;\theta)$ 拟合到观测数据 $\{(x_i,y_i)\}_{i=1}^N$。一般来说，最常用的此类技术可能是 ML learning，最小化 negative log-likelihood (NLL)：

<img src="https://i.loli.net/2020/05/06/sJnom5HPrvTE1zk.png" alt="image-20200506211357809" style="zoom:50%;" />

但是，公式中的积分很难处理。[15, 9] 使用 importance sampling 来近似这种 intractable integrals。

#### ML with Importance Sampling (ML-IS)

<img src="https://i.loli.net/2020/05/06/cU8HdE5xfvRT4pu.png" alt="image-20200506212132668" style="zoom:50%;" />

其中，$\{y^{(i,m)}\}^M_{m=1}$ 是从依赖于 ground truth target $y_i$ 的 proposal distribution $q(y|y_i)$ 中抽取的 $M$ 个样本。在 [15] 中，$q(y|y_i)$ 是以 $y_i$ 为中心的 $K$ 个等权重高斯的混合：

<img src="https://i.loli.net/2020/05/06/AYQsSjT3qm2cCat.png" alt="image-20200506213134796" style="zoom:50%;" />

#### KL Divergence with Importance Sampling (KLD-IS)

<img src="https://i.loli.net/2020/05/06/UoMVzx3h5L9ceAG.png" alt="image-20200506213401747" style="zoom:50%;" />

#### ML with MCMC (ML-MCMC)

<img src="https://i.loli.net/2020/05/06/F9Am5QlTqH7hyaX.png" alt="image-20200506214202806" style="zoom:50%;" />

#### Noise Contrastive Estimation (NCE)

作为 ML learning 的替代方法，[16] 提出 NCE 来估计 unnormalized parametric models：

<img src="https://i.loli.net/2020/05/06/HStlRrVAoNb6GZw.png" alt="image-20200506214512245" style="zoom:50%;" />

#### Score Matching (SM)

<img src="https://i.loli.net/2020/05/06/Y24hxyqQpuVMASj.png" alt="image-20200506214643665" style="zoom:50%;" />

#### Denoising Score Matching (DSM)

<img src="https://i.loli.net/2020/05/06/GVeXWRoCjZMLaFU.png" alt="image-20200506214806683" style="zoom:50%;" />

##  Proposed Training Method

本文提出了 NCE 的扩展：NCE+。

<img src="https://i.loli.net/2020/05/06/hxmLUJPj8i1kdfH.png" alt="image-20200506215145790" style="zoom:50%;" />

## Visual Tracking Experiments

<img src="https://i.loli.net/2020/05/06/ge7azCrPWKuL9hj.png" alt="image-20200506215238768" style="zoom:50%;" />