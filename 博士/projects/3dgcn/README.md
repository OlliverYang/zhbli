# TDDO

1. （已解决）输入顺序不同，最终预测结果应该是相同的。-> Global Average Pooling 应该可以实现这一功能。该操作往往位于全连接层之前。本代码中是存在这一操作的。
2. 减去中心值真的好吗？优点1：学习相对关系，避免绝对坐标影响。缺点1：图像卷积中，没有把中间像素减去。缺点2：最重要的中心点变成0了，未必好。因此试一下不减去中间值的效果。
3. 固定随机种子。
4. 邻居不含自己？那卷积/池化还有什么用呢？
5. 用有步长的卷积代替池化。

# 运行环境

pytorch1.4_python3.7

# 数据集准备

```
cd root/datasets
wget http://modelnet.cs.princeton.edu/ModelNet40.zip
unzip ModelNet40.zip
cd root/classification
python sample_points.py -source ../dataset/ModelNet40 -target ../dataset/ModelNet40_1024/ -point_num 1024
```

# 训练

```
cd root/classification
python main.py -mode train -support 1 -neighbor 20 -cuda 0 -epoch 100 -bs 8 -dataset /home/etvuz/projects/3dgcn/dataset/ModelNet40_1024 -record record.log  -save model.pkl
```

## 训练时间

分类任务约 8 小时，分割任务约 1 天。

## 可复现性

虽然会下降几个点，但大体上与论文结果相似。

## 训练结果

Epoch 100 | Tain Loss: 2.97505 Train Acc: 0.215 | Test Loss: 4.20887 Test Acc: 0.074 | Best Acc: 0.135
增加网络层数 Epoch 16 | Tain Loss: 3.36130 Train Acc: 0.141 | Test Loss: 4.32781 Test Acc: 0.042 | Best Acc: 0.073
           Epoch 31 | Tain Loss: 3.33607 Train Acc: 0.146 | Test Loss: 3.65223 Test Acc: 0.041 | Best Acc: 0.073
dummy 8     neighbor=2                      epoch   1 step  1000 | avg loss: 0.13910 | avg acc: 0.92950
dummy 16    neighbor=2                      epoch   1 step  2800 | avg loss: 0.16309 | avg acc: 0.92875
dummy 32    neighbor=2                      epoch   1 step  3200 | avg loss: 0.66319 | avg acc: 0.59000
dummy 32    neighbor=8                      epoch   1 step  4800 | avg loss: 0.18934 | avg acc: 0.90865
dummy 64    neighbor=8                      epoch   1 step  2800 | avg loss: 0.21895 | avg acc: 0.90089
dummy 128   neighbor=2                      epoch   1 step  1800 | avg loss: 0.70532 | avg acc: 0.50750
dummy 128   neighbor=8                      epoch   1 step  2400 | avg loss: 0.67042 | avg acc: 0.58458
dummy 128   neighbor=16                     epoch   1 step  1600 | avg loss: 0.25228 | avg acc: 0.91312 说明16比8好。
dummy 256   neighbor=16                     epoch   1 step  1000 | avg loss: 0.14970 | avg acc: 0.91100
dummy 512   neighbor=2                      epoch   1 step  1400 | avg loss: 0.70345 | avg acc: 0.51393
dummy 512   neighbor=16                     epoch   1 step  3200 | avg loss: 0.38822 | avg acc: 0.82828
dummy 512   neighbor=32                     epoch   1 step  2200 | avg loss: 0.23231 | avg acc: 0.90386 说明32比16好。
dummy 1024  neighbor=32   pooling_rate=1    epoch   1 step  1000 | avg loss: 0.25382 | avg acc: 0.91000
dummy 1024  neighbor=32   pooling_rate=1    epoch   1 step  1000 | avg loss: 0.40909 | avg acc: 0.82450 重复实验。说明 pooling_rate=1 与删除所有池化层等效。
dummy 1024  neighbor=32   pooling_rate=2    epoch   1 step  4800 | avg loss: 0.51565 | avg acc: 0.76219 说明池化降低效果。
dummy 1024  neighbor=32   删除所有池化层。。                                 epoch   1 step  1600 | avg loss: 0.24027 | avg acc: 0.90844
dummy 1024  neighbor=32   batch=2   pooling_rate=1    取消减去相对位置 改为级联中心坐标   epoch   1 step   400 | avg loss: 0.34476 | avg acc: 0.94125 性能明显提升。 
dummy 1024  neighbor=16   batch=16  删除所有池化层。     取消减去相对位置 改为级联中心坐标   epoch   1 step    50 | avg loss: 0.72597 | avg acc: 0.49625 貌似训练不动。 
dummy 1024  neighbor=16   batch=4   删除所有池化层。     取消减去相对位置 改为级联中心坐标   epoch   1 step   400 | avg loss: 0.45724 | avg acc: 0.82875
                                                                                    epoch   1 step   500 | avg loss: 0.43779 | avg acc: 0.85000
                                                                                    epoch   1 step   600 | avg loss: 0.43208 | avg acc: 0.84917
