from torchvision import models
import torch
import cv2
import os
import torchvision.transforms as T
import matplotlib.pyplot as plt
import numpy as np
import torch.nn.functional as F
import time


NUM_CLASSES = 16  # 若较大，则非常占显存
GPU_ID = 2
ITER_NUM = 19000

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


os.environ["CUDA_VISIBLE_DEVICES"] = str(GPU_ID)
model = models.segmentation.deeplabv3_resnet50(num_classes=NUM_CLASSES).cuda()
model.load_state_dict(torch.load('/tmp/{}.pth'.format(ITER_NUM)))
model.train()
print('no')

trf = T.Compose([T.ToTensor(),  # 转换为0~1
                 T.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])])
image_np = cv2.imread('/tmp/{}.jpg'.format(ITER_NUM))
image = trf(image_np)
inp = image.unsqueeze(0).cuda()
inp = torch.cat((inp, inp))
print('no no')
out = model(inp)['out']
out = out[0].unsqueeze(0)
print('no no no')
om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
rgb = decode_segmap(om)
plt.imshow(rgb)
plt.axis('off')
plt.show()

gt = cv2.imread('/tmp/{}.png'.format(ITER_NUM))[:, :, 0]
target = torch.from_numpy(gt).cuda()
target = target.unsqueeze(0).long()  # 必须为 long 类型，否则计算损失时会报错。

loss = cross_entropy2d(out, target, size_average=True)
print(loss.item())
