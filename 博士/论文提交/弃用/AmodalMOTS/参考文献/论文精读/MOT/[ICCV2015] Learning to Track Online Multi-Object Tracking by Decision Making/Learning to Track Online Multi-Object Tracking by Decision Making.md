# Abstract

使用马尔可夫决策过程（MDP）解决在线MOT问题。

Learning a **similarity function** for data association is equivalent to learning a **policy** for the MDP. 学习数据关联的相似函数等价于学习MDP的策略。

Moreover, our framework can naturally handle  the birth/death and appearance/disappearance of targets by treating them as **state transitions in the MDP** while leveraging existing online single object tracking methods.

The **policy learning** is approached in a **reinforcement learning** fashion.

# Introduction

For tracking-by-detection in the online mode, the **major challenge** is **how to associate** noisy object detections in the current video frame with previously tracked objects.

The basis for **any** data association algorithm is a **similarity  function between object detections and targets**.

To handle ambiguities in association, **it is useful to combine different cues** in computing the similarity, such as **appearance, motion, and location**.

In this work, we formulate the online multi-object tracking problem (MOT in the online mode) as decision making in Markov Decision Processes (MDPs), where **the lifetime of an object** is modeled with **a MDP**, and **multiple MDPs are assembled for multi-object tracking** (Fig. 1). 一个目标对应一个MDP，多个目标对应多个MDP。

# Online Multi-Object Tracking Framework

## 3.1. Markov Decision Process

MDP由如下元组构成：$(\mathcal{S}, \mathcal{A}, T(\cdot), R(\cdot))$.
$s \in \mathcal{S}$：目标状态。
$a \in \mathcal{A}$：目标可以执行的动作。
$T$：状态转移函数。
$R$：奖赏函数。执行状态 $a$ 到达状态 $s$ 后获得的奖赏。

$\mathcal{S} = \mathcal{S}_{Active} \cup \mathcal{S}_{Tracked} \cup \mathcal{S}_{Lost} \cup \mathcal{S}_{Inactive}$. **“Active” is the initial state for any target**. Likewise, a lost target can stay as lost, or go back to “Tracked” if it appears again, or **transition to “Inactive” if it has been lost for a sufficiently long time**. Finally, **“Inactive” is the terminal state for any target**, i.e., an inactive target stays as inactive forever.

In our MDP, the reward function is not given but needs to be learned from training data.

注意，采取动作的时间是，处理新一帧时。

## 3.2. Policy

策略 $\pi$ 是从状态空间到动作空间的映射。**Given the currents tate of the target, a policy determines which action to take.**

注意状态转移函数 $T$ 和策略 $\pi$ 的区别：$T$ 指在某状态下采取某动作会到达什么状态，$\pi$ 指在某状态下应该采取什么动作。

 The goal of **policy learning** is to **find a policy** which **maximizes the total rewards** obtained.

We present a novel **reinforcement learning** algorithm to **learn a good policy for data association in the Lost subspace**.

### 3.2.1 Policy in an Active State

Active 状态可以转移到 Tracked 状态或 Inactive 状态（处理噪声检测）。

通常的做法是使用 NMS 或使用检测得分阈值。

本文通过离线训练 2 类 SVM 把一个检测框分为“Tracked”或“Inactive”。这相当于学习在 Active 状态下执行动作到达状态 Tracked 或 Inactive 的奖赏。

### 3.2.2 Policy in a Tracked Stat

根据表观判断在 Tracked 状态时应该转变成 Tracked 状态还是 Lost 状态。具体而言，使用了光流信息。

$I$：target template，即目标对应的图像块。
$\mathbf{u}$：target template 中的一个点。
$\mathbf{v}$：根据光流计算的在新一帧中的 $\mathbf{u}$ 的对应点。
$\mathbf{u}'$：根据光流向后计算的在前一帧中的 $\mathbf{v}$ 的对应点。
$e$：FB error，用于衡量两个点是否对应。
$e_{medFB}$：用于判断位不同帧两个跟踪框的相似性。

### 3.2.3 Policy in a Lost State

The challenging case is to make the decision between **tracking the target** and **keeping it as lost**.  We
treat it as a **data association problem**.

具体做法是训练一个 2 类的线性分类器。使用强化学习训练该分类器。

$t$：a lost target。
$d$：an object detection。
$y$：$t$ 是否与 $d$ 相关联。