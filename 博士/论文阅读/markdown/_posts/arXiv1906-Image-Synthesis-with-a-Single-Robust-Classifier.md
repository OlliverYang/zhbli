---












title: '[arXiv1906] Image Synthesis with a Single (Robust) Classifier'
date: 2020-05-07 16:37:59
tags:
mathjax: true
---

## Abstract

本文证明，仅使用基本的分类框架就能解决一些最具挑战性的图像合成任务。与其他最新方法相比，我们的方案很简单：为所有任务使用单个开箱即用分类器。我们方法的关键是，我们训练的分类器是 adversarially robust 的。

事实证明，adversarial robustness 正是我们直接操纵输入的显著特征所需要的。

本文证明，仅使用基本的分类器就能解决各种 image synthesis 任务：generation、inpainting、image-to-image translation、super-resolution、interactive image manipulation。

我们的整个方法都基于单个分类器，并涉及执行简单的输入操作：通过梯度下降最大化 predicted class scores。

本文方法的关键是使用 adversarially robust classifiers。[Tsi+19] 观察到，最大化 robust models 的损失会生成其他类别的 realistic instances。本文充分利用这一点构建用于图像合成的多功能工具包。注意，所用的网络仅被训练用于图像分类。

> [Tsi+19] Dimitris Tsipras et al. “Robustness May Be at Odds with Accuracy”. In: International Conference on Learning Representations (ICLR). 2019.

## Robust Models as a Tool for Input Manipulation

[Tsi+19] 观察到，在  (adversarially) robust classifier 中优化图像使得分类错误，会引入错误类别的显著特征。这一属性是 robust classifier 共有的，standard models（使用 empirical risk minimization (ERM) 训练）固有的脆弱，并且预测对于输入中不可察觉的变化也很敏感。

Adversarially robust classifiers 使用 robust optimization objective 训练，而不是最小化数据的 expected loss $\mathcal L$（公式 1）：

<img src="https://i.loli.net/2020/05/07/japdbG2WKQYIi4D.png" alt="image-20200507172126566" style="zoom:50%;" />

我们在特定 perturbation set $\Delta$ 上最小化 worst case loss（公式 2）：

<img src="https://i.loli.net/2020/05/07/NroIMZPLjaVfpA7.png" alt="image-20200507172332072" style="zoom:50%;" />

通常，集合 $\Delta$ 捕获了不可察觉的变化。给定 $\Delta$，可以使用对抗训练解决公式 2。

从一个角度看，我们可以将 robust optimization 视为将先验编码到模型中，从而防止模型依赖于输入的 imperceptible features。通过鼓励模型对小的扰动保持不变，可以保证 model’s predictions 的改变对应于 salient input changes。

事实证明，当我们针对 robust model 最大化特定类别的概率时，也会出现这种现象。这表明 robust models 表现出更多的  human-aligned gradients。更重要的是，仅通过对 model output 执行梯度下降就可以精确控制输入的特征。

## Leveraging Robust Models for Computer Vision Tasks

### Realistic Image Generation

生成过程基于基于最大化 desired class 的 class score。最大化的目的是在给定的输入图像中添加与该类相关的、在语义上有意义的特征。

该方法先前已在 standard models 上，结合 domain-specific input priors，用于执行 class visualization，即合成每个类的 prototypical inputs。

由于此过程是确定性的，因此生成多样化的样本集需要使用随机种子作为最大化过程的起点。形式上，要生成 $y$ 类的样本，需要对采样一个种子并最小化标签 $y$ 的损失 $\mathcal L$：

<img src="https://i.loli.net/2020/05/07/LoEqz8CQgDV1Hx4.png" alt="image-20200507180702292" style="zoom:50%;" />

![image-20200507181212275](https://i.loli.net/2020/05/07/DcyqVPQdszeirWl.png)

其中 $\mathcal G_y$ 指 class-conditional seed distribution。

使用 targeted PGD，可以生成多样且逼真的图像。

### Inpainting

我们优化图像，以最大化真正类别的得分，同时迫使生成的图像与原始图像在未损坏区域的内容保持一致：

<img src="https://i.loli.net/2020/05/07/BmakM8O1dp4ZAlf.png" alt="image-20200507190511616" style="zoom:50%;" />

使用 PGD 进行优化。

### Image-to-Image Translation

略。

### Super-Resolution

略。

### Interactive Image Manipulation

略。