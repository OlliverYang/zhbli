# Partial Person Re-identification

ICCV 2015，引用 104。

## Abstract

We address a **new** partial person re-identification (reid) **problem**, where only a partial observation of a person is available for matching across different non-overlapping camera views.

## 1. Introduction

Manual part alignment is a solution but it is unscalable.

A **perfect body part detector** may also solve the problem but such a detector does not exist under severe occlusions.

The existing models all assume that a full body appearance of each person is available.

实验数据集

- we contribute a **new datase**t called Partial REID dataset, which is specifically designed for this problem with a great deal more partial instances (see Fig. 2).
- Moreover, **modification on two existing datasets** are also carried out to simulate the partial re-id problem.

## 2. Related Work

A **pictorial model** was employed for **part-to-part matching** for person re-id in [3].
Xu et al. [34] introduced a cluster sampling based compositional part-based template method.
However, these models rely on **prior knowledge about the part-based templates**.
In a practical scenario, the observed part of a person may not be a regular part defined by the templates.

Lian et al. [16] introduced a spatial-temporal **Bayesian model** which is able to handle occlusions caused by multiple people walking together and Zheng et al. [39] proposed **group context** to overcome self-occlusion.
However, these methods still assume that the **full body of a person is detected** (manually cropped).
Under severe occlusions, such **full body detection is not obtainable** even manually.

Although sparse model [8] is used for solving the occlusion problem, it assumes that the **alignment is given**.

**Beyond person re-id, occlusion has been studied extensively in other computer vision problems.**

It is an especially important topic in **face recognition**, since faces are often occluded or self-occluded [12].

- Recently, **sparse representation** or dictionary learning has been utilised for solving the occlusion problem in face recognition [32, 43, 6, 35].
- Liao et al. [17] proposed a **multi-task sparse representation for solving the partial face recognition problem.**
- In order to further take the structure of occlusion as prior knowledge into consideration, Min et al. [23] proposed to **first detect the occlusion parts**.
- Meng and Zhang [35] proposed to use an **occlusion dictionary** to describe the occlusion, and further improvements were reported in [24, 1].
- Weng et al. [31] proposed a robust **feature matching** method and Hu et al. [7] proposed an **instance-to-class metric** for partial face recognition.

## 3. Methodology

Our partial person re-id framework has two main **matching components**:

- **local-to-local re-id model**
  - decompose the partial observation into small patches
  - perform matching at the patch level
  - Pros
    - Local patch is less affected by view/pose changes and non-rigid deformations of human body.
  - Cons
    - it contains less information than the whole part.
    - the spatial layout information of different patches is ignored during matching, thus incurring the mis-alignment problem.
- **global-to-local re-id model**
  - take the partial observation as a whole.
  - search it in each gallery image using a sliding window search strategy
  - Pro: using the whole partial observation as a searching unit enforces spatial layout consistency.
  - Con: suffers greatly from the view/pose changes and body deformations.

### 3.1. Local-to-Local Matching

The local-to-local matching model is based on **pairwise patch-based matching** by **sparse coding**.

### 3.2. Global-to-Local Matching

We further consider a sliding window matching (SWM) process to perform global-to-local matching, i.e. the matching between the whole partially observed appearance of a probe person image and any local portion of a gallery image. 