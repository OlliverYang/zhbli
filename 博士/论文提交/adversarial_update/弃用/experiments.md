#### 我们的修改是不可察觉的：

<img src="https://i.loli.net/2020/05/03/ALdcw79a1touTHe.png" style="zoom:50%;" />

#### 我们的修改对 heatmap 的影响：

![got_test_8_2_adv](https://i.loli.net/2020/05/03/qeFhBgKxCJG8XZW.jpg)

![got_test_8_2_origin](https://i.loli.net/2020/05/03/Suwp1lHgcQC2I87.jpg)

#### 在各个数据集上做实验

GOT-10k

| AO    | SR0.50 | SR0.75 | Hz        | loop | epsilon |
| ----- | ------ | ------ | --------- | ---- | ------- |
| 0.617 | 0.748  | 0.475  | 66.99 fps | 2    | 0.05    |

VOT2018：

| A     | R     | EAO   | Hz        | loop | epsilon |
| ----- | ----- | ----- | --------- | ---- | ------- |
| 0.591 | 0.187 | 0.438 | 59.11 fps | 2    | 0.05    |

OTB-15

| success_score | precision_score | success_rate | FPS   | loop | epsilon |
| ------------- | --------------- | ------------ | ----- | ---- | ------- |
| 0.685         | 0.894           | 0.864        | 64.57 | 2    | 0.05    |

TrackingNet

#### ~~对各种孪生网络做修改~~

#### 对迭代次数、学习率的超参调整

#### 对不同对抗样本生成方法效果的实验

#### 可视化逐渐变好的 loss

#### 对抗样本对梯度的影响

<img src="https://i.loli.net/2020/05/07/nfwg5DbMm6RykLd.png" alt="image-20200507161959068" style="zoom:50%;" />

#### 消融实验：优化不同 loss——分类/回归/...

#### 对 siamfc 系列算法列出第一帧的 IoU

