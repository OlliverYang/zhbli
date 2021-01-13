---
title: >-
  [ECCV2020] SPARK: Spatial-aware Online Incremental Attack Against Visual
  Tracking
date: 2020-08-15 14:02:58
tags:
- Adversarial Attack
- Tracking
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

##  Spatial-aware Online Adversarial Attack

### Problem Definition

$V=\{X_t\}^T_1$ 是有T帧的视频。$\textbf T$ 表示目标模板。目标跟踪器为：$OT(X_t, \textbf T)$。

在帧t中有N个候选框，跟踪器为每个候选框i预测一个边框$b^i_t$和该框对应的得分$t^i_t$。

### Basic Attack

我们首先通过在每帧采用现有的对抗方法来提出基本攻击。为了攻击跟踪器 $OT(\cdot)$，可以使用另一个跟踪器 $OT'(\cdot)$ 来生成对抗样本。寻找对抗样本的方式如下：

<img src="https://i.loli.net/2020/08/15/nDJr5oh8EigOyVY.png" alt="image-20200815140628090" style="zoom:50%;" />

其中$E_t$表示扰动。D表示距离。第一行的含义是希望扰动尽量小。当 $OT=OT'$是，就是白盒攻击。

为了执行Untargeted Attack (UA)，设计如下目标函数：

<img src="https://i.loli.net/2020/08/15/bgdKwX1LcMG4Jfi.png" alt="image-20200815142208120" style="zoom:50%;" />

含义是：真实框的得分要比错误框的得分低。

### Online Incremental Attack

据上述基本攻击的实验结果发现，直接攻击每个帧是无效的。由于相邻帧非常相似，因此如何有效地利用前一帧的扰动却又不被察觉，这是个问题。一种简单的方法是将先前的扰动添加到新的扰动中，这将增加攻击的成功率，但会导致严重的失真。为了解决此问题，本文提出 spatial-aware online incremental attack (SPARK)。SPARK的公式为：

<img src="https://i.loli.net/2020/08/15/KTwBPzMFchS6EAN.png" alt="image-20200815143049319" style="zoom:50%;" />

其中$E_{t-1}$是上一帧的扰动，$\epsilon _t$ 是增量扰动。目标函数为：

<img src="https://i.loli.net/2020/08/15/EK1r4b9wcdJOqGC.png" alt="image-20200815143328866" style="zoom:50%;" />