import torch
import torch.nn.functional as F


def combinational_conv(data, origin_kernel):
    x = None
    kernel_size = origin_kernel.shape[-1]
    for i in range(kernel_size):
        for j in range(kernel_size):
            mask = torch.ones((kernel_size, kernel_size), requires_grad=False)
            mask[i][j] = 0
            kernel = origin_kernel * mask
            if x is None:
                x = F.conv2d(input=data, weight=kernel, padding=1)
            else:
                x += F.conv2d(input=data, weight=kernel, padding=1)
    x /= (kernel_size * kernel_size)
    return x


def main():
    output_channel = 5
    data_size = 13
    data = torch.zeros((1, output_channel, data_size, data_size))
    data[:, :, data_size//2, data_size//2] = 1

    kernel_size = 3
    kernel = torch.ones((output_channel, output_channel, kernel_size, kernel_size))

    x = data
    layer_number = 4
    for i in range(layer_number):
        x = combinational_conv(x, kernel)
        # x = F.conv2d(x, kernel, padding=1)
    n_np = x[0][0].data.cpu().numpy()

     return


if __name__ == '__main__':
    main()