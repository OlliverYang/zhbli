# 运行环境

pytorch1.4_python3.7

# 准备数据

1. 从 https://shapenet.cs.stanford.edu/media/shapenetcore_partanno_segmentation_benchmark_v0_normal.zip 下载模型。
2. 保存在路径 data/modelnet40_normal_resampled/ 中。

# 分类任务

## 训练

python train_cls.py --model pointnet2_cls_msg --normal --log_dir pointnet2_cls_msg

## 测试

python test_cls.py --normal --log_dir pointnet2_cls_msg

# BUG

## RuntimeError: cuDNN error: CUDNN_STATUS_NOT_SUPPORTED. This error may appear if you passed in a non-contiguous input.

### 原因

pytorch 的 bug。

### 解决方案

torch.backends.cudnn.enabled = False