---
title: '[ECCV2020] Adversarial Ranking Attack and Defense'
date: 2020-08-16 17:44:24
tags:
- ECCV2020
- Adversarial Attack
mathjax: true
---

## Adversarial Ranking

定义候选集$X=\{c_1,c_2,...,c_n\}$。

### Candidate Attack

候选攻击的目的是提升或降低**一个候选c**相对于查询集$Q=\{q_1,q_2,...,q_w\}$中的排名。通过在c上添加**扰动r**来实现。

设 $Rank_X(q,c)$ 候选c相对于查询q的排名。排名值越小表示排名越高。

<img src="https://i.loli.net/2020/08/16/szZ7qGjlw29fCR8.png" alt="image-20200816174930081" style="zoom:50%;" />

该优化问题不能被直接求解。因为排名值 $Rank_X(q,c)$ 是离散的。因此需要寻找一个替代目标函数。

在度量学习中，给定两个候选 $c_p,c_n\in X$，其中 $c_p$ 比 $c_n$ 排名靠前，即 $Rank_X(q,c_p) < Rank_X(q,c_n)$，则可用三元组损失表示：

<img src="https://i.loli.net/2020/08/16/QmaboRKPlXyS6qU.png" alt="image-20200816175700683" style="zoom:50%;" />

因此前述优化问题可表示为如下优化问题：

<img src="https://i.loli.net/2020/08/16/fdKJVtisjC3QSZ5.png" alt="image-20200816175559316" style="zoom:50%;" />

为了求解该优化问题，可使用 PGD （即迭代版 FGSM）。

具体而言，为了寻找扰动r以创建 adversarial candidate $\tilde c = c + r$，PGD每次迭代时进行两步操作。

1. 根据梯度更新 $\tilde c$
2. 进行裁剪

<img src="https://i.loli.net/2020/08/16/8QvwraKGiUhXq42.png" alt="image-20200816180850807" style="zoom:50%;" />

若想降低候选的排名，目标函数可设为：

<img src="https://i.loli.net/2020/08/16/ID8vWguPhBUc1Sw.png" alt="image-20200816181513174" style="zoom:50%;" />

### Query Attack

查询攻击的目标是提升/降低一组候选C相对于查询q的排名。通过在查询上添加扰动r实现。