"""
在一维空间，实现对邻居点的卷积。
新增：验证是否对数据顺序具有不变性。
新增：对邻居点提取相对位置而非绝对位置。
"""
import torch
from torch.nn import functional as F


def get_neighbor_index(vertices: "(bs, vertice_num, 3)",  neighbor_num: int):
    """
    Return: (bs, vertice_num, neighbor_num)
    """
    bs, v, _ = vertices.size()
    device = vertices.device
    inner = torch.bmm(vertices, vertices.transpose(1, 2))  #(bs, v, v)
    quadratic = torch.sum(vertices**2, dim=2)  #(bs, v)
    distance = inner * (-2) + quadratic.unsqueeze(1) + quadratic.unsqueeze(2)
    neighbor_index = torch.topk(distance, k=neighbor_num + 1, dim=-1, largest=False)[1]
    neighbor_index = neighbor_index[:, :, 1:]
    return neighbor_index


def indexing_neighbor(tensor: "(bs, vertice_num, dim)", index: "(bs, vertice_num, neighbor_num)" ):
    """
    Return: (bs, vertice_num, neighbor_num, dim)
    """
    bs, v, n = index.size()
    id_0 = torch.arange(bs).view(-1, 1, 1)
    tensor_indexed = tensor[id_0, index]
    return tensor_indexed


def conv(points, kernel, bias):
    print('points.shape', points.shape)  # 批次，输入点数，通道数。
    print('kernel.shape:', kernel.shape)
    kernel_size = 3
    neighbor_index = get_neighbor_index(points, kernel_size * kernel_size)  # 仅是坐标，不是数值
    neighbors = indexing_neighbor(points, neighbor_index)  # 批次，输入点数，邻居数，通道数。
    # 需要卷积的元素总数为 邻居数*通道数。哪个在前？根据对 img2col_order的分析，对于每一列，是同一通道的放在一起。所以通道数在前，邻居数在后。
    neighbors = neighbors - points.unsqueeze(2)
    neighbors = neighbors.permute([0, 3, 2, 1])  # 批次，通道数，邻居数，输入点数。
    neighbors = neighbors.reshape(neighbors.shape[0], -1, neighbors.shape[-1])
    # 批次，需要卷积的元素总数，输入点数。
    print('neighbors.shape', neighbors.shape)
    result = (kernel @ neighbors).transpose(1, 2) + bias
    result = F.relu(result, inplace=True)
    print('result.shape:', result.shape)  # 4, 16 输出通道是4，共16个点。
    return result


def main():
    points = torch.tensor([[[0, 0], [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7], [8, -8], [9, -9],
                            [10, -10], [11, -11], [12, -12], [13, -13], [14, -14], [15, -15]]])
    points2 = torch.tensor([[[15, -15], [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7], [8, -8], [9, -9],
                             [10, -10], [11, -11], [12, -12], [13, -13], [14, -14], [0, 0]]])
    # 16 个点，1*16*2 批次*点数*维数
    kernel = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                           [2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                           [3, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                           [4, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]])
    # 对应于 kernel_col, out*(in*邻居数) = 4*(2*9) = 4*18
    in_channel = points.shape[-1]
    out_channel = kernel.shape[0]
    support_num = 9
    assert in_channel * support_num == kernel.shape[-1]
    bias = torch.rand(out_channel)  # bias 尺寸等于输出通道，经核实是没错的。
    result1 = conv(points, kernel, bias)
    result2 = conv(points2, kernel, bias)
    if torch.equal(result1[:, -1], result2[:, 0]):  # 注意，一个点对应的输出特征为一列，而不是一行。
        print('success')
    else:
        print('wrong')
        print(result1[:,-1], result2[:,0])
    return

if __name__ == '__main__':
    main()