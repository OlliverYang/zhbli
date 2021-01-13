---
title: '[arXiv1703] In Defense of the Triplet Loss for Person Re-Identification'
date: 2020-04-21 19:03:31
tags: Person Re-Identification
mathjax: true
---

## Abstract

在 reid 领域，目前认为 triplet loss 不如其他损失（classification loss，verification loss）+ 单独的度量学习性能好。本文证明使用 triplet 损失端到端训练的度量学习比其他方法都好。

## Introduction

classification loss 的缺点：训练参数随类别数而增加，而这些参数在训练后被丢弃。

verification loss 的缺点：仅在 cross-image representation 模式下可用，即仅能回答“这两幅图有多像”这一问题。这使得在其他任务如 clustering 和 retrieval 时难以应用，因为每个 probe 必须与所有 gallery image 配对。

triplet loss 不受欢迎的原因：如果简单应用，则性能不佳。一个要点是难例挖掘，否则训练将止步不前。然而很难明确定义难例，同时很费时。另外，使用太难的 triplet loss 容易使训练不稳定。

本文设计了基于 batch hard sample mining 的 triplet loss，改善了性能。

