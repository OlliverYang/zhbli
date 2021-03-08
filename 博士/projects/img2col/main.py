"""
利用 img2col 实现卷积操作。从而深入了解卷积原理。
为了实现“有几个输入点，就滑动几次（即进行几次卷积）”的效果，进行0填充。
"""

import torch
from torch.nn import functional as F


def conv():
    result = F.conv2d(input=data, weight=kernel)
    return result


def img2col():
    data_col = F.unfold(data, 3)  # 1*9*16 9表示每个窗口内元素总数为9，16表示需要滑动19次窗口
    print('data_col.shape:', data_col.shape)
    kernel_col = kernel.reshape(2, 9)
    print('kernel_col.shape:', kernel_col.shape)
    result = kernel_col @ data_col[0]
    return result.reshape(2, 4, 4)  # 输出通道是 2，共 4*4 个位置。


if __name__ == '__main__':
    data = torch.tensor([[[[0.0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]]])  # 1*1*4*4 b,in,h,w
    data = F.pad(data, [1, 1, 1, 1])
    print("data.shape:", data.shape)

    kernel = torch.tensor([[[[1.0, 2, 3], [4, 5, 6], [7, 8, 9]]], [[[10, 11, 12], [13, 14, 15], [16, 17, 18]]]])
    # 2*1*3*3 out,in,h,w
    print("kernel.shape:", kernel.shape)
    result1 = conv()  # b,out,h,w
    print('result1.shape:', result1.shape)
    result2 = img2col()
    if torch.equal(result1[0], result2):
        print('success')
    else:
        print(result1, result2)
        print(result1.shape, result2.shape)
