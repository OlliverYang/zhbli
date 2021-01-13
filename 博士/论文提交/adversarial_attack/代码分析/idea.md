# 优点

只需要跟自己比。

不需要长期训练。

不需要设计防御算法。（多篇论文中，大多数都没有设计防御算法）

比较新且有价值。

做的人比较少。

# 算法设计

### 通用扰动

代码：https://github.com/ferjad/Universal_Adversarial_Perturbation_pytorch.git

论文：Universal adversarial perturbations

### 对抗补丁

代码：https://github.com/Trusted-AI/adversarial-robustness-toolbox

论文：DPATCH: An Adversarial Patch Attack on Object Detectors

# 可用代码

### https://github.com/Trusted-AI/adversarial-robustness-toolbox/examples/application_object_detection.py

目标检测+FastGradientMethod

pytorch

**对抗后仍能检测出来。**

### https://github.com/Trusted-AI/adversarial-robustness-toolbox/examples/attack_adversarial_patch_tfv2.py

对抗补丁

**tensorflow**（可以考虑移植成pytorch）

结果良好

### https://github.com/Trusted-AI/adversarial-robustness-toolbox/art/attacks/evasion/universal_perturbation.py

通用扰动

**还不会用**

### https://github.com/Trusted-AI/adversarial-robustness-toolbox/art/attacks/evasion/dpatch.py

目标检测+对抗补丁

**还不会用**

### https://github.com/ferjad/Universal_Adversarial_Perturbation_pytorch.git

通用扰动+deepfool

pytorch

**不知道如何将deepfool应用到其他任务**（可考虑使用其他对抗算法）

### https://github.com/veralauee/DPatch.git

目标检测+对抗补丁

pytorch

**据说难以复现**

### https://github.com/jhayes14/adversarial-patch

对抗补丁

pytorch

**等待数据库下载**

### https://github.com/DSE-MSU/DeepRobust/blob/master/examples/image/test_onepixel.py

单像素攻击

pytorch

**ModuleNotFoundError: No module named 'DeepRobust'**

### https://github.com/bethgelab/foolbox

**没发现太有用的算法**

# 实验设计

可视化扰动

消融实验

- 使用优化算法 vs 使用生成算法 vs 结合
- 攻击模板 vs 攻击搜索图像 vs 结合
- 攻击分类分支 vs 攻击回归分支 vs 结合
- 攻击多个数据库：got，vot，otb等
- 攻击多个数据库
- 对抗补丁在数据库之间的迁移性/黑盒攻击
- 对抗补丁的形状：原型/方形
- 对抗补丁尺寸、位置、角度变化/不变
- 对抗补丁位置，放在固定点，还是在搜索区域上随机，还是在目标位置外随机？
- 不同 batch size 对训练的影响

# 相关论文——目标跟踪

### [CVPR2020] Cooling-Shrinking Attack: Blinding the Tracker with Imperceptible Noises

冷却 heatmap 中存在目标的 hot regions。

缩小目标边框。

**优化方式：**GAN

### [ECCV2020] Efficient Adversarial Attacks for Visual Object Tracking

希望非中心区域的最大响应比中心区域的最大响应大：

<img src="https://i.loli.net/2020/08/14/xaEjvy23c1owSrO.png" alt="image-20200814111413309" style="zoom:50%;" />

希望非中心区域的最大响应位置距离中心区域的最大相应位置更远：

<img src="https://i.loli.net/2020/08/14/qaoWkJwDYt7Vfbg.png" alt="image-20200814111442203" style="zoom:50%;" />

**优化方式：**GAN

### [ECCV2020] Robust Tracking against Adversarial Attacks

不论使用真实标签还是伪标签，分类/回归损失都相同：

<img src="https://i.loli.net/2020/08/14/uvYRcZ3j2KsQX8k.png" alt="image-20200814133314604" style="zoom:50%;" />

**优化方式：**BIM

### [CVPR2020] One-shot Adversarial Attacks on Visual Tracking with Dual Attention

抑制具有高置信度的候选并激发具有中等置信度的候选：

<img src="https://i.loli.net/2020/08/14/N1JbGg5djOFiM4C.png" alt="image-20200814153929661" style="zoom:50%;" />

将z和z*的特征图的欧氏距离最大化：

