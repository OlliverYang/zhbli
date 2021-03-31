import os
from model import Model
import torchvision.transforms as T
import cv2
import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from sigmoid_ce_retina import SigmoidCrossEntropyRetina
import random
import numpy as np
from got10k import GOT10k


"""排除随机性"""
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
"""排除随机性"""


"""配置参数"""
MODEL_PATH = '/tmp/model.pth'
cfg = {'LR': 0.1, 'IMG_SIZE': 256, 'GPU_ID': '1',
       'OUT_CHANNEL': 1024, 'KERNEL_SIZE': 3, 'DILATION': 1, 'BATCH_SIZE': 1, 'RESUME': True}
os.environ['CUDA_VISIBLE_DEVICES'] = cfg['GPU_ID']
"""配置参数"""


def visualize(heat_map_np, prediction_cxy):
    """
    :param heat_map_np: b, 1, h, w
    :return:
    """
    def sigmoid(x):
        s = 1 / (1 + np.exp(-x))
        return s
    for heatmap, cxy in zip(heat_map_np, prediction_cxy):
        heatmap = (sigmoid(heatmap[0][0]) * 255).astype(np.uint8)
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_GRAY2RGB)
        heatmap = cv2.circle(heatmap, cxy, radius=0, color=(255, 0, 0), thickness=1)

        heatmap_size = heatmap.shape[0]
        heatmap = cv2.resize(heatmap, (512, 512))
        assert cv2.imwrite('/tmp/heatmap_{}.png'.format(heatmap_size), heatmap)


def train(model, inp, trf):
    """"""
    """建立 dataset 和 dataloader"""
    dataset = GOT10k(trf, cfg)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=cfg['BATCH_SIZE'])

    """建立优化器"""
    optimizer = torch.optim.SGD(model.parameters(), cfg['LR'],
                                momentum=0.9,
                                weight_decay=1e-4)
    """建立优化器"""

    """循环训练"""
    for epoch in range(20):
        for i, item in enumerate(dataloader):
            if i > 10000:
                break
            inp = item[0]
            anno_xywh = item[1]
            img_h = item[2]
            img_w = item[3]
            """前向传播与计算损失"""
            layer, loss, heat_map_np = model(inp, img_h, img_w, anno_xywh)
            print(epoch, i, layer, loss.item())

            """梯度反传与更新"""
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            """梯度反传与更新"""
        # visualize(heat_map_np)
        torch.save(model, MODEL_PATH)


def test(model, inp, img_h, img_w):
    heat_map_np, prediction_cxy = model.test(inp, img_h, img_w)
    visualize(heat_map_np, prediction_cxy)


def main(phase):
    """"""
    """建立模型"""
    model = Model(cfg).cuda()
    if cfg['RESUME']:
        print('resume')
        model = torch.load(MODEL_PATH)
    if phase == 'train':
        model = model.train()
    else:
        model = torch.load(MODEL_PATH).eval()
    """建立模型"""

    """读入图像"""
    trf = T.Compose([T.ToTensor(),  # 转换为0~1
                     T.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])])
    image_np = cv2.imread('./1.jpg')
    img_h, img_w = image_np.shape[:2]
    image_np = cv2.resize(image_np, (cfg['IMG_SIZE'], cfg['IMG_SIZE']))
    image = trf(image_np)
    inp = image.unsqueeze(0).cuda()
    """读入图像"""

    if phase == 'train':
        train(model, inp, trf)
    else:
        """运行测试"""
        test(model, inp, img_h, img_w)
        """运行测试"""


if __name__ == '__main__':
    main('train')
    #main('test')
