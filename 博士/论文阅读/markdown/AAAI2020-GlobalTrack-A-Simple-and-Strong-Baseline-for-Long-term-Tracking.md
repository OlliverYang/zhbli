---
title: '[AAAI2020] GlobalTrack: A Simple and Strong Baseline for Long-term Tracking'
date: 2020-04-24 18:19:45
tags:
- AAAI2020
- Tracking
mathjax: true
categories:
- [Tracking, Global Search]
---

## Abstract

现有 long-term 跟踪器的问题：对于 long-term 跟踪来说，需要在很大的搜索区域内寻找图像（通常是全图）。然而现在缺少用余光 global instance search 的 baseline。

本文的解决方案：提出 GlobalTrack，不对任何时间连续性/目标位置/尺度做假设，从而彻底避免了累积误差。直接使用 top-1 结果作为跟踪结果。

性能：

- https://github.com/huanglianghua/GlobalTrack
- 6 FPS
- 训练时间：4 卡，16 小时。