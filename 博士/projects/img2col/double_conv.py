import torch


def main():
    data_size = 5
    x = torch.zeros((1, 1, data_size))
    x[:, :, data_size//2] = 1
    # x[:, :, data_size//2-1] = 1
    # x[:, :, data_size//2] = 1
    # x = torch.ones((1, 1, data_size))
    kernel_2 = torch.ones((1, 1, 2))
    kernel_3 = torch.ones((1, 1, 3))
    for i in range(32):
        x_2 = torch.nn.functional.conv1d(x, kernel_2, padding=2)
        x_3 = torch.nn.functional.conv1d(x, kernel_3, padding=2)
        index_2_1 = list(range(x_2.shape[-1]))
        index_2_2 = list(range(3, x_2.shape[-1]))
        index_3_1 = list(range(x_3.shape[-1]))
        index_3_2 = list(range(2, x_3.shape[-1]))
        x = x_2[:, :, index_2_1[:data_size]] + x_2[:, :, index_2_2[:data_size]] + \
            x_3[:, :, index_3_1[:data_size]] + x_3[:, :, index_3_2[:data_size]]
        y = torch.nn.functional.conv1d(x, kernel_3, padding=1)
        print(i)
        x_list = x.data.numpy()[0][0]
        print(['{:.2f}'.format(x_) for x_ in x_list])
        y_list = y.data.numpy()[0][0]
        print(['{:.2f}'.format(x_) for x_ in y_list])


if __name__ == '__main__':
    main()