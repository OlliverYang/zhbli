make_patch.py

```python
min_in, max_in = netClassifier.input_range[0], netClassifier.input_range[1]
# 既然网络的输入是-1到1，那么这里min_in=0, max_in=1是什么含义？
mean, std = np.array(netClassifier.mean), np.array(netClassifier.std) 
# mean=0.5, std=0.5
min_out, max_out = np.min((min_in-mean)/std), np.max((max_in-mean)/std)


def attack(x, patch, mask):
    """
    x: 是否添加了patch？否。
    """
    netClassifier.eval()  # 注意，网络本身的参数不参与训练。

    x_out = F.softmax(netClassifier(x))
    target_prob = x_out.data[0][target]
    
    '''
    下述循环的含义：我们希望添加了patch的图像，都分类为target。
    如果图像本身的类别就是target，则不需要添加patch，进行下述循环操作。
    添加了补丁后，通过优化，target_prob应该逐渐增大，直到大于conf_target，
    便停止循环。
    这对应到目标跟踪中，结束条件是什么呢？
    '''
    while conf_target > target_prob:  # conf_target: 预设值，为0.9。
        ...
        adv_x = torch.clamp(adv_x, min_out, max_out)
        # min_out: -1.0, max_out: 0.1 有什么含义？网络的输入就是介于-1到1的。
        # 这句话可以保证补丁的值在0到255之间。
        
```

# 问题

怎么把输入从0~255转到-1~1的？

# TODO

- [x] 跟踪训练时，载入训好的网络。
- [x] 如果要训练多个epoch，要保证patch可以传递。
- [x] 负样本对比例调成0，边框变[0,0,40,40]
- [x] 搜索图像左上角贴图
- [x] mask的取值范围，应该和输入图像保持一致。
- [x] The checkpoint contains parameters not used by the model 就这样
- [x] Some model parameters are not in the checkpoint 就这样

跟踪训练时，固定网络参数。	

保存patch

测试时，要注意patch不能贴到目标的位置，否则不能说明问题。训练时，感觉随即放应该问题不大。