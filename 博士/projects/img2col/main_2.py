"""
对通道数为2的图像进行卷积。
"""
import torch
from torch.nn import functional as F


def img2col():
    data_col = F.unfold(data, kernel_size)  # 1*18*16 18表示每个窗口内元素总数为18(两个通道)，16表示需要滑动16次窗口
    print('data_col.shape:', data_col.shape)

    kernel_col = kernel.reshape(out_channel, -1)
    # 4*18, 4 表示输出通道为4. 每一列对应一个输出通道。
    # 18=3*3*2=卷积尺寸*输入通道数。
    # 卷积的一列（包含多个输入通道）与数据的一“行”（包含多个输出通道）相乘，得到一个输出通道的结果。
    print('kernel_col.shape:', kernel_col.shape)

    result = kernel_col @ data_col[0]  # 4*16，4表示输出通道，16表示总的空间分辨率。
    return result.reshape(out_channel, 4, 4)  # 输出通道是 2，共 4*4 个位置。


def conv():
    result = F.conv2d(input=data, weight=kernel)
    print('result1.shape', result.shape)  # 1,4,4,4 batch, out_channel, h, w
    return result


if __name__ == '__main__':
    data = torch.tensor([[[[0.0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]],
                          [[0.0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]]])
    # b, c, h, w = 1, 2, 4, 4
    print('data.shape:', data.shape)
    data = F.pad(data, [1, 1, 1, 1])

    kernel = torch.tensor([[[[1.0, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]]],
                           [[[19.0, 20, 21], [22, 23, 24], [25, 26, 27]], [[28, 29, 30], [31, 32, 33], [34, 35, 36]]],
                           [[[1.0, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]]],
                           [[[1.0, 2, 3], [4, 5, 6], [7, 8, 9]], [[10, 11, 12], [13, 14, 15], [16, 17, 18]]]])
    # 4*2*3*3 out,in,h,w
    out_channel, in_channel, kernel_size, _ = kernel.shape
    print('kernel.shape:', kernel.shape)
    result1 = conv()
    result2 = img2col()
    print('result2.shape:', result2.shape)
    if torch.equal(result1[0], result2):
        print('success')
    else:
        print(result1, result2)
        print(result1.shape, result2.shape)
