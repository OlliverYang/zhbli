## 两种跟踪算法

DCF 跟踪器：
$$
s_\theta(y,x)=(w_\theta * \phi(x))(y)
$$
孪生网络跟踪器：
$$
s_\theta(y,x)=(\phi_\theta(z) * \phi(x))(y)
$$

## 模型更新的过程

- DCF 跟踪器——更新 $w_\theta$。
- 孪生网络跟踪器——跟新 $\phi_\theta$。
- 本文——更新 $z$。

## 对抗样本

Basic Iterative Method：
$$
x_0^{adv} = \pmb X, x_{N+1}^{adv} = Clip_{X,\epsilon}\{\pmb X_N^{adv}+\alpha \text{ sign}(\nabla_X L(\pmb X_N^{adv},y_{true}))\}
$$

通过对输入图像进行难以察觉的修改，使网络对输入进行错误分类。

Iterative Target Class Method：
$$
x_0^{adv} = \pmb X, x_{N+1}^{adv} = Clip_{X,\epsilon}\{\pmb X_N^{adv}-\alpha \text{ sign}(\nabla_X L(\pmb X_N^{adv},y_{target}))\}
$$
通过对输入图像进行难以察觉的修改，使网络对输入进行错误分类，并指定错分的类别为 $y_{target}$。

## 本文的方法

$$
z_0 = z, z_{N+1} = Clip_{z,\epsilon}\{z_N -\alpha \text{ sign}(\nabla_z L(z_N,y_{true}))\}
$$

目的是对模板 $z$ 进行修改。

## 特点

- 传统 model adaptation 算法的缺点：
  - 若使用 SGD，则需要多次迭代，速度慢。
  - 若不用 SGD，则需要设计复杂的优化方法。
- 本文提出的模型更新算法的优点：
  - 仅需修改模板 $z$ 的像素值，简单快速。
  - 不需要对离线训练的网络添加新层或修改离线训练参数，从而不破坏离线训练网络的优秀表示能力，并能防止过拟合。

## 实验

![image-20200508131001798](https://i.loli.net/2020/05/08/f7kl2WtCR9HIi1z.png)