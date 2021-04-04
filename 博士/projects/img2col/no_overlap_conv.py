import torch


def main():
    data_size = 32
    x = torch.zeros((1, 1, data_size))
    x[:, :, data_size//2-1] = 1
    x[:, :, data_size//2] = 1
    kernel = torch.ones((1, 1, 2))
    for i in range(32):
        x = torch.nn.functional.conv1d(x, kernel, stride=2)
        x_list = x.data.numpy()[0][0]
        print(['{:.2f}'.format(x_) for x_ in x_list])

if __name__ == '__main__':
    main()