<img src="https://i.loli.net/2020/08/14/l54B7kZoFebw3fM.png" alt="image-20200814154707872" style="zoom:50%;" />

**优化方式：**we use Adam optimizer [13] to minimize the loss by iteratively perturbing the pixels along the gradient directions within the patch area.

### [ICCV2019] Physical Adversarial Textures That Fool Visual Object Tracking

具体来说，我们考虑以下损失：

<img src="https://i.loli.net/2020/08/15/aNS9iZy2fbPrcoM.png" alt="image-20200815133718064" style="zoom:50%;" />

含义是：增加GOTURN的训练损失。

<img src="https://i.loli.net/2020/08/15/FE5fYwR4sOqbLt1.png" alt="image-20200815133819100" style="zoom:50%;" />

含义是：让预测边框固定到搜索区域的左下角。

<img src="https://i.loli.net/2020/08/15/sQJ4GuBf7Lk2Z9o.png" alt="image-20200815134019673" style="zoom:50%;" />

含义是：让预测边框固定到搜索区域的中心。

<img src="https://i.loli.net/2020/08/15/HdanhXjOoIiKgxQ.png" alt="image-20200815134110642" style="zoom:50%;" />

含义是：让预测边框变得最大。

<img src="https://i.loli.net/2020/08/15/UzkX1ZxH42BW5vQ.png" alt="image-20200815134200243" style="zoom:50%;" />

含义是：让预测边框尽量小。

<img src="https://i.loli.net/2020/08/15/oFUesn1BiMayGND.png" alt="image-20200815134341213" style="zoom:50%;" />

含义是：让预测边框尽量大。

**优化方式：**BIM

### [ECCV2020] SPARK: Spatial-aware Online Incremental Attack Against Visual Tracking

真实框的得分要比错误框的得分低。

<img src="https://i.loli.net/2020/08/15/bgdKwX1LcMG4Jfi.png" alt="image-20200815142208120" style="zoom:50%;" />

**优化方式：**BIM

### [ICASSP2020] Hijacking Tracker: A Powerful Adversarial Attack on Visual Tracking

具有错误位置的边框的得分高于真实目标框的得分：

<img src="https://i.loli.net/2020/08/15/6LDyl948UBorRq5.png" alt="image-20200815154036766" style="zoom:50%;" />

具有错误形状的边框的得分高于真实目标框的得分：

<img src="https://i.loli.net/2020/08/15/JGc7pt9IATULYPu.png" alt="image-20200815154410627" style="zoom:50%;" />

**优化方式：**BIM

### [arXiv1909] STA: Adversarial Attacks on Siamese Trackers

将所有anchors都分类为背景：

<img src="https://i.loli.net/2020/08/15/PdhMZVk1Fvo6yr8.png" alt="image-20200815163309146" style="zoom:50%;" />

**优化方式：**BIM

# 相关论文——图像分割

### [ICCV2017] Universal Adversarial Perturbations Against Semantic Image Segmentation

优化方式：BIM

### [ICCV2017] Adversarial Examples for Semantic Segmentation and Object Detection

优化方式：BIM

### [arXiv1910] AdvSPADE: Realistic Unrestricted Attacks for Semantic Segmentation

优化方式：GAN

### [ICLRW2017] ADVERSARIAL EXAMPLES FOR SEMANTIC IMAGE SEGMENTATION

优化方式：BIM

# 相关论文——目标检测

### [arXiv1902] Daedalus:  Breaking Non-Maximum Suppression in Object Detection via Adversarial Examples

优化方式：BIM

### [arXiv1806] DPatch: An Adversarial Patch Attack on Object Detectors

### Attacking Object Detectors via Imperceptible Patches on Background

### Category-wise Attack: Transferable Adversarial Examples for Anchor Free Object Detection

### Robust adversarial perturbation on deep proposal-based models

### [UEA]Transferable adversarial attacks for image and video object detection

### Pick-Object-Attack: Type-Specific Adversarial Attack for Object Detection

### Membership Inference Attacks Against Object Detection Models

### Towards Adversarially Robust Object Detection

### TOG: Targeted Adversarial Objectness Gradient Attacks on Real-time Object Detection Systems

### Attack on Multi-Node Attention for Object Detection

### On Physical Adversarial Patches for Object Detection

