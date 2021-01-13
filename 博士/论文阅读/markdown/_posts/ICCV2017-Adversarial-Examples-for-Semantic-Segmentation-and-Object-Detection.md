---
title: '[ICCV2017] Adversarial Examples for Semantic Segmentation and Object Detection'
date: 2020-08-24 13:35:30
tags:
- Adversarial Attack
- ICCV2017
- Image Segmentation
- Object Detection
mathjax: true
---

##  Generating Adversarial Examples

### Dense Adversary Generation

定义X是图像，包含N个 recognition targets $T=\{t_1,...,t_N\}$。每个target $t_n$ 具有一个类别标签 $l_n\in \{1,2,...,C\}$。

定义 $f(X,t_n)\in R^C$ 为 $t_n$ 的分类得分向量（在softmax之前）。我们希望预测出错：

<img src="https://i.loli.net/2020/08/24/CZkFrjh29e6pHLX.png" alt="image-20200824153856337" style="zoom:50%;" />

为此，我们需要指定 adversarial label $l'_n$，从错误类别中随机选择：

<img src="https://i.loli.net/2020/08/24/8HSrZ137cwpxKuj.png" alt="image-20200824154038869" style="zoom:50%;" />

损失函数为：

<img src="https://i.loli.net/2020/08/24/1JqW7iXAzVHuOnR.png" alt="image-20200824154133124" style="zoom:50%;" />

我们采用梯度下降法来优化。假设m次迭代后的图像为$X_m$，我们收集正确预测的 targets，即 active target set：

<img src="https://i.loli.net/2020/08/24/oSLYEcHjp5P7G2R.png" alt="image-20200824154712127" style="zoom:50%;" />

然后计算梯度，并累加所有扰动：

<img src="https://i.loli.net/2020/08/24/Cx3jMJi4X8Wkosp.png" alt="image-20200824154814598" style="zoom:50%;" />

### Selecting Input Proposals for Detection

DAG算法的一个关键问题是选择 target 集合 T。对于图像分割而言，这相对容易，因为我们要对所有像素都进行错误分类。因此可以把每个像素点视为一个target。

对于目标检测而言，target的选择困难的多。因为可能的targets的总量（即proposals）比分割中targets的数量要多得多。一个简单的策略是使用由RPN生成的proposals，但是实验发现对于扰动图像，会生成一组新的proposals，而这些proposals会被正确分类。

为了解决这一问题，我们通过提高RPN中的NMS阈值，使得proposals非常密集，这可以使得每幅图片的proposals从300增加到3000。使用这一更加密集的target set T，这样的话，真实目标边框距离proposals会很近，因此会被分类错误。实验证明，对抗扰动的作用与候选框的数量呈正相关。