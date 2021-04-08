# -*- coding: UTF-8 -*-
import os
from model import SimpleNet
import torchvision.transforms as T
import cv2
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from sigmoid_ce_retina import SigmoidCrossEntropyRetina
import random
import numpy as np

seed = 31415926
# 排除PyTorch的随机性：
torch.manual_seed(seed)  # cpu种子
torch.cuda.manual_seed(seed)       # 为当前GPU设置随机种子
torch.cuda.manual_seed_all(seed)  # 所有可用GPU的种子

# 排除第三方库的随机性
np.random.seed(seed)
random.seed(seed)

# 排除cudnn加速的随机性：
torch.backends.cudnn.enabled = True   # 默认值
torch.backends.cudnn.benchmark = False  # 默认为False
torch.backends.cudnn.deterministic = True # 默认为False;benchmark为True时,y要排除随机性必须为True


cfg = {'LR': 0.01, 'NUM_CLASSES': 1, 'IMG_SIZE': 1024, 'ITER': 256, 'GPU_ID': '3',
       'OUT_CHANNEL': 4, 'KERNEL_SIZE': 3, 'DILATION': 1, 'LAYER_NUMBER': 8} # NUM_CLASSES 若较大，则非常占显存

os.environ['CUDA_VISIBLE_DEVICES'] = cfg['GPU_ID']


def decode_segmap(image_, nc=21):
    label_colors = np.array([(0, 0, 0),  # 0=background
                             # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                             (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                             # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                             (0, 128, 128), (128, 128, 128), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                             # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                             (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                             # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                             (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

    r = np.zeros_like(image_).astype(np.uint8)
    g = np.zeros_like(image_).astype(np.uint8)
    b = np.zeros_like(image_).astype(np.uint8)

    for l in range(0, nc):
        idx = image_ == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]

    rgb_ = np.stack([r, g, b], axis=2)
    return rgb_


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
        loss_ /= mask.data.sum().float()
    return loss_


def train():
    model = SimpleNet(cfg).cuda().train()

    optimizer = torch.optim.SGD(model.parameters(), cfg['LR'],
                                momentum=0.9,
                                weight_decay=1e-4)

    criteria = SigmoidCrossEntropyRetina()

    trf = T.Compose([T.ToTensor(),  # 转换为0~1
                     T.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])])
    image_np = cv2.imread('./1.jpg')
    img_h, img_w = image_np.shape[:2]

    image_np = cv2.resize(image_np, (cfg['IMG_SIZE'], cfg['IMG_SIZE']))
    image = trf(image_np)
    inp = image.unsqueeze(0).cuda()

    gt = cv2.imread('./1.png')
    gt = cv2.resize(gt, (cfg['IMG_SIZE'], cfg['IMG_SIZE']))
    gt = gt[:, :, 0] + gt[:, :, 1] + gt[:, :, 2]
    gt[gt != 0] = 1
    target = torch.from_numpy(gt).cuda()
    target = target.unsqueeze(0).long()  # 必须为 long 类型，否则计算损失时会报错。

    for i in range(cfg['ITER']+1):
        out = model(inp, img_h, img_w)

        """计算损失"""
        # loss = cross_entropy2d(out, target, size_average=True)
        loss = criteria.forward(out, target)
        print(i, loss.item())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    om = out[0][0].data.cpu().numpy()
    om[om>=0] = 255
    om[om<0] = 0
    om = om.astype(np.uint8)
    # rgb = decode_segmap(om)
    plt.imshow(om)
    plt.axis('off')
    plt.show()

    om = target[0].detach().cpu().numpy()
    rgb = decode_segmap(om)
    plt.imshow(rgb)
    plt.axis('off')
    plt.show()

    print(cfg)


if __name__ == '__main__':
    train()
