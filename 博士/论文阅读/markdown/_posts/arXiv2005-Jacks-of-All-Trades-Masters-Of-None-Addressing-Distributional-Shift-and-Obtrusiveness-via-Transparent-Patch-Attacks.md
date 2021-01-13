---
title: >-
  [arXiv2005] Jacks of All Trades, Masters Of None: Addressing Distributional
  Shift and Obtrusiveness via Transparent Patch Attacks
date: 2020-05-09 10:41:43
mathjax: true
---

##  Abstract

本文专注于开发有效的 adversarial patch attacks，首次通过设计 semi-transparent patches，同时解决 attack success 和 obtrusiveness 的对立目标。这项工作的动机是对关于几何形变的 patch attack robustness 的系统性能分析。

本文阐释了：

- patch attack success 关键因素。
- 在 Expectation over Transformation (EoT) formalism 下，训练和测试/部署之间的 distributional shift 的影响。

通过将分析重点放在三种主要的转换类别（旋转/缩放/位置）上，我们的发现为有效的 patch attacks 的设计提供了 quantifiable insights，并证明了在所有因素中，尺度极大影响了 patch attack 的成功。

从这些发现出发，我们重点关注如何克服在实际物理环境中的 scale for the deployment of attacks 的主要限制——即 large patches 的 obtrusiveness。