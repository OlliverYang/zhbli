# -*- coding: UTF-8 -*-
# TODO 类别数是多少？（用256可蒙混过关）
# TODO 有没有背景？（用256可蒙混过关）
# 有时断开不能重新连接：这是因为在TCP/IP终止连接的四次握手中，当最后的ACK回复发出后，有个2MSL的时间等待，MSL指一个片段在网络中最大的存活时间，
# 这个时间一般是30秒，所以基本上过60秒后就可以重新连接！
# 为什么要等待2MSL？是因为在最后发出ACK回复后，发送方不能确认ACK是否被另一端正常收到，如果另一端没有收到ACK回复的话，
# 将会在1MSL后再次发送FIN片段。所以说发送方等待2MSL时间，也就是刚好它发ACK回复和对方发送FIN片段的时间，如果此时间内都没有再次收到FIN片段的话，
# 发送方就假设对方已经正常接收到了ACK回复，此时它就会正常关闭连接！
import socket
import sys
import cv2
import numpy as np
import torch
from torchvision import models
import torch.nn.functional as F
import torchvision.transforms as T
import os
import argparse
import time


HOST = '172.18.32.31'  # Symbolic name meaning all available interfaces
PORT = 2019  # Arbitrary non-privileged port
NUM_CLASSES = 16  # 若较大，则非常占显存
BATCH_SIZE = 2  # 若为 2 则超出显存
FRAME_WIDTH = 1024
FRAME_HEIGHT = 768
GPU_ID = 1
LR = 0.1


parser = argparse.ArgumentParser(description='GTA5')
parser.add_argument('--save_dir', type=str, default='/tmp')
parser.add_argument('--resume', type=int, default=0)
parser.add_argument('--dummy', type=int, default=0)
parser.add_argument('--gpu_id', type=str, default='1')
args = parser.parse_args()
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_id
print(args)


def start_server_dummy():
    return None


def start_server():
    print('starting')
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 尝试解决 [Errno 98] Address already in use
        except socket.error as msg:
            print(msg)
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except socket.error as msg:
            print(msg)
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    conn_, addr = s.accept()

    print('Connected by', addr)
    conn_.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 尝试解决 [Errno 98] Address already in use
    conn_.settimeout(10.0)  # 为 recv 设置最大接受时间
    return conn_


def socketToNumpy(data, sockData):
    k_ = data.shape[2]
    j_ = data.shape[1]
    i_ = data.shape[0]
    sockData = np.fromstring(sockData, np.uint8)
    data = np.tile(sockData, 1).reshape((i_, j_, k_))

    return data


def get_one_data_dummy():
    img = cv2.imread('/tmp/1.jpg')
    mask = cv2.imread('/tmp/1.png')[:, :, 0]
    return img, mask


def get_one_data(conn_, old_img, old_mask, old_index):
    color = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), np.uint8)
    color_size = color.size
    mask = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 1), np.uint8)
    mask_size = mask.size
    print('mask_size:', mask_size)
    sockData_color = b''
    result = True

    print('receiving color...')
    nbytes = None
    while color_size:
        try:
            nbytes = conn_.recv(color_size)
        except Exception as e:
            localtime = time.asctime(time.localtime(time.time()))
            print(old_index, localtime, e)
            cv2.imwrite(os.path.join(args.save_dir, '{}.jpg'.format(old_index)), old_img)
            cv2.imwrite(os.path.join(args.save_dir, '{}.png'.format(old_index)), old_mask)
            print('old image saved, exit')
            exit(0)

        if not nbytes:
            print('color no nbytes')
            result = False
            break
        sockData_color += nbytes
        color_size -= len(nbytes)
    print('color received.')
    if result:
        color = socketToNumpy(color, sockData_color)
        color = (1 - color) * 255  # 1 - 很重要
        color = color[..., [2, 1, 0]]  # 顺序很重要
        conn_.sendall(bytes("got_color", "utf-8"))
    else:
        print('stop running')
        return None, None

    print('receiving mask...')
    sockData_mask = b''
    while mask_size:
        nbytes = conn_.recv(mask_size)
        if not nbytes:
            print('no nbytes')
            break
        sockData_mask += nbytes
        mask_size -= len(nbytes)

    if result:
        mask = socketToNumpy(mask, sockData_mask)
        conn_.sendall(bytes("got_mask", "utf-8"))
    else:
        print('stop running')
        return None, None

    return color, mask


