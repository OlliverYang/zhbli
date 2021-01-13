---
title: '[CVPR2020] Data Uncertainty Learning in Face Recognition'
date: 2020-04-21 10:16:21
tags:
- CVPR2020
- Face Recognition
mathjax: true
---

## Abstract

现有人脸识别算法的问题：对于 noisy images，建模数据不确定性是重要的，但是在人脸识别中很少被研究。先前工作 [35] 把每个人脸嵌入建模为高斯分布从而考虑不确定性。然而它使用来自现有模型的固定特征（高斯的均值）。这仅估计了方差，并依赖与专门设计的、计算量高的度量方法，因此不易使用。目前仍不清楚不确定性如何影响特征学习。

> Yichun Shi, Anil K Jain, and Nathan D Kalka. **Probabilistic face embeddings**. In Proceedings of the IEEE International Conference on Computer Vision, 2019.

本文将数据不确定性学习应用于人脸识别，首次使得特征（均值）和不确定性（方差）可以同时学习。提出两种学习方法，易于使用且性能良好。

我们还分析了整合不确定性估计如何帮助减少噪声样本的负面影响，以及如何影响特征学习的。

## Introduction

数据不确定性捕获数据的固有噪声。建模这种不确定性是重要的，因为噪声广泛存在于图像中。

大多数人脸识别方法将每张人脸图像表示为隐空间中一个确定性的嵌入点。通常，高质量的图像中，相同 ID 的人脸图像的特征是会聚集在一起的。然而很难为有噪声的人脸图像估计准确的嵌入点，通常位于 cluster 之外，并在嵌入空间中有很大的不确定性。

Probabilistic face embeddings（PFE）[35] 是首先考虑人脸识别中数据不确定性的工作。 对于每个样本，在隐空间中估计高斯分布，而不是一个固定点。具体而言，给定预训练的 FR 模型，每个样本的高斯均值固定为 FR 模型产生的嵌入。在 FR 模型添加并训练额外的分支以估计方差。训练通过新的相似性度量来进行：mutual likelihood score（MLS），用于度量两个高斯分布的 likelihood。PFE 为高质量的样本估计小的方差，为噪声样本估计大的方差。因此 PFE 可以减低噪声样本的错误匹配。

然而，PFE 仅学习不确定性，未学习嵌入特征（mean），因此不知道不确定性如何影响特征学习。同时传统的相似性度量如 cosine 距离无法使用。需要更复杂的 MLS 度量，增加了运行时间和内存。

我们首次将数据不确定性学习（DUL）引入人脸识别，使得特征（均值）和不确定性（方差）可以同时学习。这改善了特征，使得同类特征更紧凑。学习的特征可以直接使用传统相似性度量，不再需要 MLS 度量。

具体而言，我们提出两个学习方法：

1. 第一个方法是基于分类的，从头学习一个一个模型。
2. 第二个方法是基于回归的，用于改善现有模型。

我们从图像噪声的角度，讨论了学习的不确定性是如何影响这两种方法的模型训练的：学习的不确定性通过自适应降低噪声训练样本的负面影响，来改善特征嵌入的学习。

## Related Work

很多方法引入的 deep uncertainty learning，用于改进模型的鲁棒性和可解释性：

- 语义分割
  - Shuya Isobe and Shuichi Arai. **Deep convolutional encoderdecoder network with model uncertainty for semantic segmentation**. In 2017 IEEE International Conference on INnovations in Intelligent SysTems and Applications (INISTA), pages 365–370. IEEE, 2017.
  - Alex Kendall, Vijay Badrinarayanan, and Roberto Cipolla. **Bayesian segnet: Model uncertainty in deep convolutional encoder-decoder architectures for scene understanding**. BMVC, 2015.
- 目标检测
  - Jiwoong Choi, Dayoung Chun, Hyun Kim, and Hyuk-Jae Lee. **Gaussian yolov3: An accurate and fast object detector using localization uncertainty for autonomous driving**. In The IEEE International Conference on Computer Vision (ICCV), October 2019.
  - Florian Kraus and Klaus Dietmayer. **Uncertainty estimation in one-stage object detection**. arXiv preprint arXiv:1905.10296, 2019.
- Re-ID
  - Tianyuan Yu, Da Li, Yongxin Yang, Timothy M Hospedales, and Tao Xiang. **Robust person re-identification by modelling feature uncertainty**. In Proceedings of the IEEE International Conference on Computer Vision, pages 552–561, 2019.

人脸识别中，有对模型不确定性和数据不确定性的研究：

- 模型不确定性
  - Sixue Gong, Vishnu Naresh Boddeti, and Anil K Jain. **On the capacity of face representation**. arXiv preprint arXiv:1709.10433, 2017.
  - Umara Zafar, Mubeen Ghafoor, Tehseen Zia, Ghufran Ahmed, Ahsan Latif, Kaleem Razzaq Malik, and Abdullahi Mohamud Sharif. **Face recognition with bayesian convolutional networks for robust surveillance systems**. EURASIP Journal on Image and Video Processing, 2019(1):10, 2019.
  - Salman Khan, Munawar Hayat, Syed Waqas Zamir, Jianbing Shen, and Ling Shao. **Striking the right balance with uncertainty**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 103–112, 2019.
- 数据不确定性
  - Yichun Shi, Anil K Jain, and Nathan D Kalka. **Probabilistic face embeddings**. In Proceedings of the IEEE International Conference on Computer Vision, 2019.

