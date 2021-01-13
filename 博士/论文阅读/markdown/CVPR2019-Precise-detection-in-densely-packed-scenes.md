---
title: '[CVPR2019] Precise detection in densely packed scenes'
date: 2020-05-13 12:40:45
tags:
- CVPR2019
- Object Detection
mathjax: true
---

## Deep IoU detection network

### Soft-IoU layer

为每个边框预测：该框与 ground truth 之间的 IoU：

<img src="https://i.loli.net/2020/05/13/96QXnUC3otidlkH.png" alt="image-20200513125326478" style="zoom:50%;" />

其中 $c^{iou}$ 为 Soft-IoU score。

### EM-Merger unit for inference

现有 $N$ 个 predicted bounding  box locations，及对应的 objectness $c$ 和 Soft-IoU scores $c^{iou}$。这些边框往往成簇地聚集在一起，彼此重叠。EM-Merger unit filters 过滤或拆分这些 overlapping detection clusters。