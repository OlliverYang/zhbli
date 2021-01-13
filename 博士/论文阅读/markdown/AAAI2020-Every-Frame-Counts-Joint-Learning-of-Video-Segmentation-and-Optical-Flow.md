---
title: >-
  [AAAI2020] Every Frame Counts: Joint Learning of Video Segmentation and
  Optical Flow
date: 2020-07-29 15:03:06
tags:
- AAAI2020
- Video Semantic Segmentation
mathjax: true
---

## Abstract

现有算法的问题：视频分割和光流估计仍然被视为两个单独的任务。

本文的解决方案：提出同时进行视频语义分割和光流估计的框架。

## Introduction

光流编码了视频的帧间一致。主要有两方面的作用：

1. 提高视频分割精度。例如，[20, 34, 27] 复用先前帧的特征以加快分割速度，但会降低分割精度。
   1. [27] 直接利用先前帧的特征以节省计算量。
   2. [34] 利用了从 flownet 中计算的光流，将关键帧的特征传播到当前帧。
   3. [20] 自适应地传播特征。
2. 加快视频分割速度。例如，[7, 16, 8, 23, 11] 利用 flow 进行特征聚合，以获得更好的分割结果，但会降低分割速度。
   1. [7] 提出通过时空LSTM模块组合连续帧的CNN特征。
   2. [8] 将先前帧和当前帧以及当前帧中的特征组合起来以预测分割。
   3. [23] 提出了门控循环单元来传播语义标签。
   4. [16] 以无监督的方式从未标记的视频数据中学习。

> [20] Li, Y.; Shi, J.; and Lin, D. 2018. **Low-latency video semantic segmentation**. In CVPR, 5997–6005.
>
> [34] Zhu, X.; Xiong, Y.; Dai, J.; Yuan, L.; and Wei, Y. 2017. **Deep feature flow for video recognition**. In CVPR, 3.
>
> [27] Shelhamer, E.; Rakelly, K.; Hoffman, J.; and Darrell, T. 2016. **Clockwork convnets for video semantic segmentatio**n. In ECCV, 852–868. Springer.

> [7] Fayyaz, M.; Saffar, M. H.; Sabokrou, M.; Fathy, M.; Klette, R.; and Huang, F. 2016. **Stfcn: spatio-temporal fcn for semantic video segmentation**. arXiv preprint arXiv:1608.05971.
>
> [16] Jin, X.; Li, X.; Xiao, H.; Shen, X.; Lin, Z.; Yang, J.; Chen, Y.; Dong, J.; Liu, L.; Jie, Z.; et al. 2017. **Video scene parsing with predictive feature learning**. In ICCV, 5581–5589.
>
> [8] Gadde, R.; Jampani, V.; and Gehler, P. V. 2017. **Semantic video cnns through representation warping**. CoRR, abs/1708.03088 8:9.
>
> [23] Nilsson, D., and Sminchisescu, C. 2018. **Semantic video segmentation by gated recurrent flow propagation**. In CVPR, 6819–6828.
>
> [11] Hur, J., and Roth, S. 2016. **Joint optical flow and temporally consistent semantic segmentation**. In ECCV, 163–177. Springer.

本文提出同时进行视频语义分割和光流估计的框架。语义分割引入了语义信息，可帮助识别遮挡以实现更可靠的光流估计。同时，非遮挡的光流提供准确的像素级对应关系，以确保分割的时间一致性。

## Related Work

其他视频分割方法：

- [17] 在视频分割中使用了 dense random field。
- [2] 在高斯条件随机场（CRF）上引入了紧密连接的时空图。
- [11] 基于超像素，估计在光流和时间上一致的语义分割结果。
- [4] 提出了在多任务框架中学习视频目标分割和光流的方法，该框架着重于分割实例级的目标，以有监督的方式学习光流和目标分割。相比之下，我们的任务是对整个图像进行语义分割，而我们的光流是在无监督的情况下学习的。这两个任务不能直接比较。