dummy 1024  neighbor=16   batch=2   删除所有池化层。     取消减去相对位置 改为级联中心坐标   epoch   1 step   400 | avg loss: 0.23224 | avg acc: 0.89250
                                                                                    epoch   1 step   500 | avg loss: 0.19519 | avg acc: 0.91400
                                                                                    epoch   1 step   600 | avg loss: 0.16881 | avg acc: 0.92833
dummy 1024  neighbor=32   batch=2   删除所有池化层。     取消减去相对位置 改为级联中心坐标   epoch   1 step   200 | avg loss: 0.28339 | avg acc: 0.90250 再次说明邻居32比16好。
                                                                                    epoch   1 step   300 | avg loss: 0.21954 | avg acc: 0.93500
                                                                                    epoch   1 step   400 | avg loss: 0.18060 | avg acc: 0.95125
dummy 1024  neighbor=64   batch=2   删除所有池化层。     取消减去相对位置 改为级联中心坐标   epoch   1 step   100 | avg loss: 0.36422 | avg acc: 0.91500 说明邻居64比32好。
                                                                                    epoch   1 step   210 | avg loss: 0.27674 | avg acc: 0.95952
dummy 1024  neighbor=32   batch=4   删除所有池化层。     取消减去相对位置 改为级联中心坐标   epoch   1 step   100 | avg loss: 0.72168 | avg acc: 0.47500
                                                                                    epoch   1 step   200 | avg loss: 0.68917 | avg acc: 0.53750
                                                                                    epoch   1 step   300 | avg loss: 0.64144 | avg acc: 0.62500
                                                                                    epoch   1 step   400 | avg loss: 0.58483 | avg acc: 0.70375
                                                                                    epoch   1 step   500 | avg loss: 0.54100 | avg acc: 0.75750
                                                                                    epoch   1 step   600 | avg loss: 0.49991 | avg acc: 0.79583
                                                                                                            epoch   1 step   700 | avg loss: 0.45956 | avg acc: 0.81929
                                                                                                            epoch   1 step  1200 | avg loss: 0.37276 | avg acc: 0.88354
dummy 1024  neighbor=32   batch=4   删除所有池化层。     取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.33400 | avg acc: 0.87250 性能明显提升。
                                                                                                            epoch   1 step   200 | avg loss: 0.24841 | avg acc: 0.93000
dummy 1024  neighbor=32   batch=8   删除所有池化层。     取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.62129 | avg acc: 0.63125 如果你想，等了好久，100 次之后才0.63，训练不好了，那你的这种想法就错了。
                                                                                                            epoch   1 step   200 | avg loss: 0.33445 | avg acc: 0.81563
                                                                                                            epoch   1 step   300 | avg loss: 0.22585 | avg acc: 0.87708
                                                                                                            epoch   1 step   400 | avg loss: 0.17110 | avg acc: 0.90781 及格。
dummy 1024  neighbor=32   batch=8   pooling_rate=2    取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.71845 | avg acc: 0.50000
                                                                                                            epoch   1 step   200 | avg loss: 0.71167 | avg acc: 0.51250
                                                                                                            epoch   1 step   300 | avg loss: 0.70944 | avg acc: 0.51708
                                                                                                            epoch   1 step   400 | avg loss: 0.70706 | avg acc: 0.52063
                                                                                                            epoch   1 step   500 | avg loss: 0.70255 | avg acc: 0.52675
                                                                                                            epoch   1 step   600 | avg loss: 0.70212 | avg acc: 0.52958
                                                                                                            epoch   1 step   700 | avg loss: 0.69918 | avg acc: 0.53482
                                                                                                            epoch   1 step  2000 | avg loss: 0.28644 | avg acc: 0.82800 加了池化明显不好。
