# ABSTRACT

Neurocomputing 2020，引用4。

Four main steps in MOT algorithms are identified, and  an in-depth review of how Deep Learning was employed in each one of these stages is presented.

# 1 Introduction

The main difficulty in tracking multiple targets simultaneously stems from the various **occlusions** and **interactions** between objects, that can sometimes also have **similar appearance**.

We provide the **first** comprehensive survey on the use of Deep Learning in Multiple Object Tracking.

# 2 MOT: algorithms, metrics and datasets

## 2.1 Introduction to MOT algorithms

Many MOT algorithms formulate the task as an **assignment problem**.

The **majority** of MOT methods (with some exceptions, as we  will see) have been focusing on improving the **association**.

MOT algorithms can also be divided into **batch and online methods**. Batch tracking algorithms are allowed to use **future information** (i.e. from future frames) when trying to determine the object identities in a certain frame.

跟踪步骤：

- Detection stage
- Feature extraction/motion prediction stage
- Affinity stage: features and motion predictions are used to **compute a similarity/distance score** between pairs of detections and/or tracklets.
- Association stage: the similarity/distance measures are used to associate detections and tracklets belonging to the same target by assigning the same ID to detections that identify the same target.

## 2.2 Metrics

$MOTA = 1 - \frac{(FN + FP + IDSW)}{GT} \in (-\infty, 1]$

## 2.3 Benchmark datasets

MOTChallenge/KITTI.

# 3 Deep learning in MOT

## 3.1 DL in detection step

### 3.1.1 Faster R-CNN

SORT跟踪器的结果表明使用 Faster R-CNN 的检测结果可以提高跟踪性能。

At the time of publishing, SORT was ranked as the best-performing open source algorithm on the MOT15  dataset.

Moreover, an adaptation of  Faster R-CNN that adds a segmentation branch, Mask R-CNN [17], has been used for example by Zhou et al. [55] both to detect and to track pedestrians.

### 3.1.2 SSD

### 3.1.3 Other detectors

### 3.1.4 Other uses of CNNs in the detection step

Bullinger et al. explored a different approach in [76], where instead of computing classical bounding boxes in the detection step, a Multi-task Network Cascade [77] was instead **employed to obtain instance-aware semantic segmentation maps**. The authors argue that since the 2D shape of instances, differently from rectangular bounding boxes, **do not  contain background structures or parts of other objects**, optical flow based tracking algorithms would perform better,  especially when the target position in the image is also subject to camera motion in addition to the object’s own  motion.

## 3.2 DL in feature extraction and motion prediction

The most typical approach in this area is the use of CNNs to extract visual features, as it is commented in section 3.2.2.

Instead of using classical  CNN models, another recurrent idea consists in training them as **Siamese CNNs**, using contrastive loss functions, in order to **find the set of features that best distinguish between subjects**.

## 3.3 DL in affinity computation

While many works compute affinity between tracklets and detections (or tracklets and other tracklets) by **using some  distance measure over features extracted by a CNN**, there are also algorithms that use deep learning models to **directly output an affinity score, without having to specify an explicit distance metric** between the features.

## 3.4 DL in Association/Tracking step

Some works, albeit not as many as for the other steps in the pipeline, **have used deep learning models to improve the  association process** performed by classical algorithms, like the **Hungarian algorithm**, or to manage the track status (e.g. by deciding to start or terminate a track).