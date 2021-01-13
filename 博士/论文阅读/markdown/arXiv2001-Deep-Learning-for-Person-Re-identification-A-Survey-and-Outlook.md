---
title: '[arXiv2001] Deep Learning for Person Re-identification: A Survey and Outlook'
date: 2020-04-21 19:17:48
tags: Person Re-Identification
mathjax: true
---

![image-20200421192713520](https://i.loli.net/2020/04/21/o2fRQlx6d1873vz.png)

Identity Loss：将 reid 视为图像分类问题。

Verification Loss：用于优化成对关系。包括 contrastive loss 和 binary verification loss。

- contrastive loss：

  <img src="https://i.loli.net/2020/04/21/G9ERy8rfFTYegNA.png" alt="image-20200421193745441" style="zoom:50%;" />

- verification loss with cross-entropy：

  <img src="https://i.loli.net/2020/04/21/F6laoOyuEPsvepT.png" alt="image-20200421193902135" style="zoom:50%;" />

- Triplet loss

  <img src="https://i.loli.net/2020/04/21/nCGsM1UQLdZyhmP.png" alt="image-20200421194054482" style="zoom:50%;" />