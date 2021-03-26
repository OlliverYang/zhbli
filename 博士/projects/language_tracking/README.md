# TODO

改为全图输入

看看 feature crop 怎么回事

看看 offset/stride 那块啥意思

可视化 GT

单图是否收敛？会收敛，但是很慢。

# 我们的修改

负样本对为 0

# TODO

取消随机性

可视化每层权重的均值和方差

语言向量特征归一化 .norm，图像特征也归一化。
加了语言归一化后，收敛更快。

因为背景变多了，所以进行前背景平衡。

# 归一化对单图训练收敛速度的影响（seed=31415926）

均后端归一化
epoch 0, lr: 1.4e-04, cls: 1.351, ctr: 0.159, reg: 11.140, iou: 0.035, data: 3.5 debug 128
epoch 0, lr: 2.7e-04, cls: 0.894, ctr: 0.152, reg: 3.618, iou: 0.330, data: 3.8e debug 256
epoch 0, lr: 5.5e-04, cls: 0.745, ctr: 0.131, reg: 3.107, iou: 0.402, data: 3.8e debug 512 结论：不如仅前端归一化语言好

仅前端归一化语言
epoch 0, lr: 1.4e-04, cls: 1.352, ctr: 0.159, reg: 11.134, iou: 0.035, data: 2.2 debug 128
epoch 0, lr: 2.7e-04, cls: 0.894, ctr: 0.152, reg: 2.549, iou: 0.447, data: 2.3e debug 256
epoch 0, lr: 5.5e-04, cls: 0.121, ctr: 0.003, reg: 0.449, iou: 0.864, data: 1.4e debug 512

前端归一化语言和图像特征
epoch 0, lr: 5.5e-04, cls: 0.119, ctr: 0.003, reg: 0.784, iou: 0.779, data: 1.5e debug 512 结论：不如仅前端归一化语言好
epoch 0, lr: 1.1e-03, cls: 0.026, ctr: 0.000, reg: 0.171, iou: 0.945, data: 1.5e debug 1024

# 正负样本均衡对单图收敛速度的影响（seed=31415926，仅前端归一化)。回归损失不需要正负样本均衡。

epoch 0, lr: 2.7e-04, cls: 0.582, ctr: 0.149, reg: 2.549, iou: 0.447, data: 1.4e debug 256
epoch 0, lr: 5.5e-04, cls: 0.129, ctr: 0.005, reg: 0.544, iou: 0.837, data: 1.8e debug 512 结论：其实没啥影响，效果略逊于原来。

# 互相关与加法对训练损失的影响

epoch 0, lr: 1.4e-04, cls: 1.351, ctr: 0.159, reg: 3.018, iou: 0.404, data: 1.9e debug 128
epoch 0, lr: 2.7e-04, cls: 0.641, ctr: 0.103, reg: 2.676, iou: 0.429, data: 3.6e debug 256
epoch 0, lr: 5.5e-04, cls: 0.115, ctr: 0.003, reg: 2.540, iou: 0.448, data: 1.9e debug 512 结论：加法是不行的。