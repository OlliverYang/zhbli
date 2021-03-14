# -*- coding: UTF-8 -*-
# TODO 类别数是多少？（用256可蒙混过关）
# TODO 有没有背景？（用256可蒙混过关）
import socket
import sys
import numpy as np
import torch
from torchvision import models
import torch.nn.functional as F
import torchvision.transforms as T
import os

HOST = '172.18.32.31'  # Symbolic name meaning all available interfaces
PORT = 2019  # Arbitrary non-privileged port
NUM_CLASSES = 16  # 若较大，则非常占显存
BATCH_SIZE = 2  # 若为 2 则超出显存
FRAME_WIDTH = 1024
FRAME_HEIGHT = 768
GPU_ID = 1

os.environ["CUDA_VISIBLE_DEVICES"] = str(GPU_ID)


def start_server_dummy():
    return None


def start_server():
    print('starting')
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except socket.error as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    return conn


def socketToNumpy(data, sockData):
    k = data.shape[2]
    j = data.shape[1]
    i = data.shape[0]
    sockData = np.fromstring(sockData, np.uint8)
    data = np.tile(sockData, 1).reshape((i, j, k))

    return data


def get_one_data_dummy(conn):
    img = np.zeros((768, 1024, 3), dtype=np.uint8)
    mask = np.zeros((768, 1024), dtype=np.int)
    return img, mask


def get_one_data(conn):
    color = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), np.uint8)
    color_size = color.size
    mask = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 1), np.uint8)
    mask_size = mask.size
    print('mask_size:', mask_size)
    sockData_color = b''
    result = True

    print('receiving color...')
    while color_size:
        nbytes = conn.recv(color_size)
        if not nbytes: break; result = False
        sockData_color += nbytes
        color_size -= len(nbytes)
    print('color received.')
    if result:
        color = socketToNumpy(color, sockData_color)
        color = (1 - color) * 255  # 1 - 很重要
        color = color[..., [2, 1, 0]]  # 顺序很重要
        conn.sendall(bytes("got_color", "utf-8"))
    else:
        print('stop running')
        return None, None

    print('receiving mask...')
    sockData_mask = b''
    while mask_size:
        nbytes = conn.recv(mask_size)
        if not nbytes: break; result = False
        sockData_mask += nbytes
        mask_size -= len(nbytes)

    if result:
        mask = socketToNumpy(mask, sockData_mask)
        conn.sendall(bytes("got_mask", "utf-8"))
    else:
        print('stop running')
        return None, None

    return color, mask


def cross_entropy2d(input, target, weight=None, size_average=True):
    # input: (n, c, h, w), target: (n, h, w)
    n, c, h, w = input.size()
    # log_p: (n, c, h, w)
    log_p = F.log_softmax(input, dim=1)
    # log_p: (n*h*w, c)
    log_p = log_p.transpose(1, 2).transpose(2, 3).contiguous()
    log_p = log_p[target.view(n, h, w, 1).repeat(1, 1, 1, c) >= 0]
    log_p = log_p.view(-1, c)
    # target: (n*h*w,)
    mask = target >= 0
    target = target[mask]
    loss = F.nll_loss(log_p, target, weight=weight, reduction='sum')
    if size_average:
        loss /= mask.data.sum()
    return loss


conn = start_server()

model = models.segmentation.deeplabv3_resnet50(num_classes=NUM_CLASSES).cuda().train()

optimizer = torch.optim.SGD(model.parameters(), 0.1,
                            momentum=0.9,
                            weight_decay=1e-4)

# Apply the transformations needed
trf = T.Compose([T.ToTensor(),
                 T.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])])
trf_mask = T.Compose([T.ToTensor()])

i = 0
while True:
    i += 1
    print(i)
    img_list = []
    target_list = []
    print('receiving data...')
    for j in range(BATCH_SIZE):
        image_np, target_np = get_one_data(conn)
        target_np[target_np >= NUM_CLASSES] = 0
        if image_np is None:
            save_path = '/tmp/{}.pth'.format(i)
            torch.save(model.state_dict, save_path)
            print(save_path, 'stop')
            exit(0)
        image = trf(image_np)  # 必须为 uint8 格式，否则会报错：浮点数例外，核心已转储。
        image = image.unsqueeze(0)
        target = trf_mask(target_np)
        target = target.unsqueeze(0).long()  # 必须为 long 类型，否则计算损失时会报错。
        img_list.append(image)
        target_list.append(target)
    print('received.')
    inp = torch.cat(img_list, dim=0).cuda()
    target = torch.cat(target_list, dim=0).cuda()
    out = model(inp)[
        'out']  # batch size 若是 1 则报错 ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 256, 1, 1])
    loss = cross_entropy2d(out, target, size_average=False)

    # compute gradient and do SGD step
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if i & (i - 1) == 0:
        save_path = '/tmp/{}.pth'.format(i)
        torch.save(model.state_dict, save_path)
        print(save_path)
