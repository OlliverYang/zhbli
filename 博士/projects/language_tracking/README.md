# 训练
export PYTHONPATH=/home/etvuz/projects/language_tracking

cd language_tracking
python main/train.py -cfg experiments/siamfcpp/train/lasot/siamfcpp_googlenet-trn.yaml

# 测试

cd language_tracking
python main/test.py -cfg experiments/siamfcpp/test/lasot/siamfcpp_googlenet-lasot.yaml

# TODO

测试时，eval 了吗？应该是了。

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
epoch 0, lr: 5.5e-04, cls: 0.121, ctr: 0.003, reg: 0.449, iou: 0.864, data: 1.4e debug 512 结论：不如输入尺寸 256 好

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

# 句子模型是否反传梯度

epoch 0, lr: 1.4e-04, cls: 1.352, ctr: 0.159, reg: 11.134, iou: 0.035, data: 4.7 debug 128
epoch 0, lr: 2.7e-04, cls: 0.894, ctr: 0.152, reg: 2.560, iou: 0.445, data: 2.2e debug 256
epoch 0, lr: 5.5e-04, cls: 0.122, ctr: 0.006, reg: 0.495, iou: 0.851, data: 3.9e debug 512 结论：其实没啥影响，效果略逊于原来。

# 输入有 1024 768 改为 256 256 的影响
epoch 0, lr: 1.4e-04, cls: 1.350, ctr: 0.152, reg: 2.698, iou: 0.426, data: 1.8e debug 128
epoch 0, lr: 2.7e-04, cls: 0.869, ctr: 0.144, reg: 0.322, iou: 0.899, data: 1.2e debug 256 结论：权重 1 1 3 不如 0.5 0.5 8 好

# 回归损失权重影响 由 1 1 3 变为 0.5 0.5 8
epoch 0, lr: 1.4e-04, cls: 0.769, ctr: 0.076, reg: 2.066, iou: 0.778, data: 4.2e debug 128
epoch 0, lr: 2.7e-04, cls: 0.556, ctr: 0.075, reg: 0.460, iou: 0.945, data: 4.3e debug 256 结论：权重 0.5 0.5 8 不如 0.1 0.1 10 好

# 回归损失为 0.1 0.1 10
epoch 0, lr: 1.4e-04, cls: 0.174, ctr: 0.015, reg: 1.736, iou: 0.843, data: 6.7e debug 128 结论：权重 0.1 0.1 10 不如 0.1 0.1 20 好 （大数据会训飞）

# 回归损失为 0.1 0.1 20
epoch 0, lr: 1.4e-04, cls: 0.174, ctr: 0.015, reg: 2.567, iou: 0.881, data: 2.4e debug 128 （大数据会训飞）

# 损失为 0.1 0.1 40
epoch 0, lr: 1.4e-04, cls: 0.174, ctr: 0.015, reg: 6.111, iou: 0.862, data: 3.5e debug 128 结论：0.1 0.1 40 不如 0.1 0.1 20 好

# 训练结果

