# Abstract

In this paper, we present an online method that encodes long-term **temporal dependencies** across multiple cues.

Our method allows to correct data association errors and **recover observations from occluded states**.

# Introduction

In this work, we tackle the MTT (Multi-Target Tracking) problem by jointly learning a representation that takes  into account **Appearance**, **Motion**, and **Interaction** cues using RNNs (AMIR) (see Figure 1).

This is often formulated as an optimization problem with respect to a **graph** [57, 58]. **Each detection is represented by a node, and edges encode the similarity scores** [18, 4].

Our motion and interaction models leverage two separate Long Short-Term  Memory (LSTM) networks that track the motion and interactions of targets for longer periods – suitable for presence of **long-term occlusions**.

# Related work

Although appearance is an important cue, relying only on appearance can be problematic in MTT scenarios where the scene is highly crowded or when targets may share the same appearance.

To this end,  some work has been focused on **improving the appearance model** [19, 8], while other work has combined the **dynamics and interaction** between targets with the target appearance  [62, 3, 57, 80, 10, 65, 58].

## 2.1. Appearance Model

- raw pixel template
- color histogram
- covariance matrix
- pixel comparison
- SIFT-like features
- pose features
- deep features

## 2.2. Motion Model

The motion cue is a crucial cue for MTT, since knowing the likely position of targets in future frames will reduce the search space and hence increases the appearance model accuracy.

We present a Long Short-Term Memory (LSTM) model which learns to predict similar motion patterns.

## 2.3. Interaction Model

Interaction models capture **interactions and forces** between different targets in a scene [22, 25, 76].

In these models, each target reacts to energy potentials caused by interactions with other objects through forces (repulsion or attraction),  while trying to keep a desired speed and motion direction  [62, 3, 57, 80, 10, 65, 58].

# Multi-Target Tracking Framework

In this work, we propose a **new method** to **compute these similarity scores**.

## 3.1. Overall Architecture

As discussed in the introduction, combining these cues **linearly** is not necessarily the best way to compute the similarity score. We instead propose to use a structure of **RNNs to combine these cues** in a principled way.

In our framework, we **represent each cue with an RNN**.

We refer to the RNNs obtained from these cues as appearance (A), motion (M), and interaction (I) RNNs. The features represented by these RNNs ($\phi_{A}$,$\phi_{M}$,$\phi_{I}$) are **combined through another RNN** which is referred to as the **target (O) RNN**.

The target RNN outputs a **feature vector**, $\phi(t,d)$, which is used to output the **similarity** between a **target** $t$ and a **detection** $d$.

## 3.2. Appearance

The underlying idea of our appearance model is that we can compute the similarity score **between a target and candidate detection** based on purely visual cues.

Therefore, our appearance model should be able to **describe the similarities between input pairs**, as well  as be **robust to occlusions** and other visual disturbances.

Our appearance RNN (A) is an LSTM that accepts as inputs the appearance features from the appearance feature extractor ($\phi_{1}^{A}, ..., \phi_{t}^{A}$) and produces H-dimensional output $\phi_{i}$ for each timestep.

## 3.3. Motion

Our motion RNN (M) is an LSTM that accepts as inputs the velocities of a specific target at timesteps $1, ..., t$ as motion features, and produces an H-dimensional output $\phi_{i}$.

## 3.4. Interaction Model

The motion of a particular target is governed not only by its own previous motion, but also by the behavior of nearby  targets.

Since the number of nearby targets can vary, in order to use the same size input, we model the neighborhood of each target as a fixed size **occupancy grid**. The occupancy grids are extracted from our **interaction feature extractor**. For each target, we use an LSTM network to **model the sequence of occupancy grids**  (see Figure 6).

## 3.5. Target

Target RNN 的训练分为两步：

- 对 A, M, I RNN 和 CNN 特征提取器进行预训练。
- 讲 A, M, I 的输出向量串接成单个特征向量，作为 target RNN 的输入。