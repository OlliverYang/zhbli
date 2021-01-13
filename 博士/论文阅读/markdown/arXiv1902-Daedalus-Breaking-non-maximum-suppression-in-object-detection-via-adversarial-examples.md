---
title: >-
  [arXiv1902] Daedalus: Breaking non-maximum suppression in object detection via
  adversarial examples
date: 2020-08-20 15:03:47
tags:
- Object Detection
- Adversarial Attack
mathjax: true
---

## THE DAEDALUS ATTACK

###  Generating adversarial examples

输入图像为x，对抗样本为x‘，扰动为$\delta=x'-x$。优化问题为：

<img src="https://i.loli.net/2020/08/20/yXfEBJsxr5KpemQ.png" alt="image-20200820150618490" style="zoom:50%;" />

f是对抗损失函数。

采用双曲正切函数进行变量替换：

<img src="https://i.loli.net/2020/08/20/wWpGvijT5HyJYPb.png" alt="image-20200820150955931" style="zoom:50%;" />

### Adversarial loss functions

总共有n个detection boxes。目标检测器为F。对于输入图像x，输出为$F(x)=\{B^x,B^y,B^w,B^h,B^0,P\}$。其中$B^x=\{b^x_0,b^x_1,...,b^x_n\}$，$B^y=\{b^y_0,b^y_1,...,b^y_n\}$。$B^0$为 objectness scores，P为class probabilities。

可以指定对特定类别$\lambda$的目标进行攻击，也可以指定对多个类别$\Lambda$进行攻击。我们定义如下损失：

<img src="https://i.loli.net/2020/08/20/nu1RLP9JxolGCmB.png" alt="image-20200820151739374" style="zoom:50%;" />

f1：最小化box间的IOU。

f2：最小化box的尺寸，最大化box间的距离。

f3：最小化box的尺寸。