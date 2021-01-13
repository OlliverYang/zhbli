---
title: '[ECCV2020] Robust Tracking against Adversarial Attacks'
date: 2020-08-14 13:14:23
tags:
- ECCV2020
- Tracking
- Adversarial Attack
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## Proposed Algorithm

### Adversarial Example Generation

根据跟踪器的 input frame 和 output response（classification scores / regression maps）生成对抗扰动，然后将这些扰动添加到输入帧中，以生成对抗样本。

$I$ 表示输入图像，$N$ 表示 **proposal number**，$L_c$ 表示二值分类损失，$L_r$ 表示边框回归损失，$p_c$ 表示分类标签，$p_r$ 表示回归标签，$S^{t-1}$ 表示上一帧的跟踪结果，$S^1$ 表示第一帧的真实框。原始的跟踪损失为：

<img src="https://i.loli.net/2020/08/14/Lb5tyG3QVKXBgOn.png" alt="image-20200814132630112" style="zoom:50%;" />

其中 $I_n$ 是图像中的一个 proposal。

为了生成对抗扰动，我们希望 CNN 做出错误预测。我们创建伪分类标签 $p_c^*$ 和伪回归标签 $p_r^*$。对抗损失的目标是，不论使用真实标签还是伪标签，$L_c$ 和 $L_r$ 都相同：

<img src="https://i.loli.net/2020/08/14/uvYRcZ3j2KsQX8k.png" alt="image-20200814133314604" style="zoom:50%;" />

#### 伪标签的设定

对于 $p^*_c$，我们反转 $p_c$ 的值，以迷惑分类分支。

对于 $p^*_l$，我们在 $p_l$ 上添加随机的位置/尺度扰动。

#### 对抗样本的计算

计算了对抗损失后，我们取对抗损失相对于输入图像的偏导，并迭代N次获得最终的对抗扰动：

<img src="https://i.loli.net/2020/08/14/9uqF7RNBaislj5U.png" alt="image-20200814133902070" style="zoom:50%;" />

#### 时空域的对抗攻击

将上一帧的对抗扰动加到当前帧上：

<img src="https://i.loli.net/2020/08/14/RskJi9xf1dNw8rL.png" alt="image-20200814134220211" style="zoom:50%;" />

### Adversarial Defense

我们估计扰动，并从输入图像中减去扰动。

给定带有未知对抗扰动的输入图像 $I$，我们首先根据 $S^{t-1}$ 生成正确标签和伪标签。随后计算偏导并应用于输入图像：

<img src="https://i.loli.net/2020/08/14/KU5PqjtyhAzkaYi.png" alt="image-20200814135659458" style="zoom:50%;" />

我们仍将上一帧的对抗扰动转移到当前帧上：

<img src="https://i.loli.net/2020/08/14/E3SZnbdyoPaMgU9.png" alt="image-20200814135752557" style="zoom:50%;" />