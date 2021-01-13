# Abstract

arXiv 1610，引用 488。

We classify most current re-ID methods into two classes, i.e., **image-based and video-based**.

# 1 Introduction

Technically speaking, a practical person re-ID system in video surveillance can be broken down into three modules,  i.e., **person detection, person tracking, and person retrieval**.

It is generally believed that the first two modules are  independent computer vision tasks, so most re-ID works **focus on the last module, i.e., person retrieval**.

## 1.1 Organization of This Survey

In Section 4, since **the relationship between detection, tracking, and re-ID has not been extensively studied**, we will discuss several previous works and point out future research emphasis.

## 1.2 A Brief History of Person Re-ID

Person re-ID research started with **multi-camera tracking** [8].

One year later in **2006**, Gheissari et al. [11] employed only the visual cues of persons after a spatial-temporal segmentation algorithm for **foreground detection**.

This work [11] **marks the separation of person re-ID from multi-camera tracking**, and its beginning as an **independent computer vision task**.

Initially intended for tracking in videos, most re-ID works focus on image matching instead.

[13] additionally employ a **segmentation model to detect the foreground**.

# 2 IMAGE-BASED PERSON RE-ID

In literature, person re-ID is mostly explored with single images (**single shot**).

$\mathcal{G}$：a gallery (database) composed of $N$ images。每幅图像对应一个具有不同 identity 的人。
$\mathcal{G} = \{g_{i}\}_{i=1}^{N}$
$q$：a probe (query) image。
$i^{*}$：the identity of probe $q$。
$i^{*} = arg\ max_{i \in 1,2,...,N}sim(q, g_{i})$

# 3 VIDEO-BASED PERSON RE-ID

$q = \{q_{i}\}_{i=1}^{n_q}$
$g = \{g_{j}\}_{j=1}^{n_{g}}$
$n_{q}/n_{g}$: the number of bounding boxes within each video sequence, respectively.

As important as the bounding box features are, video-based methods pay additional attention to **multi-shot** matching schemes and the integration of **temporal information**.

# 4 FUTURE: DETECTION, TRACKING AND PERSON RE-ID

 In [29], Zheng et al. propose fusing local-local and global-local matches to address partial reID problems with **severe occlusions or missing parts**.