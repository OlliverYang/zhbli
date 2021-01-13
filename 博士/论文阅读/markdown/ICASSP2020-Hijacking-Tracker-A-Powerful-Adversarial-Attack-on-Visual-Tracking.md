---
title: >-
  [ICASSP2020] Hijacking Tracker: A Powerful Adversarial Attack on Visual
  Tracking
date: 2020-08-15 15:16:47
tags:
- Tracking
- Adversarial Attack
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## ATTACK METHODOLOGY

给定一个视频序列，我们的目的是将一个边框从真实目标位置劫持到错误位置$D(L_d,S_d)$。通过向视频帧中添加不起眼的扰动实现这一点。$L_d$ 表示D的位置，$S_d$表示D的形状。

具体来说，对于一个视频序列，设置劫持方向向量$\vec d$（指向$L_d$），和形状改变向量$\vec s$（指向$S_d$）。

### Loss Functions

对抗损失包括两部分：location loss 和 shape loss。具体来说，定义具有T个候选框的搜索区域为x。希望获得对抗扰动 $\Delta x$，使得预测框沿$\vec d$发生位置偏移，沿$\vec s$ 发生形状收缩。我们首先对T个候选框排序。然后，我们收集排名前5的confidence indexes set$I_c$，满足$\vec d$的top 5 location indexes set $I_{loc}$，满足$\vec s$的top 5 shape indexes set $I_{shape}$。

location loss 定义为：

<img src="https://i.loli.net/2020/08/15/6LDyl948UBorRq5.png" alt="image-20200815154036766" style="zoom:50%;" />

$S(\cdot)$ 表示 confidence score。上述公式的含义是，加了扰动后，具有错误位置的边框的得分高于真实目标框的得分。

<img src="https://i.loli.net/2020/08/15/JGc7pt9IATULYPu.png" alt="image-20200815154410627" style="zoom:50%;" />

上述公式的含义是，加了扰动后，具有错误形状的边框的得分高于真实目标框的得分。