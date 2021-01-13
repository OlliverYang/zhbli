---
title: '[CVPR2020] Memory Enhanced Global-Local Aggregation for Video Object Detection'
date: 2020-05-09 13:36:47
tags:
- CVPR2020
- Video Object Detection
---

## Abstract

人类如何识别视频中的物体？由于单帧图像质量的下降，人们可能很难进利用一幅图像的信息来识别该帧中的被遮挡目标。

我们认为，人类识别视频中的目标有两个重要线索：

1. global semantic information
2. local localization information

近来，许多方法采用自注意力机制来利用线索 1 或线索 2 增强关键帧中的特征。

本文提出 memory enhanced global-local aggregation (MEGA) 网络，这是同时考虑线索 1 和线索 2 的首批方法之一。

此外，借助新颖的 Long Range Memory (LRM) module，可以使关键帧访问更多内容。

性能：

- https://github.com/Scalsol/mega.pytorch
- ImageNet VID validation set：mAP=85.4。