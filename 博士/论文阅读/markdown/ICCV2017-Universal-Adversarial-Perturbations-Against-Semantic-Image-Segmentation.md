---
title: >-
  [ICCV2017] Universal Adversarial Perturbations Against Semantic Image
  Segmentation
date: 2020-08-21 11:25:51
tags:
- ICCV2017
- Image Segmentation
- Adversarial Attack
mathjax: true
---

## Background

定义$f_\theta$是参数为$\theta$的神经网络，x是$f_\theta$的输入图像。$f_\theta(x)$是$f_\theta$的输出，即条件概率$p(y|x,\theta)$，编码为 class probability vector。$y^{true}$是ground truth target，即 one hot encoding of the class。令$J_{cls}(f_\theta(x),y^{true})$是分类损失，如交叉熵。

### Adversarial Examples

定义$\xi$是对抗扰动，对抗样本为$x^{adv}=x+\xi$。

## Adversarial Perturbations Against Semantic Image Segmentation

对于图像语义分割，损失是所有空间位置$(i,j)\in I$的和：

<img src="https://i.loli.net/2020/08/21/rVRG3c7TNx98bYd.png" alt="image-20200821114028688" style="zoom:50%;" />

希望网络的预测能接近$y^{target}$。接下来讨论如何选择$y^{target}$。

### Adversarial Target Generation

原则上，$y^{target}$的选择可以是任意的。但是，不能依赖$y^{true}$得到$y^{target}$，因为我们不知道$y^{true}$。因此，可以依赖$y^{pred}$得到$y^{pred}$。

希望$y^{pred}$和$y^{target}$大体上是相似的，只是隐藏一些重要的目标。

#### Static target segmentation

对于一段视频序列，将第一帧的$y^{pred}$定义为后续所有帧的$y^{target}$。该方式适用于如下情况：希望攻击静态摄像机，隐藏特定时间段内的可以活动。

#### Dynamic target segmentation

对于运动场景，希望$y^{pred}$和$y^{target}$大体上是相似的，只是隐藏一些重要的目标。定义$o$是希望隐藏的类别，$I_o=\{(i,j)|f_\theta(x_{ij}=o)\}, I_{bg}=I \backslash I_o$。隐藏方式为替换为附近区域的类别。

### Image-Dependent Perturbations

对抗目标为：

<img src="https://i.loli.net/2020/08/21/SdpwfnDEBUzP1Yq.png" alt="image-20200821115810284" style="zoom:50%;" />

优化方法为：

<img src="https://i.loli.net/2020/08/21/DuMHXfpG52wEnyt.png" alt="image-20200821115946591" style="zoom:50%;" />

由于隐藏特定目标更重要，所以为不同区域施加不同权重：

<img src="https://i.loli.net/2020/08/21/zN2gI3vGm6d9KSO.png" alt="image-20200821120117519" style="zoom:50%;" />

另一个问题是，不同像素点之间的梯度可能是相反的，因此存在竞争关系。标准的交叉熵损失通常会鼓励已经分对的预测置信度更高。这在分类任务中不存在问题，因为只有一个 target output。为此，我们对于置信度超过0.75的损失设为0。

### Universal Perturbations

我们在m个训练输入$D^{train}=\{(x^{(k)}, y^{target,k})\}_{k=1}^m$上生成通用对抗扰动Ξ。我们希望该扰动可以泛化到测试图像x上，而且x没有target $y^{target}$。优化函数为：

<img src="https://i.loli.net/2020/08/21/lYvDsXMcGE3yAda.png" alt="image-20200821122041831" style="zoom:50%;" />

这个方法的一个潜在问题是过度拟合训练数据。我们采用相对简单的正则化方法：使Ξ在两个空间维度上都是周期性的：

<img src="https://i.loli.net/2020/08/21/MGC3eih7wlgDBdV.png" alt="image-20200821122951632" style="zoom:50%;" />

因此需要在所有训练数据和所有tiles上计算梯度：

<img src="https://i.loli.net/2020/08/21/BnSbPXjruVDIw9d.png" alt="image-20200821123500699" style="zoom:50%;" />