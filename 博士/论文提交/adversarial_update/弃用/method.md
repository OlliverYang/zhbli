#### Abstract

> We show that the basic adversarial examples alone can be used to tackle the online update task in object tracking. [4]

> Our method involves performing a simple input manipulation: maximizing predicted class scores with gradient descent. Our approach is thus simple to implement, while also requiring minimal tuning. [4]

> We propose a novel framework for real-time object tracking with efficient model adaptation. Given an object tracker, our framework learns to fine-tune its input template in only a few gradient-descent iterations using the target ground-truth at the first frame. [3]

To our knowledge, this work is the first attempt to exploit adversarial information for template update in siamese-based trackers. Extensive experiments on recent benchmarks demonstrate
that our method achieves better performance than other state-of-the-art trackers.

#### Introduction

Recently, some work focus on model update.

However, all of them perform on the weights, which has so many parameters, all of them need to be updated, which easily cause overfitting and compution cost. To solve these problems, many method design complex strategy to escape from overfiting and lower the compution.

> However, is there a simpler toolkit for solving these tasks ? [4]

 However, we only need to update the input tensor of shape $3\times 128\times128$. The benefits are two floders:

(1) escape from overfitting.

(2) speed up.

> To solve this problem, many researches [16, 45, 40] present different mechanisms to update template features. However, these methods only focus on combining the previous target features, ignoring the discriminative information in background clutter. This results in a big accuracy gap between the siamese-based trackers and those with online update. [1]

We are the  first to update the template.

Generally, adversarial exampless is used to attack the network. However, we use it to update the template.

#### Method

> At a high level, our adaptaion procedure is based on minimizing the loss of a tracker. [4]

> We propose the adversarial update tracker (AUTracker), with adversarial module, to online update as shown in Fig. 2. AUTracker is built upon the siamfc++ tracker, with a target classification branch and a target localization branch. The classification branch converts the feature map into a response map and provides the coarse locations of the target. The localization branch uses the bounding-box regression to localize targets. the adversarial module is applied in a plug-and-play manner, as shown in Fig. 3. [2]

We introduce a adversarial module for online update that is pluggable, in the sense that it does not alter the overall architecture of the base tracker.

The module takes as input the target $z$ and search region $x$ in the first frame, and outputs a new input $z'$.

The follow-up tracking procedure remains unchanged.

> The template generation process consists of initial embedding, gradient calculation and template updating.
>
> 1. First, the template image $z\in\mathbb R^{3\times128\times 128}$ is send to the siamese backbone $\phi$ to obtain an initial template β which is used to calculate the initial loss L.
> 2. Second, the gradient of the whole tracker is calculated through backward propagation.
> 3. Finally, the gradient of the template image is substracted to template image to get an updated target image. [1]

##### Basic Tracker

> We adopt siamfc++ as the basic tracker. fx(.) is used to model the feature extraction branch for search region, fz(.) is used to model the feature extraction branch for target region. We assume that the movement of the target is smooth between two consecutive frames. Thus, we can crop a search region X which is larger than the target patch Z in the current frame, centered at the target’s position in the last frame. The final score map is calculated by: ...

Sepcifically, we adopt the Basic Iterative Method (BIM) to generate the new input.

We expect to obtain $z'$ from $z$，such that, after $N$ steps of pixel update on support set $(z, x_0)$ to obtain $z'$, the tracker performs well on query set $(z', x_i)$。

The $i$th gradienet update step on $z'$ can be expressed as:
$$
z_0 = z, z_{N+1} = Clip_{z,\epsilon}\{z_N -\alpha \text{ sign}(\nabla_z L(z_N,y_{true}))\}
$$

> The AU module is inspired by the AIM developed for adversarial training. However, AU is different from the adversarial training from the following two aspects: 1) AU targets at update the target appearance so that loss can be well fitted to make the prediction better. In contrast, the AIM modify inputs to make the prediction bad; 2) PRP leverages more efficient row- and column-wise maximization operations to aggregate the large response to target centers, while the center/corner pooling uses comparison and substitution operations. [2]

#### 参考文献

[1] GradNet: Gradient-Guided Network for Visual Object Tracking

[2] SPSTracker: Sub-Peak Suppression of Response Map for Robust Object Tracking

[3] Real-Time Object Tracking via Meta-Learning: Efficient Model Adaptation and One-Shot Channel Pruning

[4] Image Synthesis with a Single (Robust) Classifier