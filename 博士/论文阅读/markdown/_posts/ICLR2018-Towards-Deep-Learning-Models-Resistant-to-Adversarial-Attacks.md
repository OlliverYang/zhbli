---
title: '[ICLR2018] Towards Deep Learning Models Resistant to Adversarial Attacks'
date: 2020-05-09 09:56:55
tags:
- ICLR2018
mathjax: true
---

## Abstract

最近的工作表明：

- 神经网络易受对抗样本攻击。
- 对抗攻击的存在可能是深度学习模型的固有弱点。

本文通过 robust optimization 的角度研究神经网络的 adversarial robustness。

## Introduction

本文提出如下贡献：

1. 对于 saddle point formulation 对应的 optimization landscape 进行仔细研究。尽管其组成部分具有 non-convexity 和 non-concavity，但我们发现优化问题是可以解决的。本文提供了有力的证据，证明一阶方法可以可靠地解决此问题。

2. 本文探索了网络架构对 adversarial robustness 的影响，发现 model capacity 具有重要作用。为了可靠地抵抗强大的 adversarial attacks，model capacity 需要更大。这表明，saddle point problem 的 robust decision boundary 可能比仅将良性数据点分开的 decision boundary 要复杂得多。
3. 通过优化 saddle point formulation，并使用 PGD 作为可靠的 first-order adversary，训练了 robust models。