epoch 0, lr: 8.0e-02, cls: 0.121, ctr: 0.036, reg: 1.559, iou: 0.618, data: 8.7e-05, fwd: 4.3e-01, bwd: 1.3e-01, optim: 3.8e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [30:48<00:00,  1.18s/it]
2021-03-26 18:31:27.240 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-0.pkl
epoch 1, lr: 7.9e-02, cls: 0.082, ctr: 0.025, reg: 1.224, iou: 0.682, data: 7.6e-05, fwd: 4.4e-01, bwd: 1.5e-01, optim: 3.7e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [29:06<00:00,  1.12s/it]
2021-03-26 19:00:37.093 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-1.pkl
epoch 2, lr: 7.8e-02, cls: 0.094, ctr: 0.025, reg: 1.306, iou: 0.671, data: 7.7e-05, fwd: 4.1e-01, bwd: 1.3e-01, optim: 4.0e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [29:37<00:00,  1.14s/it]
2021-03-26 19:30:18.708 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-2.pkl
epoch 3, lr: 7.5e-02, cls: 0.079, ctr: 0.022, reg: 1.530, iou: 0.618, data: 6.1e-05, fwd: 4.2e-01, bwd: 1.5e-01, optim: 3.7e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [32:22<00:00,  1.24s/it]
2021-03-26 20:02:43.383 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-3.pkl
epoch 4, lr: 7.2e-02, cls: 0.066, ctr: 0.018, reg: 0.944, iou: 0.743, data: 6.7e-05, fwd: 4.2e-01, bwd: 1.4e-01, optim: 3.8e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [34:46<00:00,  1.34s/it]
2021-03-26 20:37:32.264 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-4.pkl
epoch 5, lr: 6.7e-02, cls: 0.066, ctr: 0.019, reg: 1.103, iou: 0.708, data: 6.6e-05, fwd: 4.1e-01, bwd: 1.5e-01, optim: 3.9e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [35:14<00:00,  1.35s/it]
2021-03-26 21:12:49.216 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-5.pkl
epoch 6, lr: 6.2e-02, cls: 0.075, ctr: 0.020, reg: 0.978, iou: 0.736, data: 8.7e-05, fwd: 5.4e-01, bwd: 1.6e-01, optim: 3.7e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [34:37<00:00,  1.33s/it]
2021-03-26 21:47:29.531 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-6.pkl
epoch 7, lr: 5.6e-02, cls: 0.071, ctr: 0.021, reg: 1.005, iou: 0.727, data: 7.3e-05, fwd: 4.3e-01, bwd: 1.8e-01, optim: 3.8e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [34:37<00:00,  1.33s/it]
2021-03-26 22:22:08.901 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-7.pkl
epoch 8, lr: 5.0e-02, cls: 0.064, ctr: 0.017, reg: 0.890, iou: 0.754, data: 1.2e+00, fwd: 4.1e-01, bwd: 1.5e-01, optim: 3.8e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [33:33<00:00,  1.29s/it]
2021-03-26 22:55:44.693 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-8.pkl
epoch 9, lr: 4.3e-02, cls: 0.066, ctr: 0.018, reg: 0.864, iou: 0.763, data: 2.5e-03, fwd: 4.4e-01, bwd: 1.5e-01, optim: 3.8e-01,  max mem: 8250.6M: 100%|█████████████████████████████████████████████████████████████████████████████████| 1562/1562 [33:15<00:00,  1.28s/it]
2021-03-26 23:29:02.717 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-9.pkl
epoch 10, lr: 3.7e-02, cls: 0.047, ctr: 0.012, reg: 0.619, iou: 0.823, data: 7.8e-05, fwd: 4.3e-01, bwd: 2.5e-01, optim: 4.3e-01,  max mem: 8304.1M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [32:59<00:00,  1.27s/it]
2021-03-27 00:02:04.395 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-10.pkl
epoch 11, lr: 3.0e-02, cls: 0.052, ctr: 0.017, reg: 0.743, iou: 0.794, data: 7.2e-05, fwd: 4.1e-01, bwd: 2.5e-01, optim: 4.2e-01,  max mem: 8305.4M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [32:41<00:00,  1.26s/it]
2021-03-27 00:34:48.252 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-11.pkl
epoch 12, lr: 2.4e-02, cls: 0.034, ctr: 0.010, reg: 0.516, iou: 0.848, data: 1.1e-04, fwd: 4.1e-01, bwd: 2.7e-01, optim: 4.3e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [32:26<00:00,  1.25s/it]
2021-03-27 01:07:17.142 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-12.pkl
epoch 13, lr: 1.8e-02, cls: 0.036, ctr: 0.009, reg: 0.475, iou: 0.861, data: 6.3e-05, fwd: 4.1e-01, bwd: 2.5e-01, optim: 3.8e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [32:11<00:00,  1.24s/it]
2021-03-27 01:39:31.125 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-13.pkl
epoch 14, lr: 1.3e-02, cls: 0.025, ctr: 0.008, reg: 0.448, iou: 0.866, data: 6.7e-05, fwd: 4.3e-01, bwd: 2.5e-01, optim: 4.4e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [31:57<00:00,  1.23s/it]
2021-03-27 02:11:30.882 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-14.pkl
epoch 15, lr: 8.4e-03, cls: 0.044, ctr: 0.011, reg: 0.518, iou: 0.853, data: 6.7e-03, fwd: 4.4e-01, bwd: 2.6e-01, optim: 4.2e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [31:30<00:00,  1.21s/it]
2021-03-27 02:43:03.521 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-15.pkl
epoch 16, lr: 4.8e-03, cls: 0.028, ctr: 0.006, reg: 0.351, iou: 0.894, data: 1.2e-04, fwd: 3.9e-01, bwd: 2.3e-01, optim: 4.2e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [31:23<00:00,  1.21s/it]
2021-03-27 03:14:29.725 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-16.pkl
epoch 17, lr: 2.2e-03, cls: 0.027, ctr: 0.007, reg: 0.376, iou: 0.887, data: 9.4e-05, fwd: 4.6e-01, bwd: 2.6e-01, optim: 4.3e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [30:56<00:00,  1.19s/it]
2021-03-27 03:45:28.372 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-17.pkl
epoch 18, lr: 5.5e-04, cls: 0.027, ctr: 0.008, reg: 0.401, iou: 0.879, data: 7.3e-05, fwd: 4.2e-01, bwd: 2.7e-01, optim: 4.2e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [30:32<00:00,  1.17s/it]
2021-03-27 04:16:03.320 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-18.pkl
epoch 19, lr: 1.0e-06, cls: 0.025, ctr: 0.007, reg: 0.386, iou: 0.885, data: 2.1e-05, fwd: 4.2e-01, bwd: 2.4e-01, optim: 4.0e-01,  max mem: 8317.0M: 100%|████████████████████████████████████████████████████████████████████████████████| 1562/1562 [30:35<00:00,  1.18s/it]
2021-03-27 04:46:40.961 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/epoch-19.pkl
2021-03-27 04:46:42.037 | INFO     | videoanalyst.engine.trainer.trainer_base:save_snapshot:155 - Snapshot saved at: snapshots/siamfcpp_googlenet-lasot/final_model.pkl

## 实验获得成功。
"success_score": 0.44, "precision_score": 0.43, "normalized_precision_score": 0.47, "success_rate": 0.51,