---
title: '[CVPR2020] ROAM: Recurrently Optimizing Tracking Model'
date: 2020-05-11 20:30:35
tags:
- CVPR2020
- Tracking
mathjax: true
categories:
- [Tracking, Meta-Learning]
---

![image-20200511204845469](https://i.loli.net/2020/05/11/AtycLmXMWuZjQGK.png)

## Proposed Algorithm

### Resizable Tracking Model

Tracking model $\pmb \theta$ 包括两部分：correlation filter $\pmb \theta_{cf}$ 和 bounding box regression filter $\pmb \theta_{reg}$。这两个滤波器都通过双线性插值进行尺度缩放，以适应目标的形状变化：

<img src="https://i.loli.net/2020/05/11/nARypXgYNSzBh1a.png" alt="image-20200511213652811" style="zoom:50%;" />

### Recurrent Model Optimization

本文提出 recurrent neural optimizer，使用该 optimizer 对网络进行一次梯度更新就能使模型收敛到较好的状态。

在离线训练阶段，我们使用 recurrent neural optimizer 对跟踪模型执行一步梯度更新，然后再未来帧中计算损失，并使损失降至最低。

离线学习阶段完成后，使用 recurrent  neural optimizer 循环更新跟踪模型，以适应目标表观变化。

我们定义 response generation network 为 $\mathcal G(F;\pmb \theta_{cf},\phi)$，定义 bounding box regression network 为 $\mathcal R(F;\pmb \theta_{reg},\phi)$，跟踪损失包括 response loss 和 regression loss：

<img src="https://i.loli.net/2020/05/12/oJ1MKTPnStfijCA.png" alt="image-20200512195315208" style="zoom:50%;" />

其中 $M$ 是具有高斯形状的 label map，$B$ 是 ground truth box。

跟踪网络的更新方式为：

<img src="https://i.loli.net/2020/05/12/xVlH2y7qwbrX98K.png" alt="image-20200512195723109" style="zoom:50%;" />

其中 $\pmb \lambda^{(t-1)}$ 是 fully element-wise  learning rate，与 tracking model parameters $\pmb \theta^{(t-1)}$ 具有相同的维数。

学习率由 LSTM 产生，输入包括：

- previous learning rate $\pmb \lambda^{(t-2)}$
- current parameters $\pmb\theta^{(t-1)}$
- current update loss $\ell ^{(t-1)}$
- gradient $\nabla_{\pmb\theta^{(t-1)}}\ell^{(t-1)}$

<img src="https://i.loli.net/2020/05/13/hvKHIP5bp7drk18.png" alt="image-20200513102328102" style="zoom:50%;" />

其中 $\mathcal O(\cdot;\pmb w)$ 是参数为 $\pmb w$ 的 coordinate-wise LSTM [1]。该 LSTM 在输入 的所有维度上共享梯度，而 $\sigma$ 是用于限制学习率的 sigmoid 函数。LSTM 的输入 $\mathcal I^{(t-1)}$ 为：将四个 sub-inputs 沿新轴 进行 element-wise stacking。

> [1] Marcin Andrychowicz, Misha Denil, Sergio Gomez, Matthew W. Hoffman, David Pfau, Tom Schaul, and Nando de Freitas. **Learning to Learn by Gradient Descent by Gradient Descent**. In NeurIPS, 2016.

Current update loss $\ell^{(t-1)}$ 从具有 $n$ 个 updating samples 的 mini-batch 中计算：

<img src="https://i.loli.net/2020/05/13/3Ia5mcUFGutHv1W.png" alt="image-20200513103103312" style="zoom:50%;" />

其中 updating samples $(F_j,M_j,B_j)$ 从前 $\tau$ 帧中收集，$\tau$ 是在线跟踪过程中模型更新的 frame interval。

最后，我们在随机选择的未来帧上测试 updated model $\pmb\theta^{(t)}$ 并获得  meta loss：

<img src="https://i.loli.net/2020/05/13/yQnPecro3UMKZJp.png" alt="image-20200513103416981" style="zoom:50%;" />

其中 $\delta$ 是在 $[0,\tau-1]$ 中随机选择的。

在离线训练期间，在一小段视频上执行上述步骤，并获得 averaged meta loss 以更新 neural optimizer：

<img src="https://i.loli.net/2020/05/13/u3RoiB6TCvprwEI.png" alt="image-20200513103627187" style="zoom:50%;" />

其中 $N$ 是 batch size，$T$ 是 model updates 的数量。

### Random Filter Scaling

Neural optimizers 由于过拟合问题而难以在新任务上泛化。我们发现经过初步训练的优化器将预测相似的学习率。我们将其归因于过拟合到具有相似 magnitude  scales 的网络输入。为解决这一问题，在离线训练的每次迭代中，将跟踪模型 $\pmb \theta$ 与随机采样的向量相乘。这样，网络输入 $\pmb x$ 可以间接缩放而无需修改训练样本。因此，学习的神经优化器被迫预测具有不同幅度的输入的自适应学习率。