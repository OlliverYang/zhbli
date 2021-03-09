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


# 测试

# TODO
1. 测试代码能否跑通
2. （不紧急）写 tensorboard
3. （不紧急）跑原始代码的结果
4. （调整kennel大小）不紧急，因为要和原始算法形成公平比较