> [17] Kundu, A.; Vineet, V.; and Koltun, V. 2016. **Feature space optimization for semantic video segmentation**. In CVPR, 3168–3175.
>
> [2] S. Chandra, C. Couprie, and I. Kokkinos (2018) **Deep spatio-temporal random fields for efficient video segmentation**. In CVPR, pp. 8915–8924.
>
> [11] J. Hur and S. Roth (2016) **Joint optical flow and temporally consistent semantic segmentation.** In ECCV, pp. 163–177.
>
> [4] J. Cheng, Y. Tsai, S. Wang, and M. Yang (2017) **Segflow: joint learning for video object segmentation and optical flow.** In ICCV, pp. 686–695.

## Methodology

<img src="https://i.loli.net/2020/07/29/HZSjcwBYXCbzJym.png" alt="image-20200729161445548" style="zoom:50%;" />

### Framework Overview

模型的输入是来自同一视频的图像对 $I_i, I_{i+t}, t\in [1,5]$。

网络包含三部分：

- the shared encoder part：包含resnet的1-3层。
- the segmentation decoder part
- the flow decoder part

网络还包括如下两个模块：

- temporal consistency module
- occlusion handling module

### Temporally Consistent Constraint

对于两帧 $I_i,I_{i+t}$，送入编码网络得到特征图 $S_i,S_{i+t}$。因为我们同时学习前向和后向光流 $F_{i\rightarrow i+t}, F_{i+t\rightarrow i}$，我们得到 warp 的特征 $S'_{i},S'_{i+t}$：

<img src="https://i.loli.net/2020/07/29/P2W16amikZYzhqj.png" alt="image-20200729162918256" style="zoom:50%;" />

使用可微分的双线性插值进行warp操作。

注意，光流在遮挡区域不可用。因此我们通过检查一个像素在相邻帧是否有对应像素，估计 occlusion maps $O_{est}^i, O_{est}^{i+t}$。Temporal
consistency loss 定义为：

<img src="https://i.loli.net/2020/07/29/9GJTqZgnW2y3jRC.png" alt="image-20200729163507163" style="zoom:50%;" />

训练时计算了两个方向的损失。

### Occlusion Estimation

网络通过自监督方式学习遮挡。遮挡估计网络和光流估计网络共享大部分参数。在光流分支的每个 block，添加两层卷积和一个sigmoid层用于遮挡估计。利用后向光流 $F_{i+t\rightarrow i}$，可以在像素级别计算两帧的对应关系。我们把光流解耦为垂直项和水平项$F_{i+t\rightarrow i}(y,x,1),F_{i+t\rightarrow i}(y,x,0)$，则有：

<img src="https://i.loli.net/2020/07/29/eGHj8nS4B6LivEK.png" alt="image-20200729165326943" style="zoom:50%;" />

（说明：上述公式的作用是计算$i$帧中的坐标点$(x_i,y_i)$经过光流后在第$i+t$帧的对应坐标点$(x_{i+t},y_{i+t})$。）

后向光流$F_{i+t\rightarrow i}$的 occlusion mask $\hat O_i$ 定义为：若在 $I_{i+t}$ 中存在对应像素$(y_{i+t},x_{i+t})$，则$\hat O_i (y_i,x_i)=0$，否则为1。

带惩罚项的交叉熵用于计算遮挡估计的损失：

<img src="https://i.loli.net/2020/07/29/u6onPfBFTEAQLc5.png" alt="image-20200729165948735" style="zoom:50%;" />

### Optical Flow Estimation

语义图$M$引入了有关运动的语义信息。此外会计算error masks以指出错误的光流区域，从而进行可靠的光流估计。

首先计算两个分支的inconsistent mask $O_{seg} = (M \ne M')$，其中$M'$是使用双线性插值得到的warp后的分割结果。Error mask 计算为：

<img src="https://i.loli.net/2020/07/29/S4oizhab5kwespx.png" alt="image-20200729171613094" style="zoom:50%;" />

Photometric loss 的计算：

<img src="https://i.loli.net/2020/07/29/BPeObF6q8Qgx4Ei.png" alt="image-20200729172546868" style="zoom:50%;" />

其中 $I'$ 是 warp 后的图像。

Smoothness loss 为：

<img src="https://i.loli.net/2020/07/29/fQXldyBHjeVLZg7.png" alt="image-20200729172813782" style="zoom:50%;" />