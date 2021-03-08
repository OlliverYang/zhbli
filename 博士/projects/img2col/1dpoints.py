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


def conv(points, kernel):
    neighbor_index = get_neighbor_index(points, 9)  # 仅是坐标，不是数值
    neighbors = indexing_neighbor(points, neighbor_index)  # 批次，输入点数，邻居数，通道数。
    # @TODO：需要卷积的元素总数为 邻居数*通道数。哪个在前？
    neighbors = neighbors.permute([0, 2, 3, 1])  # 批次，邻居数，通道数，输入点数。
    neighbors = neighbors.reshape(neighbors.shape[0], -1, neighbors.shape[-1])
    # 批次，需要卷积的元素总数，输入点数。
    print('neighbors.shape', neighbors.shape)
    result = kernel @ neighbors[0]
    print('result.shape:', result.shape)  # 2, 16 输出通道是2，共16个点。
    return result


def main():
    points = torch.tensor([[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15]]])
    points2 = torch.tensor([[[15], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [0]]])
    # 16 个点，1*16*1 批次*点数*维数
    kernel = torch.tensor([[1, 2, 3, 4, 5, 6, 7, 8, 9], [10, 11, 12, 13, 14, 15, 16, 17, 18]])  # 2*9, 对应于 kernel_col
    print('points.shape', points.shape)
    print('kernel.shape:', kernel.shape)
    result1 = conv(points, kernel)
    result2 = conv(points2, kernel)
    print(result1, result2)


if __name__ == '__main__':
    main()