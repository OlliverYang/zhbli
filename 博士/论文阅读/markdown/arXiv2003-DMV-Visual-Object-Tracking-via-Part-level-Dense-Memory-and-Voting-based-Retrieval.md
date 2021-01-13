---
title: >-
  [arXiv2003] DMV Visual Object Tracking via Part-level Dense Memory and
  Voting-based Retrieval
date: 2020-05-13 16:48:53
tags:
- Tracking
mathjax: true
categories:
- [Tracking, Architecture]
---

<img src="https://i.loli.net/2020/05/13/IR5Los8WYJm4dez.png" alt="image-20200513165310769" style="zoom:50%;" />

<img src="https://i.loli.net/2020/05/13/mzWPIaJrxofkiVn.png" alt="image-20200513165329316" style="zoom:50%;" />

注意, 算法尚未开源.

key 和 value 的空间分辨率相同. $value = \phi(concat(key, cls_{map}, reg_{map}))$.

query 中的每个特征向量, 和所有 T 个 keys 的所有特征向量计算相似度, 得到 similarity score matrix $S \in \mathbb{R}^{(HW) \times (THW + 1)}$.

$S$ 的作用: 用于选择 memory cadidates, 即每个位置选择 $K$ 个来自于 values 的向量.

candidate value set $\mathbf{V}_i^*$: 注意是从 values 中选择的. 针对的是query的一个空间位置.

得到 candidates 后, 通过 Top-K Voting 获得 final target-aware features.

voting networks

- 输入: $K \times 2C$, 将 $K$ 个 candidate vaules 和 原始查询向量 $q_i$ 串接起来.
- 输出: $C$. 空间位置 $i$ 检索到的结果.

### 说明

跟踪结果是query和检索的特征相加得到的. 

训练voting networks时视频长度从 2 到 5, 说明如果视频过长则难以训练.

### Q&A

Q: 如果把 visual features 当作 search feature, 把 retrieved feautures 当作 template feature, 本文的两个特征尺度相同并直接相加预测最终结果, 而传统算法中 template feature 的尺寸是远小于 search feature 的, 并在每个位置执行互相关操作得到最终结果. 为什么会有这种差异 ?

A: 两种方法不能直接类比. retrieved features 中的每个元素是各自从 memory 中挑选的.

Q: 网络是怎么识别出模板特征的? 也就是图中有物体a和物体b, 怎么知道要跟踪哪个物体? 

A: 对于孪生网络, 根据 template features 知道的. 本文的话推测是在memory中得到特定于物体的信息. memory包括key和value, key是纯粹的表观特征, value包括表观特征和标签. 因此是基于value中的标签来判断要跟踪哪个物体.

Q: 测试时, 如何知道我要跟踪的是物体a还是物体b?

A: 对于孪生网络, 区别是template feature不一样. 本文中则是memory中第一帧的value的heatmap不一样.