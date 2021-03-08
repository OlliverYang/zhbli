"""
在一维空间，实现对邻居点的卷积。
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


if __name__ == '__main__':
    kernel_size = 3
    points = torch.tensor([[[0,0], [1,-1], [2,-2], [3,-3], [4,-4], [5,-5], [6,-6], [7,-7], [8,-8], [9,-9],
                            [10,-10], [11,-11], [12,-12], [13,-13], [14,-14], [15,-15]]])
    # 16 个点，1*16*2 批次*点数*维数
    kernel = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
                           [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]])
    # 对应于 kernel_col, out*(in*num) = 4*(2*9) = 4*18
    print('points.shape', points.shape)
    print('kernel.shape:', kernel.shape)
    neighbor_index = get_neighbor_index(points, kernel_size*kernel_size)  # 仅是坐标，不是数值
    neighbors = indexing_neighbor(points, neighbor_index)  # 批次，输入点数，邻居数，通道数。
    # 需要卷积的元素总数为 邻居数*通道数。哪个在前？根据对 img2col_order的分析，对于每一列，是同一通道的放在一起。所以通道数在前，邻居数在后。
    neighbors = neighbors.permute([0, 3, 2, 1])  # 批次，通道数，邻居数，输入点数。
    neighbors = neighbors.reshape(neighbors.shape[0], -1, neighbors.shape[-1])
    # 批次，需要卷积的元素总数，输入点数。
    print('neighbors.shape', neighbors.shape)
    result = kernel @ neighbors[0]
    print('result.shape:', result.shape)  # 4, 16 输出通道是4，共16个点。
    print(result)
