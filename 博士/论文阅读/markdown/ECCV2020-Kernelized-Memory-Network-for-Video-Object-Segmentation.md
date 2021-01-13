---
title: '[ECCV2020] Kernelized Memory Network for Video Object Segmentation'
date: 2020-07-19 08:17:08
tags:
- ECCV2020
- Video Object Segmentation
mathjax: true
---

## Abstract

现有算法的问题：尽管 space-time memory networks (STM) 在 VOS 上发挥了作用，但 STM 是 non-local 的，而 VOS 是 local 的。

将 STM 应用于 VOS 的基本思想是使用第一帧和当前帧之间的中间帧。在STM中，当前帧是 query frame，历史帧是 memory frames。但 STM 是 non-local 的，而 VOS 是 local 的。具体而言，STM 在 query frame 和 memory frames 之间执行 non-local matching。而在 VOS 中，query frame 中的目标常常是 memory frames 中目标的 local neighborhood。

本文的解决方案：为了解决 VOS 和 STM 的不匹配，本文提出 kernelized memory network (KMN)。使用高斯核减小 STM 的 non-localization 的程度。

本文的另一个创新点：在使用视频训练之前，使用静态图像进行预训练。在预训练时，使用 Hide-and-Seek 策略，以更好地处理遮挡和进行分割边界提取。

速度：0.12秒每帧。

## Related Work

#### Memory networks

如果当前输入的目标信息存在于其他输入时，常使用 query，key，value（QKV）概念。Memory networks 将当前输入设置为 query，将其他输入设置为 memory。Key 和 value 从 memory 中提取。通过对 query 特征和 key 特征执行 non-local matching 操作，生成 query 和 memory 的 correlation map。然后，在 correlation map 上检索加权平均的 value。STM 利用 QKV 概念提升了 VOS 的性能。

#### Memory networks

[21] 在 correlation map 上使用高斯核创建用于语义对应的 argmax 函数。

> [21] Lee, J., Kim, D., Ponce, J., Ham, B.: **Sfnet: Learning object-aware semantic correspondence**. In: CVPR. pp. 2278–2287 (2019) 3

在语义对应任务中，对于每个 source point，仅需要从 source image 到 target image 的单个 matching flow。然而在 correlation map 上使用离散 softmax 会使网络无法训练。为此，kernel soft argmax 在 correlation map 上使用高斯核，然后平均 correlation scores。本文借鉴了这一思想，但存在差异：kernel soft argmax 把高斯核应用到 searching flow（即 memory frame）的结果上，作为可求梯度的 argmax 函数，而我们把高斯核应用到 query frame 上。

#### Difficulties in segmentation near object boundaries

EGNet [53] 使用目标边缘训练了一个  low-level layer，以提高对边缘的预测精度。LDF [48] 通过分离边界像素于非边界像素，并对其分别训练，以解决这一问题。

> [53] Zhao, J.X., Liu, J.J., Fan, D.P., Cao, Y., Yang, J., Cheng, M.M.: **Egnet: Edge guidance network for salient object detection**. In: ICCV. pp. 8779–8788 (2019) 4
>
> [48] Wei, J., Wang, S., Wu, Z., Su, C., Huang, Q., Tian, Q.: **Label decoupling framework for salient object detection**. In: CVPR. pp. 13025–13034 (2020) 4

本文解决了标注数据在边缘不够精确的问题。Hide-and-Seek 通过生成清晰的边界来解决该问题。

## Kernelized Memory Network

#### Architecture

网络结构与 STM [30] 相同。

> Oh, S.W., Lee, J.Y., Xu, N., Kim, S.J.: **Video object segmentation using spacetime memory networks**. In: ICCV (October 2019) 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13

与 STM 一样，当前帧是 query，带有 mask 的历史帧是 memory。一个 resnet50 从 memory 中提取 key 和 value，另一个 resnet50 从 query 中提取 key 和 value。在 memory 中，mask 和 和 RGB 通道进行串接。

通过在 res4 特征上附加卷积层（key/value embedding layers），获得 query/memory 的 key features 和 value features。

Memory 可能包含多帧，先分别为每帧计算 key/value features，再进行串接。

Query 和 memory 的 correlation map 的计算：对 query 和 memory 的 key features 的所有可能的组合计算内积。

利用 kernelized memory read 操作从 correlation map 中检索高度匹配的像素。Memory 中匹配的像素的 values 与 query 的 value 进行串接。然后，将串接的 value tensor 送入 decoder。

KMN 与 STM 的不同体现在 memory read 操作中。STM 仅执行 Query-to-Memory 匹配。而 KMN 同时执行 Memory-to-Query 和 Query-to-Memory 匹配。

#### Kernelized Memory Read

在 STM 的 memory read 操作中，non-local correlation map $c(p, q)$ 使用 memory 的 embedded key $k^M$ 和 query 的 embedded key $k^Q$ 计算得到：

<img src="https://i.loli.net/2020/07/19/PNmxXFcS9il7Kzg.png" alt="image-20200719095553156" style="zoom: 33%;" />

然后，位置 q 的 query 利用 correlation map 检索 value：

<img src="https://i.loli.net/2020/07/19/RpDQMjeL8uiIKor.png" alt="image-20200719095917226" style="zoom:33%;" />

STM 的 memory read 操作具有两个问题：

1. query 中的每个位置都在 memory 中检索。即仅存在 Query-to-Memory matching。若 query 中存在多个近似物体，则都会与 memory 中的目标成功匹配。
2. STM 在 query frame 和 memory frames 之间执行 non-local matching。而在 VOS 中，query frame 中的目标常常是 memory frames 中目标的 local neighborhood。

为了解决这些问题，本文利用 2D 高斯核进行 kernelized memory read 操作：

1. 同 STM，计算 non-local correlation map $c(p, q)$。
2. 对于 memory frames 中的每个位置 p，在 query 中的最佳匹配位置为：<img src="https://i.loli.net/2020/07/19/j7Cr8UV5pNBsDqh.png" alt="image-20200719101042655" style="zoom:33%;" />。这就是 Memory-to-Query matching。
3. 以 $\hat q(p)$ 为中心的 2D Gaussian kernel g 计算如下：<img src="https://i.loli.net/2020/07/19/AgMquFfs4jSVzBC.png" alt="image-20200719101417855" style="zoom:33%;" />。使用高斯核，memory 中的 value 以 local 方式进行检索：<img src="https://i.loli.net/2020/07/19/Okmo16DtTeAXlcY.png" alt="image-20200719101649077" style="zoom:33%;" />。这就是 Query-to-Memory matching。