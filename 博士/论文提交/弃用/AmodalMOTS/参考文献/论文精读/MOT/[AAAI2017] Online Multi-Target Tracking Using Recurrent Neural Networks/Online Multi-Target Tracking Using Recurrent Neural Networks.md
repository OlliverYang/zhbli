# Abstract

AAAI 2017，引用 239。

Here, we propose for **the first time**, an end-to-end learning approach for online multi-target  tracking.

# Introduction

Inspired by the well-studied Bayesian filtering idea, we present **a recurrent neural network** capable of performing **all multi-target tracking tasks** including prediction, data association, state update as well as initiation and termination of targets within a unified network structure (Fig. 1).

# Related Work

Early works include the **multiple hypothesis tracker** (MHT) (Reid 1979) and **joint probabilistic data association** (JPDA) (Fortmann, Bar-Shalom, and  Scheffe 1980).

Recently, the problem is cast as a **linear program and solved via relaxation, shortest-path, or min-cost algorithms**.

More recently, **graph multi-cut** formulations (Tang et al. 2016) have also been employed.

#  Background

## Recurrent Neural Networks

$h_{t}^{l}$：hidden state at time $t$ on layer $l$。
$h_{t}^{l} = tanh\ W^{l}(h_{t}^{l-1}, h_{t-1}^{l})$：时刻 $t$ 的 $l$ 层的状态由时刻 $t$ 的 $l-1$ 层的状态和时刻 $t-1$ 的 $l$ 层的状态决定。
$W$：可学习的参数矩阵。
$y_{t}$：the desired output。

LSTM: Next to the hidden state, the LSTM unit also keeps an embedded representation of the state $c$ that acts as a memory.

A **gated mechanism** controls how much of the previous state should be “forgotten” or replaced by the new input (see Fig. 2, right, for an illustration).

$h_{t}^{l} = o \odot tanh\ (c_{t}^{l})$
$c_{t}^{l} = f \odot c_{t-1}^{l} + i \odot g$
$n$：the size of input/output/forget gates。

![image-20200226085814194](C:\Users\zhbli\Documents\博士\论文提交\AmodalMOTS\参考文献\论文精读\MOT\[AAAI2017] Online Multi-Target Tracking Using Recurrent Neural Networks\RNN+LSTM.png)

## Bayesian Filtering

In Bayseian filtering, the goal is to estimate the true **state** $x$ from noisy **measurements** $z$.

# Our Approach

## Preliminaries and Notation

$x_{t} \in \mathbb{R}^{N \cdot D}$： the vector containing the states for **all targets** at **one time** instance。一帧中的所有目标。
$(x, y, w, h)$：目标的特征，用边框表示。
$D = 4$：目标特征的维数。
$N$：the number of interacting targets that are represented (or tracked) simultaneously in one particular  frame. $N$ is what we call the **network’s order** and captures the **spatial dependencies between targets**. Here, we consider a special case with  $N = 1$ where all targets are assumed to **move independently**. In other words, **the same RNN is used for each target**.
$z_{t} \in \mathbb{R}^{M \cdot D}$： the vector of all measurements in one frame。
$M$：每帧中最多能检测到的目标数。
$\mathcal{A}  \in [0, 1]^{N \times (M+1)}$： assignment probability matrix。

## Multi-Target Tracking with RNN

As motivated above, we decompose the problem at hand into two major blocks: **state prediction and update as well as track management** on one side, and **data association** on the other.

## Target Motion

We rely on a temporal RNN depicted in Fig. 2 (left) to learn the temporal dynamic model of targets as well as an indicator to determine births and deaths of targets (see next section).

在时刻 $t$，RNN 为下一个 time step 预测四个输出：
$x_{t+1}^{*} \in \mathbb{R}^{N \cdot D}$：a vector of predicted states for all target。
$x_{t+1} \in \mathbb{R}^{N \cdot D}$： a vector of all updated states。
$\mathcal{E}_{t+1} \in (0, 1)^{N}$： a vector of probabilities indicating for each target how likely it is a real trajectory。
$\mathcal{E}_{t+1}^{*}$：the absolute difference to $\mathcal{E}_{t}$。

## Initiation and Termination

We propose to capture  the time-varying number of targets by an additional variable  $\mathcal{E} \in (0, 1)^{N}$ that mimics the probability that a target exists  ($\mathcal{E} = 1$) or not ($\mathcal{E} = 0$) at one particular time instance.

## Data Association with LSTMs

Approaches like JPDA are on the other side of the  spectrum. They consider **all possible assignment hypotheses** jointly, which results in an **NP-hard** combinatorial problem.

The main idea is to exploit the LSTM's temporal step-by-step functionality to predict the **assignment for each target one target** at a time.