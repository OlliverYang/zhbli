---
title: '[writing] Siamese trackers'
date: 2020-09-10 17:41:45
tags:
- writing
---

## Siamese trackers

### ATOM - Introduction

These Siamese trackers formulate the visual object tracking problem as learning a general similarity map by **cross-correlation** between the feature representations learned for the **target template** and the **search region**.

### ATOM - Related Work

These trackers formulate visual tracking as a crosscorrelation problem and are expected to better leverage the merits of deep networks from end-to-end learning. In order to produce a similarity map from cross-correlation of the two branches, they train a Y-shaped neural network that joins two network branches, one for the object template and the other for the **search region**. Additionally, these two branches can remain fixed during the tracking phase [42, 1, 16, 45, 25, 54] or updated online to adapt the appearance changes of the target [44, 43, 13].

### SPM

SiamFC employs Siamese convolutional neural networks (CNNs) to extract features, and then uses a simple **cross-correlation** layer to perform dense and efficient sliding-window evaluation in the search region. Every patch of the same size as the target gets a similarity score, and the one with the highest score is identified as the new target location. 

### DiMP

These approaches first learn a feature embedding, where the similarity between two image regions is computed by a simple cross-correlation. Tracking is then performed by finding the image region most similar to the target template.

### D3S

Siamese trackers apply a backbone pre-trained offline with general targets such that object-background discrimination is maximized by correlation between the **search region** and **target template** extracted in the first frame [2].

### SiamAttn

The Siamese-based trackers formulate the problem of visual object tracking as a matching problem by computing **cross-correlation** similarities between a **target template** and a **search region**, which transforms the tracking problem into finding the target object from an image region by computing the highest visual similarity [1, 25, 24, 36, 44].

### Ours

Siamese trackers formulate the visual object tracking problem as learning **cross-correlation** similarities between a **target template** and a **search region**. Tracking is then performed by finding the target object from an image region by computing the highest visual similarity.