## Methodology

###  Classification-based DUL for FR

#### Distributional Representation

将每个样本 $\mathbf{x}_i$ 在隐空间中的特征表示 $\mathbf{z}_i$ 定义为高斯分布：

<img src="https://i.loli.net/2020/04/21/HcBsDzOleWUp5N3.png" alt="image-20200421101935936" style="zoom:50%;" />

其中，高斯分布的均值和方差都与输入相关，并通过 CNN 预测：

<img src="https://i.loli.net/2020/04/21/MjtHph4kBedfzQC.png" alt="image-20200421111911376" style="zoom:50%;" />

此处预测的高斯是 diagonal multivariate normal。$\pmb{\mu}_i$ 可被视作人脸的理想特征，$\pmb{\sigma}_i$ 可视作不确定性。现在，每个样本的表示不再是固定的嵌入点，而是从高斯分布中随机采样的嵌入。

然而采样操作是无法反向传播的。我们使用 re-parameterization trick [24] 使得模型仍然能计算梯度。具体而言，首先从正太分布中采样与模型参数无关的随机噪声 $\epsilon$，然后生成 $\mathbf{s}_i$ 作为等效的特征表示（公式2）：

<img src="https://i.loli.net/2020/04/21/9VK7SxLcGrEw1Z5.png" alt="image-20200421101958743" style="zoom:50%;" />

其中，$\mathbf{s}_i$ 是图像的最终表示。

#### Classification Loss

使用分类器最小化 softmax 损失（公式3）：

<img src="https://i.loli.net/2020/04/21/gPpFnJNcm14ojk6.png" alt="image-20200421102125834" style="zoom:50%;" />

实际上，使用 softmax 损失的不同变种来训练分类模型：

- additive margin：Feng Wang, Jian Cheng, Weiyang Liu, and Haijun Liu. **Additive margin softmax for face verification**. IEEE Signal Processing Letters, 25(7):926–930, 2018.
- feature $\ell2$ normalization： Rajeev Ranjan, Carlos D Castillo, and Rama Chellappa. **L2-constrained softmax loss for discriminative face verification**. arXiv preprint arXiv:1703.09507, 2017.
- arcface：Jiankang Deng, Jia Guo, Niannan Xue, and Stefanos Zafeiriou. **Arcface: Additive angular margin loss for deep face recognition**. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition, pages 4690– 4699, 2019.

#### KL-Divergence Regularization

公式 2 表明，在训练时所有特征嵌入都会被 $\pmb{\sigma}_i$ 破坏，这会让网络对所有样本都预测小的 $\pmb \mu_i$ 来抑制 $\mathbf{s}_i$ 的不稳定成分，这样公式 3 仍然能收敛，不过退退化成原始的确定性表示。

受 variational information bottleneck [1] 的启发，在优化时引入正则项：显式约束 $\mathcal{N}(\pmb \mu_i, \pmb \sigma_i)$ 为正态分布，者通过 KL 散度来度量：

<img src="https://i.loli.net/2020/04/21/AWohfxjNg9DPHSX.png" alt="image-20200421102221253" style="zoom:50%;" />

> Alexander A Alemi, Ian Fischer, Joshua V Dillon, and Kevin Murphy. **Deep variational information bottleneck**. In Proceedings of the International Conference on Learning Representations, 2017.

### Regression-based DUL for FR

#### Difficulty of Introducing Data Uncertainty Regression to FR

由于在人脸的映射空间 $\mathcal{X \rightarrow Y}$ 中，$\mathcal{X}$ 是连续的，但 $\mathcal{Y}$ 是离散的，因此不能直接应用数据不确定性回归。

#### Constructing New Mapping Space for FR

我们为人脸数据构建了连续的 target space，这与原始的离散 target space 几乎等价。步骤如下：

1. 预训练基于分类的确定性 FR 模型。
2. 利用分类模型的分类层 $\mathcal W \in \mathbb R^{D\times C}$ 作为 expected target vector。其中 $D$ 是嵌入的维度，$C$ 是训练集的类别数。
3. 由于每个 $\mathbf w_i \in \mathcal W$ 可以看作具有相同类别的嵌入的 typical center，$\{\mathcal{X,W}\}$ 可以看作新的 equivalent mapping space。$\{\mathcal{X,W}\}$ 同样具有固有噪声。
4. 我们可以建立从 $\mathbf x_i \in \mathcal X$ 到 $\mathbf w_i \in \mathcal W$ 的映射：$\mathbf w_i = f(\mathbf x_i) + n(\mathbf x_i)$。

#### Distributional Representation

接下来通过 data uncertainty regression 估计 $f(\mathbf x_i)$ 和 $n(\mathbf x_i)$：将 $\mathbf w_c$ 视作 target，我们应为每个 $\mathbf x_i$ 最大化如下 likelihood：

<img src="https://i.loli.net/2020/04/21/cxvXulP2NjOUdrI.png" alt="image-20200421102257681" style="zoom:50%;" />

实际上，我们采用 log likelihood：

<img src="https://i.loli.net/2020/04/21/AuCJilcwqbX1yot.png" alt="image-20200421102318903" style="zoom:50%;" />

likelihood 最大化改写为损失函数最小化：

<img src="https://i.loli.net/2020/04/21/sRmZr2bPhVSEovF.png" alt="image-20200421102453700" style="zoom:50%;" />

