---
title: '[CVPR2018] Squeeze-and-Excitation Networks'
date: 2020-05-10 20:09:31
tags:
- CVPR2018
mathjax: true
---

<img src="https://i.loli.net/2020/05/10/R2ofU953wTZQeAb.png" alt="image-20200510201500197" style="zoom:50%;" />

![image-20200510202104414](https://i.loli.net/2020/05/10/5dCOXRLBe6bKcvW.png)

Squeeze 操作生成通道描述符，具有全局感受野。使用全局平均池化实现。

$r=16$ 为 reduction ratio。

$\text F_{scale}$ 为 channel-wise multiplication。