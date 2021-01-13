---
title: >-
  [CVPR2020] NMS by Representative Region: Towards Crowded Pedestrian Detection
  by Proposal Pairing
date: 2020-05-13 13:48:11
tags:
- CVPR2020
- Object Detection
mathjax: true
---

## Introduction

对于类内遮挡，使得检测器难以区分目标边界。为了解决这一问题，Repulsion loss [23] 和 AggLoss [26] 对出现在两个人中间的边框该处额外惩罚。

> [23] Xinlong Wang, Tete Xiao, Yuning Jiang, Shuai Shao, Jian Sun, and Chunhua Shen. **Repulsion loss: Detecting pedestrians in a crowd**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 7774– 7783, 2018.
>
> [26] Shifeng Zhang, Longyin Wen, Xiao Bian, Zhen Lei, and Stan Z Li. **Occlusion-aware r-cnn: detecting pedestrians in a crowd**. In Proceedings of the European Conference on Computer Vision (ECCV), pages 637–653, 2018.

Adaptive NMS 预测 density map，在 NMS 时，根据 density 为不同的边框设定不同的 IoU 阈值。

> [12] Songtao Liu, Di Huang, and Yunhong Wang. **Adaptive nms: Refining pedestrian detection in a crowd**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 6459–6468, 2019.

[16] 将注意力机制整合到行人检测中。

> [16] Yanwei Pang, Jin Xie, Muhammad Haris Khan, Rao Muhammad Anwer, Fahad Shahbaz Khan, and Ling Shao. **Mask-guided attention network for occluded pedestrian detection**. In Proceedings of the IEEE International Conference on Computer Vision, pages 4967–4975, 2019.

本文提出一种新的 NMS 算法 R$^2$NM——NMS by representative region。该算法可以充分利用行人的可见部分。

为了获得行人的可见部分，提出 Paired-Box Model (PBM)，同时预测行人的 full box 和 visible box。

## Method

### NMS by Representative Region

R$^2$NMS 和普通 NMS 的区别是，在 IoU 计算中，不是将两个 full-body boxes 的重叠，而是计算可见区域的重叠。这是因为，行人的可见区域的 IoU 通常较低。

### Paired-BBox Faster R-CNN

PBM 基于原始 Faster R-CNN 进行三点修改：

1. Paired Region Proposal Network (P-RPN)：生成 full/visible proposal pairs。
2. Paired Proposal Feature Extractor (PPFE)：为 proposal pair 提取特征，融合 full/visible boxes 的特征，得到 integrated representations。
3. Pair R-CNN (P-RCNN)：进行 pair-wise classification，微调 full/visible boxes。

#### Paired Proposal Feature Extractor

<img src="https://i.loli.net/2020/05/13/6cYICq3i5OJyaMH.png" alt="image-20200513144633752" style="zoom:50%;" />

对于每个 proposal pair，生成一个 visible body attention mask。1 表示可见，0 表示不可见。