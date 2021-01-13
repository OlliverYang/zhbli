### Method

跟踪问题是 confidence-based regression 问题 ，即给定 output-input pair $(y,x)$，学习一个函数 $s_\theta:\mathcal{Y\times X\rightarrow \mathbb R}$，预测一个 scalar confidence score $s_\theta(y,x)\rightarrow\mathbb R$。Final estimate $f(x)=y^*$ 预测如下：
$$
f(x) = \arg\max_{y\in \mathcal Y}s_\theta (y,x)
$$
输入：$\mathcal X$ 表示图像空间。$y$ 表示回归目标，可以是 spatial position，也可以是 entire target box。

优化：
$$
L(\theta;x_i,y_i)=\int_{\mathcal Y}\ell(s_\theta(y,x_i),a(y,y_i))\ \mathrm{d}x
$$
DCF 跟踪器：
$$
s_\theta(y,x)=(w_\theta * \phi(x))(y)
$$
其中 $w_\theta$ 是卷积核，$\phi(x)$ 是图像特征。DCF 的损失函数为 $\ell(s,a)=(s-a)^2$。几乎所有的 DCF 方法的 pseudo label 为 $a(y,y_i)=e^{-\frac{||y-y_i||^2}{2\sigma^2}}$。

孪生网络跟踪器：
$$
s_\theta(y,x)=(\phi_\theta(z) * \phi(x))(y)
$$
传统的方法更新 $\phi_\theta$，但是我们更新 $z$。

Basic Iterative Method：
$$
x_0^{adv} = \pmb X, x_{N+1}^{adv} = Clip_{X,\epsilon}\{\pmb X_N^{adv}+\alpha \text{ sign}(\nabla_X L(\pmb X_N^{adv},y_{true}))\}
$$

Iterative Target Class Method：
$$
x_0^{adv} = \pmb X, x_{N+1}^{adv} = Clip_{X,\epsilon}\{\pmb X_N^{adv}-\alpha \text{ sign}(\nabla_X L(\pmb X_N^{adv},y_{target}))\}
$$
我们的方法：
$$
z_0 = z, z_{N+1} = Clip_{z,\epsilon}\{z_N -\alpha \text{ sign}(\nabla_z L(z_N,y_{true}))\}
$$
其中 $L$ 表示损失函数。

SiamFC++ 损失函数：
$$
\begin{equation}
\begin{split}
L(\{p_{x,y}\},q_{x,y},\{\pmb t_{x,y}\}) &= \frac{1}{N_{\text{pos}}}\sum_{x,y}L_{\text{cls}}(p_{x,y},c^*_{x,y})\\
&+\frac{\lambda}{N_{\text{pos}}}\sum_{x,y}\pmb1_{\{c^*_{x,y}>0\}}L_{\text{quality}}(q_{x,y},q^*_{{x,y}})\\
&+\frac{\lambda}{N_{\text{pos}}}\sum_{x,y}\pmb1_{\{c^*_{x,y}>0\}}L_{\text{reg}}(\pmb t_{x,y},\pmb t^*_{{x,y}})
\end{split}
\end{equation}
$$

其中 $L_{\text{cls}}$ 是 focal loss。$L_{\text{quality}}$ 是用于 quality assessment 的 binary cross entropy (BCE) loss。$L_{reg}$ 是用于边框回归的 IoU loss。

$\pmb t^*=(l^*,t^*,r^*,b^*)$，位置 $(x,y)$ 的 regression target 是：
$$
\begin{equation}
\begin{split}
&l^*=(\lfloor\frac{s}{2}\rfloor+xs)-x_0,\ &t^*=(\lfloor\frac{s}{2}\rfloor+ys)-y_0\\
&r^*=x_1-(\lfloor\frac{s}{2}\rfloor+xs),\ &b^*=y_1-(\lfloor\frac{s}{2}\rfloor+ys)
\end{split}
\end{equation}
$$

使用 Prior Spatial Score (PSS) 进行 quality assessment：
$$
\text{PSS}^* = \sqrt{\frac{\min(l^*,r^*)}{\max(l^*,r^*)}\times\frac{\min(t^*,b^*)}{\min(t^*,b^*)}}
$$


### 优点

结果具有确定性，而非随机性。

对任意孪生网络都有用。

将对抗样本反向应用是很合适的。一方面，对于分类任务，已经训练的很好的，没必要用对抗样本提高分类得分，而且分类任务也不适合这么做。另一方面，跟踪中测试的可能是看不到的物体，因此需要做微调。对抗样本反向应用，就是做微调的过程。

改变权重的缺点是过拟合，但是我们的方法也许没有这一问题。

改变权重用梯度下降的话很难，或者设计复杂的优化方法，我们超简单。时间消耗可以忽略。

分析：与模板更新的关系；与模型更新的关系。

### 待读论文

Feature Denoising for Improving Adversarial Robustness