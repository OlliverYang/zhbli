---
title: >-
  [arXiv1611] A Discriminatively Learned CNN Embedding for Person123
  Re-identification
date: 2020-04-21 17:59:11
tags: Person Re-Identification
mathjax: true
---

## Abstract

本文回顾了两种 reid 网络结构：verification model 和 identification model。这两种模型各有优缺点。本文结合了这两种模型：提出孪生网络同时计算 identification loss 和 verification loss。给定一个图像对，网络预测两幅图像的身份，同时预测它们是否同一身份。

## Introduction

Verification model 的问题：仅使用 weak reid labels，没有充分利用标签信息，因此没有考虑图像对与数据集中其他图像之间的关系。

为了充分利用 reid 标签，identification models 将 reid 视为多类识别问题。缺点是训练任务与测试不完全一致。

<img src="https://i.loli.net/2020/04/22/Z3jKr42lFUHna9q.png" alt="image-20200422104418316" style="zoom:50%;" />

<img src="https://i.loli.net/2020/04/22/8heMbH7zpnFB94N.png" alt="image-20200422104845255" style="zoom:50%;" />