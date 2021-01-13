# Abstract

本文回顾了经典的MHT（multiple hypotheses tracking/多假设跟踪）算法。

The success of MHT largely depends on the ability to **maintain a small list of potential hypotheses**, which can be facilitated with the accurate object detectors that are  currently available.

In order to further utilize the strength of MHT in exploiting **higher-order information**, we introduce a method for training online **appearance models** for each **track hypothesis**.

# Introduction

MHT **builds a tree of potential track hypotheses for each candidate target**, thereby providing a systematic solution to the **data association problem**.

The **likelihood of each track is calculated** and the most  likely combination of tracks is selected.

Importantly, MHT is ideally suited to exploiting **higher-order** information such as **long-term motion** and **appearance** models, since the **entire track hypothesis can be considered** when computing the likelihood.

因为当前目标检测的方法进步了，所以MHT的搜索空间就小了很多。

# Related word

Collins [11] showed mathematically that the **multidimensional assignment problem** is a more complete representation of the multi-target tracking problem than the **network flow formulation**.

**Classical solutions to multidimensional assignment** are **MHT** [36, 12, 17, 34] and Markov Chain Monte Carlo  (**MCMC**) data association [19, 32].

#### Exploit appearance information to solve data association:

- **Network flow-based method**: the pairwise terms can be weighted by offline trained appearance templates [38] or a simple distance metric between appearance features [45].
- **MHT framework**: In [17], a simple fixed appearance model is incorporated into a standard
  MHT framework. 

# Multiple Hypotheses Tracking

$k$：most recent frame。
$M_{k}$：$k$ 帧中的目标（observation）数。
$i_{k}$：对于一段轨迹，该轨迹在 $k$ 帧中对应的目标。
$i_{1}, i_{2}, ..., i_{k}$：track hypothesis over $k$ frames——这段轨迹在第一帧中选了哪个目标，在第二帧中选了那哪段目标，……。
$z_{i_{i}i_{2}...i_{k}}$：一个 track hypothesis 是否被选做最终解。
global hypothesis：一组不冲突的 track hypothesis。

A **key strategy in MHT** is to **delay data association decisions by keeping multiple hypotheses active** until **data association ambiguities are resolved**.

MHT **maintains multiple track trees**, and **each tree represents all of the hypotheses that originate from a single observation** (Fig. 1c). 每棵树具有多个轨迹假设。

At each frame, the **track trees are updated from observations** and **each track in the tree is scored**.

The best set of non-conflicting tracks (the **best global hypothesis**) can then  be found by solving a **maximum weighted independent set (MWIS) problem** (Fig. 2a).

Afterwards, branches that deviate too much from the global hypothesis are pruned from the trees,  and the algorithm proceeds to the next frame.

## 3.1. Track Tree Construction and Updating

A track tree encapsulates multiple hypotheses **starting from a single observation**.

At each frame, a **new track tree** is constructed **for each observation**, representing the possibility that this observation corresponds to a **new object entering the scene**. 当前帧的一个检测框，可能是一个新跟踪轨迹的起点。

Previously existing track trees are also updated with **observations from the current frame**. 也可能属于已有的跟踪轨迹。

## 3.2. Gating

Based on the motion estimates, a **gating area** is **predicted for each track hypothesis** which specifies **where the next observation of the track is expected to appear**.

$\mathbf{x}_{k}^{l}$：轨迹 $l$ 在时刻 $k$ 可能出现的区域。

## 3.3. Track Scoring

Each track hypothesis is associated with a track score.

$S^{l}(k)$：轨迹 $l$ 在第 $k$ 帧的得分。
$S_{mot}^{l}(k)$：运动得分。
$S_{app}^{l}(k)$：表观得分。
$i_{1:k}$：观测序列 $i_{1}, i_{2}, ..., i_{k}$。

## 3.4. Global Hypothesis Formation

Given the set of trees that contains all trajectory hypotheses for all targets, we **want to determine the most likely combination of object tracks at frame k**.

Following [34], the task of finding the most likely set of tracks can be formulated as a **Maximum Weighted Independent Set (MWIS) problem**. This problem was shown in [34] to be **equivalent to the multidimensional assignment** problem (13) in the context of MHT..

## 3.5. Track Tree Pruning

Pruning is an essential step for MHT due to the exponential increase in the number of track hypotheses over time.  We adopt the standard N-scan pruning approach.

# 4. Online Appearance Modeling

Motion-based  constraints are not very robust.

When target appearances are distinctive, taking the appearance information into account is essential to improve the accuracy of the tracking algorithm.

We adopt the **multioutput regularized least squares (MORLS) framework** [25] for learning appearance models of targets in the scene.

## 4.1. Multi-output Regularized Least Squares

Multiple linear regressors are trained and updated simultaneously in multi-output regularized least squares.

## 4.2. Application of MORLS to MHT

**Each tree branch (track hypothesis) is paired with a regressor** which is trained with the detections **from** the time when the track tree was born **to** the current time k.