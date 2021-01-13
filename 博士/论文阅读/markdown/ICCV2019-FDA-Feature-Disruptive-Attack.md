---
title: '[ICCV2019] FDA: Feature Disruptive Attack'
date: 2020-08-16 19:07:04
tags:
- Adversarial Attack
mathjax: true
---

## Related Work

自 [49] 提出对抗样本概念以来，多个工作 [22, 38, 29, 16, 4, 33, 13, 10] 提出了生成对抗样本的不同方法。

> [49] Christian Szegedy, Wojciech Zaremba, Ilya Sutskever, Joan Bruna, Dumitru Erhan, Ian J. Goodfellow, and Rob Fergus. Intriguing properties of neural networks. arXiv preprint arXiv:1312.6199, 2013.
>
> [22] Ian J. Goodfellow, Jonathon Shlens, and Christian Szegedy. Explaining and harnessing adversarial examples. arXiv preprint arXiv:1412.6572, 2014.
>
> [38] Seyed-Mohsen Moosavi-Dezfooli, Alhussein Fawzi, and Pascal Frossard. Deepfool: A simple and accurate method to fool deep neural networks. In IEEE Computer Vision and Pattern Recognition (CVPR), 2016.
>
> [29] Alexey Kurakin, Ian Goodfellow, and Samy Bengio. Adversarial examples in the physical world. arXiv preprint arXiv:1607.02533, 2016.
>
> [16] Yinpeng Dong, Fangzhou Liao, Tianyu Pang, Hang Su, Jun Zhu, Xiaolin Hu, and Jianguo Li. Boosting adversarial attacks with momentum. In The IEEE Conference on Computer Vision and Pattern Recognition (CVPR), June 2018.
>
> [4] Anish Athalye, Nicholas Carlini, and David Wagner. Obfuscated gradients give a false sense of security: Circumventing defenses to adversarial examples. In Proceedings of the 35th International Conference on Machine Learning, ICML, July 2018.
>
> [33] Aleksander Madry, Aleksandar Makelov, Ludwig Schmidt, Dimitris Tsipras, and Adrian Vladu. Towards deep learning models resistant to adversarial attacks. In International Conference on Learning Representations (ICLR), 2018.
>
> [13] Nicholas Carlini and David Wagner. Towards evaluating the robustness of neural networks. arXiv preprint arXiv:1608.04644, 2016.
>
> [10] Wieland Brendel, Jonas Rauber, and Matthias Bethge. Decision-based adversarial attacks: Reliable attacks against black-box machine learning models. In International Conference on Learning Representations (ICLR), 2018.



同时， [36, 57, 6] 探索了对抗样本在其他任务上的应用。

> [36] Jan Hendrik Metzen, Mummadi Chaithanya Kumar, Thomas Brox, and Volker Fischer. Universal adversarial perturbations against semantic image segmentation. In International Conference on Computer Vision (ICCV), 2017.
>
> [57] Cihang Xie, Jianyu Wang, Zhishuai Zhang, Yuyin Zhou, Lingxi Xie, and Alan Yuille. Adversarial examples for semantic segmentation and object detection. In International Conference on Computer Vision (ICCV), 2017.
>
> [6] Vahid Behzadan and Arslan Munir. Vulnerability of deep reinforcement learning to policy induction attacks. arXiv preprint arXiv:1701:04143, 2017.

与本文最接近的方法是 [59, 43, 41]。

> [59] Wen Zhou, Xin Hou, Yongjun Chen, Mengyun Tang, Xiangqi Huang, Xiang Gan, and Yong Yang. Transferable adversarial perturbations. In The European Conference on Computer Vision (ECCV), September 2018.
>
> [43] Sara Sabour, Yanshuai Cao, Fartash Faghri, and David J Fleet. Adversarial manipulation of deep representations. arXiv preprint arXiv:1511.05122, 2015.
>
> [41] Konda Reddy Mopuri, Aditya Ganeshan, and R. Venkatesh Babu. Generalizable data-free objective for crafting universal adversarial perturbations. IEEE Transactions on Pattern Analysis and Machine Intelligence, pages 1–1, 2018.

## Proposed attack

本文提出的攻击方法为 Feature Disruptive Attack (FDA)，用于产生破坏 CNN 内部表示的扰动。

对于第i层$l_i$，我们的 layer objective L（希望L增加）为：

<img src="https://i.loli.net/2020/08/17/7ELgSf9mN3tcqMl.png" alt="image-20200816191941294" style="zoom:50%;" />

$l_i(\tilde x)_{N_j}$ 表示层 $l_i(\tilde x)$ 的第 $N_j$ 个值。$S_i$ 表示支持当前预测的激活的集合。

D是单调递增函数，本文中定义为输入$l_i(\tilde x)$ 的二范数。

上述公式的含义：让不支持当前预测的激活值尽量大，让支持当前预测的激活值尽量小。

寻找 $S_i$ 是不平凡的。不过，虽然高激活值未必都支持当前预测，但这是有效的近似。定义支持集 $S_i$ 为：

<img src="https://i.loli.net/2020/08/17/XmJlp6gH4uN7tBK.png" alt="image-20200817100815074" style="zoom:50%;" />

实验发现，$spatial-mean(l_i(x)) = C(h,w)$ (mean across channels) 是最有效的近似。 

因此，layer objective L 为：

<img src="https://i.loli.net/2020/08/17/hCX3ftZPaAkj96e.png" alt="image-20200817101313198" style="zoom:50%;" />	

我们在每个非线性层执行此优化：

<img src="https://i.loli.net/2020/08/17/LDJ3X9NQcfv7dK5.png" alt="image-20200817101423503" style="zoom:50%;" />