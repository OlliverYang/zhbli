# 修改记录

将 num_workers 改为 1，否则内存泄露。

# 实验结果

## 配置文件

yolof.res50.C5.1x
pods_train --num-gpus 4

## 训练时间

[04/12 05:09:22 c2.engine.hooks]: Overall training speed: 44998 iterations in 10:58:36 (0.8782 s / it)
[04/12 05:09:22 c2.engine.hooks]: Total training time: 12:02:33 (1:03:57 on hooks)

## 收敛情况

[04/12 05:09:22 c2.utils.dump.events]: eta: 0:00:00  iter: 45000/45000  total_loss: 0.477  loss_cls: 0.191  loss_box_reg: 0.287    time: 0.8782  data_time: 0.0347  lr: 0.000600  max_mem: 5210M

## 测试结果

[04/12 05:09:21 c2.engine.runner]: Evaluation results for coco_2017_val in csv format:
[04/12 05:09:21 c2.evaluation.testing]: copypaste: Task: bbox
[04/12 05:09:21 c2.evaluation.testing]: copypaste: AP,AP50,AP75,APs,APm,APl
[04/12 05:09:21 c2.evaluation.testing]: copypaste: 37.5377,56.9454,40.3480,18.7224,42.2852,52.4176

### 原文结果

YOLOF_R_50_C5_1x COCO val mAP 37.7

## 结论

可复现