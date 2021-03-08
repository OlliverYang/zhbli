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

# 测试