---
title: >-
  [arXiv2005] Enhancing Geometric Factors in Model Learning and Inference for
  Object Detection and Instance Segmentation
date: 2020-05-09 13:54:04
mathjax: true
---

## Abstract

本文提出 Complete-IoU (CIoU) loss 和  Cluster-NMS，用于增强边框回归和 NMS 中的几何因素。

我们考虑三个几何因素：

1. overlap area
2. normalized central point distance
3. aspect ratio

这项工作是对我们的开创性工作 [40] 的扩展。

> [40] Z. Zheng, P. Wang, W. Liu, J. Li, R. Ye, and D. Ren, “**Distance-IoU Loss: Faster and better learning for bounding box regression**,” in The AAAI Conference on Artificial Intelligence, 2020.

https://github.com/Zzh-tju/CIoU

## COMPLETE-IOU LOSS

在目标检测中，原始的 IoU loss [34] 为：

<img src="https://i.loli.net/2020/05/09/3WAXiVhgFmxbCSJ.png" alt="image-20200509140815169" style="zoom:50%;" />

> [34] H. Rezatofighi, N. Tsoi, J. Gwak, A. Sadeghian, I. Reid, and S. Savarese, “**Generalized intersection over union: A metric and a loss for bounding box regression**,” in The IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2019, pp. 658–666.

然而，它无法区分两个框不重叠的情况。因此提出了 GIoU [34]：

<img src="https://i.loli.net/2020/05/09/LgRpMK36EwjldxH.png" alt="image-20200509141020004" style="zoom:50%;" />

在无重叠的情况下，预测框将朝目标框移动。

### Analysis to IoU and GIoU Losses

####  Simulation Experiment

首先，我们分析 IoU loss 和 GIoU loss 的局限性。

对于 predicted box $\mathcal B_i$，current prediction 为：

<img src="https://i.loli.net/2020/05/09/koNMOFcmbThyCZ7.png" alt="image-20200509141805656" style="zoom:50%;" />

注意，梯度被乘上了 $2-IoU^{t-1}_i$ 以加速收敛。

#### Limitations of IoU and GIoU Losses

IoU loss 的缺点：无法处理边框不重叠的情况。

GIoU loss 的缺点：对于高长宽比的边框，收敛速度慢。

### CIoU Loss

损失函数考虑三种几何因素：

<img src="https://i.loli.net/2020/05/09/u2yOsovUrmF3lE5.png" alt="image-20200509142815050" style="zoom:50%;" />

其中 $S, D, V$ 分别表示 overlap area、distance 和 aspect ratio。

与 IoU 相似，我们希望 $D, V$ 都是尺度不变的：

<img src="https://i.loli.net/2020/05/09/pgLwm7zu9ODH1qe.png" alt="image-20200509143156078" style="zoom:50%;" />

<img src="https://i.loli.net/2020/05/09/9iGWOuzdaPEHIR6.png" alt="image-20200509143218627" style="zoom:50%;" />

<img src="https://i.loli.net/2020/05/09/TyOqv1kp9gmhwbW.png" alt="image-20200509143238776" style="zoom:50%;" />

<img src="https://i.loli.net/2020/05/09/csoKSWkUxbvglFL.png" alt="image-20200509143259419" style="zoom:50%;" />

<img src="https://i.loli.net/2020/05/09/z2iCnfmo98ZdKTD.png" alt="image-20200509143354412" style="zoom:50%;" />

## CLUSTER-NMS

略。