# OSMO: Online Specific Models for Occlusion in Multiple Object Tracking under Surveillance Scene

MM 2018.

## ABSTRACT

Occlusion is the primary difficulty in surveillance MOT, which can be categorized into the **inter-object occlusion** and the **obstacle occlusion**.

Many current studies on general MOT focus on the former occlusion, but few studies have been conducted on the latter one.

Hence, we propose two models for dealing with these two kinds of occlusions.

- The  attention-based appearance model is proposed to solve the interobject occlusion
- the scene structure model is proposed to solve the obstacle occlusion.

## 1 INTRODUCTION

There are two kinds of inputs for MOT generally, including  the video shot by moving cameras (e.g. ego-motion videos), and  the video shot by static cameras (e.g. surveillance videos). In this paper, we focus on MOT in **surveillance videos**.

The inter-object occlusion is caused by the situation that one object occludes another object, which is also a big challenge in the general MOT. Recent studies have already focused on dealing with this problem.

- Some approaches try to build **robust appearance models** to distinguish the two objects before and after the occlusion  (e.g. [6, 29, 31]).
  - [6] Near-Online Multi-target Tracking with Aggregated Local Flow Descriptor. ICCV2015
  - [29] Part-based multiple-person tracking with partial occlusion handling. CVPR2012
  - [31] Multiple People Tracking by Lifted Multicut and Person Re-identification. CVPR2017
- And [7, 27] also consider the temporal appearance change of these two objects.
  - [7] Online Multi-object Tracking Using CNN-Based Single Object Tracker with Spatial-Temporal Attention Mechanism. ICCV2017
  - [27] Tracking the Untrackable: Learning to Track Multiple Cues with Long-Term Dependencies. ICCV2017
- Besides, some motion models (e.g.  [9, 20]) and interaction models (e.g. [27, 35, 41]) are also proposed to deal with the inter-object occlusion.
  - [9] The Way They Move: Tracking Multiple Targets with Similar Appearance. ICCV2013
  - [20]  Enhancing Linear Programming with Motion Modeling for Multi-target Tracking. WACV2015
  - [35] Exploiting Hierarchical Dense Structures on Hypergraphs for Multi-Object Tracking. PAMI2015
  - [41] Online Multi-object Tracking via Structural Constraint Event Aggregation. CVPR2016

On the other hand, the obstacle occlusion is caused by the situation that obstacles in the background occlude the object.

## 2 RELATED WORKS

## 3 OBSTACLE MAP SEGMENTATION

## 4 SCENE STRUCTURE MODEL FOR OBSTACLE OCCLUSION

## 5 ATTENTION-BASED APPEARANCE MODEL FOR INTER-OBJECT OCCLUS

However, when the **candidate detection is partially occluded**, the similarity between the candidate detection and the object is likely to decrease, which could lead to a **wrong association**  between the detection and the missing object. Hence, we design  an attention sub-network to measure the similarity between the  candidate detection and each bounding box on the trajectory $T_{i}$. Bounding boxes that are **similar to the candidate detection** will  account for a **large proportion** of the input of each LSTM cell,  which could increase the appearance similarity between the object and the **positive occluded detection**.

Given a **missing object** $o_{i}$ and a **candidate detection** $d_{j}$ at frame $t$,  their features can be extracted, where $\phi_{i}^{o}$  and $\phi_{j}^{d}$ denote features of $o_{i}$ and $d_{j}$, and $T_{i}$ denotes **the trajectory** of $o_{i}$. $\hat{\phi}_{i,k}$ denotes the output feature of the $k$-th bounding box $b_{i,k}$ on trajectory $T_{i}$ at frame $t_{k}$ , which is derived from the CNN.

Then we use an attention sub-network to measure the similarity between the candidate detection and each bounding box on the trajectory $T_{i}$.