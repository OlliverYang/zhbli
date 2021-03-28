import torch
import torch.nn.functional as F


def xcorr_depthwise(x, kernel):
    r"""
    Depthwise cross correlation. e.g. used for template matching in Siamese tracking network

    Arguments
    ---------
    x: torch.Tensor
        feature_x (e.g. search region feature in SOT)
    kernel: torch.Tensor
        feature_z (e.g. template feature in SOT)

    Returns
    -------
    torch.Tensor
        cross-correlation result
    """
    batch = int(kernel.size(0))
    channel = int(kernel.size(1))
    x = x.reshape(1, int(batch * channel), int(x.size(2)), int(x.size(3)))
    kernel = kernel.reshape(batch * channel, 1, int(kernel.size(2)),
                         int(kernel.size(3)))
    out = F.conv2d(x, kernel, groups=batch * channel)
    out = out.reshape(batch, channel, int(out.size(2)), int(out.size(3)))
    return out


class SimpleNet(torch.nn.Module):
    def __init__(self, cfg):
        super(SimpleNet, self).__init__()

        self.cfg = cfg

        NUM_CLASSES = cfg['NUM_CLASSES']
        OUT_CHANNEL = cfg['OUT_CHANNEL']
        KERNEL_SIZE = cfg['KERNEL_SIZE']
        DILATION = cfg['DILATION']
        PADDING = (DILATION * (KERNEL_SIZE - 1) + 1) // 2

        self.conv_first = torch.nn.Conv2d(3, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.bn_first = torch.nn.BatchNorm2d(OUT_CHANNEL)

        self.hidden = torch.nn.ModuleList([])
        for i in range(self.cfg['LAYER_NUMBER']):
            self.hidden.extend([torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)])
            self.hidden.extend([torch.nn.BatchNorm2d(OUT_CHANNEL)])
            self.hidden.extend([torch.nn.ReLU()])

        self.last_conv = torch.nn.Conv2d(OUT_CHANNEL, NUM_CLASSES, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.last_bn = torch.nn.BatchNorm2d(NUM_CLASSES)

    def forward(self, x, img_h, img_w):
        x = F.relu(self.bn_first(self.conv_first(x)))

        for i in range(self.cfg['LAYER_NUMBER'] - 3):
            x = self.hidden[i](x)

        x = self.hidden[-3](x)  # conv

        """互相关"""
        scale_x = x.shape[3] / img_w
        scale_y = x.shape[2] / img_h
        x1, y1, w, h = [70, 80, 350, 128]  # 相对于原始输入图像。未经过任何缩放。
        cx = int((x1 + w / 2) * scale_x)
        cy = int((y1 + h / 2) * scale_y)
        obj_vector = x[:, :, cy, cx].unsqueeze(2).unsqueeze(3)
        x = xcorr_depthwise(x, obj_vector)  # 互相关前，不 relu
        x = F.relu(x)  # 互相关后，relu
        """互相关"""

        """降维到类别数"""
        x = self.last_bn(self.last_conv(x))

        return x
