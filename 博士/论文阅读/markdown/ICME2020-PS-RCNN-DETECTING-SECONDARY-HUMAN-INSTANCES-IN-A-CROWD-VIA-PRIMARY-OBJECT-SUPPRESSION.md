---
title: >-
  [ICME2020] PS-RCNN: DETECTING SECONDARY HUMAN INSTANCES IN A CROWD VIA PRIMARY
  OBJECT SUPPRESSION
date: 2020-05-13 13:08:10
tags:
- ICME2020
- Object Detection
---

## PS-RCNN

###  Structure of PS-RCNN

PS-RCNN 包括两个并行的模块 P-RCNN 和 S-RCNN。

P-RCNN 用于检测未被遮挡或被轻微遮挡的目标，S-RCNN 用于检测被严重遮挡的目标。

在 PS-RCNN 中，RPN 用于为所有目标提供 proposals。

使用所有 ground truth 训练 P-RCNN，使用 P-RCNN 未检测到的目标训练 S-RCNN。

设 P-RCNN 检测到的目标为 $G_d$，在特征图上的每个 $G_d$ 对应的 ground truth 边框位置覆盖 human-shaped binary mask，利用该特征训练 S-RCNN。

### High resolution RoI Align

High Resolution RoI Align (HRRA) 指仅从最高分辨率的特征图利用 RoI Align 提取特征。