---
title: '[arXiv2004] Learning Gaussian Maps for Dense Object Detection'
date: 2020-05-13 13:35:59
tags:
- Object Detection
mathjax: true
---

## Our Approach

将目标视为 2D 高斯，峰值位于目标。

我们将 UNet 添加到 RetinaNet baseline 中。并在输出高斯图上添加额外的均方损失，进行多任务学习。

<img src="https://i.loli.net/2020/05/13/nupZVdM6hSyeXrs.png" alt="image-20200513134124853" style="zoom:50%;" />