def cross_entropy2d(input_, target_, weight=None, size_average=True):
    # input_: (n, c, h, w), target_: (n, h, w)
    n, c, h, w = input_.size()
    # log_p: (n, c, h, w)
    log_p = F.log_softmax(input_, dim=1)
    # log_p: (n*h*w, c)
    log_p = log_p.transpose(1, 2).transpose(2, 3).contiguous()
    log_p = log_p[target_.view(n, h, w, 1).repeat(1, 1, 1, c) >= 0]
    log_p = log_p.view(-1, c)
    # target_: (n*h*w,)
    mask = target_ >= 0
    target_ = target_[mask]
    loss_ = F.nll_loss(log_p, target_, weight=weight, reduction='sum')
    if size_average:
        loss_ /= mask.data.sum()
    return loss_


if args.dummy == 1:
    print('dummy connect')
    conn = None
else:
    conn = start_server()

model = models.segmentation.deeplabv3_resnet50(num_classes=NUM_CLASSES).cuda().train()

optimizer = torch.optim.SGD(model.parameters(), LR,
                            momentum=0.9,
                            weight_decay=1e-4)

# Apply the transformations needed
trf = T.Compose([T.ToTensor(),  # 转换为0~1
                 T.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])])

i = args.resume
if i != 0:
    resume_path = os.path.join(args.save_dir, '{}.pth'.format(i))
    model.load_state_dict(torch.load(resume_path))
    model.train()
    print('resume model loaded:', resume_path)

while True:
    i += 1
    print(i)
    image_np = None
    target_np = None  # 为了最后对其进行保存
    img_list = []
    target_list = []
    print('receiving data...')
    for j in range(BATCH_SIZE):
        if args.dummy == 1:
            print('dummy data')
            image_np, target_np = get_one_data_dummy()
        else:
            image_np, target_np = get_one_data(conn, image_np, target_np, i)
        target_np[target_np >= NUM_CLASSES] = 0
        if image_np is None:
            save_path = '/tmp/{}.pth'.format(i)
            torch.save(model.state_dict(), save_path)
            print(save_path, 'stop')
            exit(0)
        image = trf(image_np)  # 必须为 uint8 格式，否则会报错：浮点数例外，核心已转储。
        image = image.unsqueeze(0)
        target = torch.from_numpy(target_np)
        target = target.unsqueeze(0).long()  # 必须为 long 类型，否则计算损失时会报错。
        img_list.append(image)
        target_list.append(target)
    print('received.')
    inp = torch.cat(img_list, dim=0).cuda()
    target = torch.cat(target_list, dim=0).cuda()
    out = model(inp)['out']
    # batch size 若是 1 则报错
    # ValueError: Expected more than 1 value per channel when training, got input size torch.Size([1, 256, 1, 1])
    loss = cross_entropy2d(out, target, size_average=True)
    print(loss.item())

    # compute gradient and do SGD step
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if i % 1000 == 0 or i == 1 or i == args.resume + 1:  # i == 1 or i == args.resume + 1 是为了看看下面的代码能不能正确保存。
        save_path = os.path.join(args.save_dir, '{}.pth'.format(i))
        torch.save(model.state_dict(), save_path)  # 是 .state_dict() 而不是 .state_dict
        cv2.imwrite(os.path.join(args.save_dir, '{}.jpg'.format(i)), image_np)
        cv2.imwrite(os.path.join(args.save_dir, '{}.png'.format(i)), target_np)
        print(save_path)
