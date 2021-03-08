"""
为了验证 img2_col 中数字的顺序。
"""
import torch
from torch.nn import functional as F


def main():
    data = torch.tensor(list(range(32))).reshape([1,2,4,4]).float()  # 1*2*2*2 bchw
    print(data[0][0])  # 第一通道的内容
    print(data[0][1])  # 第二通道的内容
    data_col = F.unfold(data, 3)
    # 观察 data_col 可知，顺序为：先把第一通道变成向量，再把第二通道变成向量，再拼起来。因此对应到点云中，应该是先把x轴变成向量，再把y轴变成向量，再拼起来，作为一列。
    return


if __name__ == '__main__':
    main()