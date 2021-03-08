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


if __name__ == '__main__':
    points = torch.tensor([[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15]]])
    # 16 个点，1*16*1 批次*点数*维数
    kernel = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18]])  # 2*9, 对应于 kernel_col
    print('points.shape', points.shape)
    print('kernel.shape:', kernel.shape)
    neighbors = get_neighbor_index(points, 9)
    neighbors = neighbors.transpose(1, 2)
    print('neighbors.shape', neighbors.shape)
    result = kernel @ neighbors[0]
    print('result.shape:', result.shape)  # 2, 9 输出通道是2，共9个点。
    print(result)