dummy 1024  neighbor=32   batch=8   使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.73268 | avg acc: 0.47625
                                                                                                            epoch   1 step   200 | avg loss: 0.71625 | avg acc: 0.50875
                                                                                                            epoch   1 step   400 | avg loss: 0.69033 | avg acc: 0.54406
                                                                                                            epoch   1 step   800 | avg loss: 0.55156 | avg acc: 0.67000 不如neighbor=16好。
dummy 1024  neighbor=16   batch=8   使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.70853 | avg acc: 0.53375
                                                                                                            epoch   1 step   200 | avg loss: 0.67941 | avg acc: 0.56875
                                                                                                            epoch   1 step   400 | avg loss: 0.48520 | avg acc: 0.74438
                                                                                                            epoch   1 step   800 | avg loss: 0.25810 | avg acc: 0.87156
dummy 1024  neighbor=8    batch=8   lr=0.0001   使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.71915 | avg acc: 0.49625
                                                                                                                        epoch   1 step   200 | avg loss: 0.71478 | avg acc: 0.50687
                                                                                                                        epoch   1 step   400 | avg loss: 0.71731 | avg acc: 0.50438 前 400 结果几乎没变化
                                                                                                                        epoch   1 step   800 | avg loss: 0.50396 | avg acc: 0.69125
                                                                                                                        epoch   1 step  1030 | avg loss: 0.20102 | avg acc: 0.90024 及格。
dummy 1024  neighbor=16    batch=8   lr=0.001    使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.71866 | avg acc: 0.51125
                                                                                                                        epoch   1 step   200 | avg loss: 0.72019 | avg acc: 0.50438
                                                                                                                        epoch   1 step   400 | avg loss: 0.71868 | avg acc: 0.50656 前 400 结果几乎不变。
dummy 1024  neighbor=16    batch=8   lr=0.001    使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居  epoch   1 step   100 | avg loss: 0.55596 | avg acc: 0.67625 重复实验
                                                                                                                        epoch   1 step   200 | avg loss: 0.32152 | avg acc: 0.82688 重复实验的结果，在收敛速度上差别很大。
                                                                                                                        epoch   1 step   400 | avg loss: 0.16418 | avg acc: 0.91312
                                                                                                                        epoch   1 step   800 | avg loss: 0.08257 | avg acc: 0.95656 效果非常好。
dummy 1024  neighbor=16    batch=8   lr=0.001  无随机性  使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居  epoch   1 step   100 | avg loss: 0.70383 | avg acc: 0.54375 重复实验。
                                                                                                                        epoch   1 step   200 | avg loss: 0.68881 | avg acc: 0.55812
                                                                                                                        epoch   1 step   400 | avg loss: 0.65819 | avg acc: 0.59406
                                                                                                                        epoch   1 step   800 | avg loss: 0.56377 | avg acc: 0.67063
                                                                                                                        epoch   1 step  1230 | avg loss: 0.46526 | avg acc: 0.73709 不好。
dummy 1024  neighbor=16    batch=8   lr=0.0001 无随机性    使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居  epoch   1 step  1230 | avg loss: 0.41363 | avg acc: 0.74228 不好
dummy 1024  neighbor=16    batch=8   lr=0.0001 无随机性    删除卷积层         取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居  epoch   1 step   610 | avg loss: 0.26577 | avg acc: 0.84508 不如0.001好
dummy 1024  neighbor=16    batch=8   lr=0.001 无随机性     删除卷积层          取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居  epoch   1 step   610 | avg loss: 0.17386 | avg acc: 0.90717 比0.0001好 data_stamp: 0.9999923706054688
                                                                                                                                epoch   1 step   750 | avg loss: 0.14143 | avg acc: 0.92450

dummy 1024  neighbor=16    batch=8   lr=0.0001  使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居   epoch   1 step   100 | avg loss: 0.72085 | avg acc: 0.46500
                                                                                                                        epoch   1 step   200 | avg loss: 0.71178 | avg acc: 0.48688
                                                                                                                        epoch   1 step   400 | avg loss: 0.71048 | avg acc: 0.49531 结果几乎不变。
