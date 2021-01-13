---
title: '[CVPR2016] DeepFool: a simple and accurate method to fool deep neural networks'
date: 2020-08-23 13:12:29
tags:
- CVPR2016
- Adversarial Attack
mathjax: true
---

##  DeepFool for binary classifiers

定义 $f:R^n\rightarrow R$ 是图像的两类分类器，$\hat k(x) = sign(f(x))$，$F=\{x:f(x)=0\}$。首先分析 $f$ 是线性分类器的情况：

<img src="https://i.loli.net/2020/08/24/GejKp2rxlbiNzEQ.png" alt="image-20200824191203168" style="zoom:50%;" />

定义 $f$ 在点 $x_0$ 的鲁棒性为 $\Delta(x_0,f)^2$，即 $x_0$ 到决策边界的距离：

<img src="https://i.loli.net/2020/08/23/e9YAjzF74EZDmd2.png" alt="image-20200823133306059" style="zoom:50%;" />

扰动的闭式解为：

<img src="https://i.loli.net/2020/08/23/O8bQsTNimoaGJjU.png" alt="image-20200823133421748" style="zoom:50%;" />

现在假设 $f$ 是通用的两类的可微的分类器，我们采用迭代方法来估计鲁棒性 $\Delta(x_0,f)$。具体来说，每次迭代时，$f$ 在当前点 $x_i$ 附近被认为是线性的，且该线性分类器的最小扰动为：

<img src="https://i.loli.net/2020/08/23/EjRwk2WvMlHdguy.png" alt="image-20200823133852937" style="zoom:50%;" />

第 $i$ 次迭代的扰动 $r_i$ 由前述闭式解计算，用于更新 $x_{i+1}$。当 $x_{i+1}$ 的分类符号改变时，终止迭代。

## DeepFool for multiclass classifiers

分类器有c个输出，c是类别数。因此，分类器被定义为：$f:R^n\rightarrow R^c$，分类通过如下方式进行：

<img src="https://i.loli.net/2020/08/24/ZqD6whGgTPdrc8U.png" alt="image-20200824185922651" style="zoom:50%;" />

其中$f_k(x)$是f(x)对应于第k类的输出。

与两类分类器类似，我们先分析线性分类器，再分析通用分类器。

### Affine multiclass classifier

定义分类器为：

<img src="https://i.loli.net/2020/08/24/gfKUwSHbzpJt2lC.png" alt="image-20200824191107547" style="zoom:50%;" />

最小扰动为：

<img src="https://i.loli.net/2020/08/24/opxzSnUshLjlWFg.png" alt="image-20200824190904363" style="zoom:50%;" />

其中$w_k$是矩阵W的第k列。

从几何上讲，上述问题对应于计算$x_0$和 the complement of the convex polyhedron P 的距离：

<img src="https://i.loli.net/2020/08/24/1NXWPlr7Q8tMETB.png" alt="image-20200824191509670" style="zoom:50%;" />

其中$x_0$位于P的内部。我们定义这个距离为$dist(x_0,P^c)$.多面体P定义了f的输出为$\hat k(x_0)$ 的区域，如下图所示：

<img src="https://i.loli.net/2020/08/24/aEYbjOFl6zJRDXf.png" alt="image-20200824191848430" style="zoom:50%;" />

该问题的闭式解的计算如下所示。

定义$\hat l(x_0)$是到P的边界最近的超平面（即上图的$F_3$）：

<img src="https://i.loli.net/2020/08/24/Zb4RWHsOmvGyjqA.png" alt="image-20200824192222232" style="zoom:50%;" />

最小扰动为：

<img src="https://i.loli.net/2020/08/24/2iytpDK3eY18MvL.png" alt="image-20200824192426135" style="zoom:50%;" />

换句话说，我们寻找$x_0$到P的表面的最近的投影。

### General classifier

对于通用的非线性分类器，P不再是多面体。我们将第i次迭代时的$P_i$近似为多面体$\tilde P_i$：

<img src="https://i.loli.net/2020/08/24/lHPAVoBUNQpMFYd.png" alt="image-20200824192825580" style="zoom:50%;" />