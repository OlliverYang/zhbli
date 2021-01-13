---
title: '[arXiv1804] Adversarial Attacks and Defences Competition'
date: 2020-04-25 15:03:00
tags:
---

## Abstract

Google Brain 组织了 NIPS 2017 competition，鼓励开发生成对抗样本的新方法，同时鼓励开发相应的防御方法。本文介绍了竞赛的结构和组织，以及一些解决方案。

##  Adversarial examples

###  Common attack scenarios

可能的对抗攻击场景可以从不同的角度分类。

首先，可以按照攻击的目的分类：

- Non-targeted attack：对抗的目的是预测任何一个不正确的标签即可。
- Targeted attack：预测一个指定的类别。

其次，还可以按照 adversary 对模型的了解程度进行分类：

- White box：了解模型的所有信息，包括模型类型，模型结构，模型参数。
- Black box with probing：不了解模型，但可以对模型进行查询：提供输入，观察输出。
- Black box without probing：不了解模型的任何信息。

第三，可以按将数据送入模型的方式分类：

- Digital attack：可以直接将入 float32 等的数据送入网络。
- Physical attack：仅能通过相机等的结果作为网络的输入。

### White box digital attacks

#### L-BFGS

优化如下损失：

<img src="https://i.loli.net/2020/04/25/6CnkrEtd8cebFXZ.png" alt="image-20200425153241406" style="zoom:50%;" />

缺点：相当慢。	

#### Fast gradient sign method (FGSM)

<img src="https://i.loli.net/2020/04/25/81UQfdlvGbKcPR2.png" alt="image-20200425153619577" style="zoom:50%;" />

扩展： Basic Iterative Method (BIM) 或称作 Iterative FGSM (I-FGSM)：

<img src="https://i.loli.net/2020/04/25/UYhWg3P7bAJ14TK.png" alt="image-20200425153644273" style="zoom:50%;" />

BIM 可轻松扩展为 target attack，称作 Iterative Target Class Method：

<img src="https://i.loli.net/2020/04/25/NoyH9JOXaE2YFLw.png" alt="image-20200425153710879" style="zoom:50%;" />

> [23] A. Kurakin, I. Goodfellow, and S. Bengio. **Adversarial examples in the physical world**. In ICLR’2017 Workshop, 2016.

#### Madry et. al's Attack

通过选择 $\varepsilon$ norm ball 内的随机点最为 starting point，可显著改善 BIM。这种攻击通常称为 projected gradient descent（PGD）。

> [27] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and A. Vladu. **Towards deep learning models resistant to adversarial attacks**. In ICLR, 2018.

#### Carlini and Wagner attack (C&W)

对 L-BFGS 的改进。

<img src="https://i.loli.net/2020/04/25/mOI1LSUPHRxnlVC.png" alt="image-20200425154340241" style="zoom:50%;" />

> [6] N. Carlini and D. Wagner. Towards evaluating the robustness of neural networks. IEEE Symposium on Security and Privacy, 2017.

#### Adversarial transformation networks (ATN)

训练生成模型来制作对抗样本。优点是，如果生成模型很小，则比显式优化算法更快生成对抗样本，甚至比 FGSM 更快。

> [1] S. Baluja and I. Fischer. Adversarial transformation networks: Learning to generate adversarial examples. 2017.