dummy 1024  neighbor=16    batch=16   lr=0.001  使用步长卷积代池化   取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居  epoch   1 step   100 | avg loss: 0.67735 | avg acc: 0.56437
                                                                                                                        epoch   1 step   200 | avg loss: 0.63035 | avg acc: 0.62531
                                                                                                                        epoch   1 step   400 | avg loss: 0.63685 | avg acc: 0.62406
                                                                                                                        epoch   1 step   800 | avg loss: 0.58070 | avg acc: 0.67000
                                                                                                                        epoch   1 step  1360 | avg loss: 0.59264 | avg acc: 0.65253
-------------------------------------------以下略去 dummy 1024 取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居----------------
neighbor=16 batch=16    lr=0.001 no_pooling 每个block仅一个卷积                    100 | avg loss: 0.60694 | avg acc: 0.65125  data_stamp: 0.9999923706054688 24471.76953125
                                                                                200 | avg loss: 0.31789 | avg acc: 0.82219
                                                                                400 | avg loss: 0.15927 | avg acc: 0.91109  结论：效果很理想。

neighbor=16 batch=16    lr=0.001 no_pooling 第一个block4个卷积，其余block1个卷积    100 | avg loss: 0.71675 | avg acc: 0.51438   data_stamp: 0.9999923706054688 24471.76953125
                                                                                200 | avg loss: 0.69785 | avg acc: 0.53187
                                                                                400 | avg loss: 0.69891 | avg acc: 0.53734  结论：非常奇怪，增加卷积层反而不好。

neighbor=8  batch=32    lr=0.001    no_pooling 每个block仅一个卷积                 100 | avg loss: 0.48556 | avg acc: 0.71625 data_stamp: 0.9999814033508301 49123.4453125
                                                                                200 | avg loss: 0.24364 | avg acc: 0.85813
                                                                                400 | avg loss: 0.12211 | avg acc: 0.92906 结论：效果很理想。

neighbor=4  batch=64    lr=0.001    no_pooling 每个block仅一个卷积                 100 | avg loss: 0.49561 | avg acc: 0.70234  data_stamp: 0.9999972581863403 98198.875
                                                                                200 | avg loss: 0.24824 | avg acc: 0.85117
                                                                                400 | avg loss: 0.12428 | avg acc: 0.92559  结论：效果很理想。
-------------------------------------------以下改为真实数据 略去学习率lr=0.001 取消减去相对位置 改为级联中心坐标   找点的邻居而不是特征的邻居----------------
neighbor=4  batch=64                no_pooling 每个block仅一个卷积                 100 | avg loss: 3.45500 | avg acc: 0.11406  结论：程序bug死。

neighbor=4  batch=32                no_pooling 每个block仅一个卷积                 100 | avg loss: 3.45630 | avg acc: 0.11281
                                                                                200 | avg loss: 3.41580 | avg acc: 0.12375
                                                                                epoch   2 step   100 | avg loss: 3.37902 | avg acc: 0.12375 结论：在acc=12左右就几乎不涨了。

neighbor=4  batch=8                 no_pooling 每个block仅一个卷积                 100 | avg loss: 3.45062 | avg acc: 0.13375
                                                                                200 | avg loss: 3.45842 | avg acc: 0.11438
                                                                                400 | avg loss: 3.44299 | avg acc: 0.12219
                                                                                800 | avg loss: 3.39614 | avg acc: 0.13328  结论：在acc=13左右就几乎不涨了。

neighbor=4  batch=8                 no_pooling  第一个block4个卷积，其余block1个卷积 epoch   1 step   200 | avg loss: 3.48081 | avg acc: 0.10187
                                                                                epoch   1 step   400 | avg loss: 3.46271 | avg acc: 0.11469 
                                                                                epoch   1 step   800 | avg loss: 3.40886 | avg acc: 0.12875
neighbor=4  batch=8                 第一次进行步长卷积   第一个block4个卷积，其余block1个卷积        epoch   1 step   100 | avg loss: 3.45818 | avg acc: 0.11875
                                                                                            epoch   1 step   200 | avg loss: 3.46502 | avg acc: 0.10625
                                                                                            epoch   1 step   400 | avg loss: 3.44572 | avg acc: 0.11625
                                                                                            epoch   1 step   800 | avg loss: 3.40614 | avg acc: 0.12703 结论：进行池化也没啥影响。
# 测试

# TODO
1. 测试代码能否跑通
2. （不紧急）写 tensorboard
3. （不紧急）跑原始代码的结果
4. （调整kennel大小）不紧急，因为要和原始算法形成公平比较