---
title: '[arXiv1806] DPatch: Attacking Object Detectors with Adversarial Patches'
date: 2020-08-24 16:39:12
tags:
- Adversarial Attack
- Object Detection
mathjax: true
---

## Proposed Approach

### DPATCH Formulation

#### Original Adversarial Patch

由 Google (Brown et al. 2017) 提出的对抗补丁希望当在图像中贴上补丁时，可以最大化CNN分类器的损失：

<img src="https://i.loli.net/2020/08/24/oimJAGzfpNUTqy4.png" alt="image-20200824164337943" style="zoom:50%;" />

其中A(P,x,l,t)表示在原始图像x的位置l上以变换t应用补丁P后的图像。$Pr(\hat y|A)$是分类器把A分为正确类别$\hat y$的概率。

> Brown, T. B.; Man, D.; Roy, A.; Abadi, M.; and Gilmer, J. 2017. **Adversarial patch**. arXiv preprint arXiv:1712.09665.

#### Adversarial Patch on Object Detectors

对于 untargeted attack，我们希望寻找一个补丁$\hat P_u$，希望将该补丁按照 apply function A 的方式应用到图像x后，可以最大化检测器相对于真实类别标签$\hat y$和真实边框$\hat B$的损失。

对于 targeted attack，希望寻找补丁 $\hat P_t$，最小化到指定类别$y_t$和指定边框$B_t$的损失。

<img src="https://i.loli.net/2020/08/24/fVh2q1SXnCca56w.png" alt="image-20200824165301671" style="zoom:50%;" />