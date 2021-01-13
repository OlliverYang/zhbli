---
title: '[ICCV2019] Physical Adversarial Textures That Fool Visual Object Tracking'
date: 2020-08-14 16:12:26
tags:
- ICCV2019
- Tracking
- Adversarial Attack
mathjax: true
categories:
- [Tracking, Adversarial Attack]
---

## Attacking Regression Networks

### Adversarial Strength

adversarial strength 定义为：

<img src="https://i.loli.net/2020/08/14/9pkm3tGP82iweJI.png" alt="image-20200814164004886" style="zoom:50%;" />

其中 $l_j$ 表示**预测的目标边框**，$\hat l_j$ 表示**真实目标边框**。$f^†$ 表示添加了对抗补丁的图像，$f$ 表示正常图像。A表示边框面积。

### Perceptual Similarity

#### Optimizing for Adversarial Behaviors

提出了几种对抗损失：

- non-targeted loss：使模型的训练损失最大化，如 FGSM，BIM。
- targeted losses：是模型到 adversarial target output 的损失最小化，如 JSMA。
- guided losses：介于上述两者之间。
- hybrid losses：上述损失的线性组合。

具体来说，我们考虑以下损失：

<img src="https://i.loli.net/2020/08/15/aNS9iZy2fbPrcoM.png" alt="image-20200815133718064" style="zoom:50%;" />

含义是：增加GOTURN的训练损失。

<img src="https://i.loli.net/2020/08/15/FE5fYwR4sOqbLt1.png" alt="image-20200815133819100" style="zoom:50%;" />

含义是：让预测边框固定到搜索区域的左下角。

<img src="https://i.loli.net/2020/08/15/sQJ4GuBf7Lk2Z9o.png" alt="image-20200815134019673" style="zoom:50%;" />

含义是：让预测边框固定到搜索区域的中心。

<img src="https://i.loli.net/2020/08/15/HdanhXjOoIiKgxQ.png" alt="image-20200815134110642" style="zoom:50%;" />

含义是：让预测边框变得最大。

<img src="https://i.loli.net/2020/08/15/UzkX1ZxH42BW5vQ.png" alt="image-20200815134200243" style="zoom:50%;" />

含义是：让预测边框尽量小。

<img src="https://i.loli.net/2020/08/15/oFUesn1BiMayGND.png" alt="image-20200815134341213" style="zoom:50%;" />

含义是：让预测边框尽量大。

总之，我们的攻击方法将 source texture $X_0$ 优化为 adversarial variant $X_i$，通过最小化如下损失实现：

<img src="https://i.loli.net/2020/08/15/CgJTmuZSERFhdlw.png" alt="image-20200815134757517" style="zoom: 50%;" />

texture 按如下方式更新：

<img src="https://i.loli.net/2020/08/15/gsN6SaOmqyiRtQL.png" alt="image-20200815134841124" style="zoom:50%;" />