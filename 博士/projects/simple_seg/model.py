import torch
import torch.nn.functional as F


NUM_CLASSES = 16  # 若较大，则非常占显存
OUT_CHANNEL = 64
KERNEL_SIZE = 3
DILATION = 1
PADDING = (DILATION*(KERNEL_SIZE-1) + 1)//2
print(PADDING)

class SimpleNet(torch.nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.conv1 = torch.nn.Conv2d(3,           OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv2 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv3 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv4 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv5 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv6 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv7 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv8 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv9 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv10 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv11 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv12 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv13 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv14 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv15 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.conv16 = torch.nn.Conv2d(OUT_CHANNEL, OUT_CHANNEL, KERNEL_SIZE, dilation=DILATION, padding=PADDING)
        self.last_conv = torch.nn.Conv2d(OUT_CHANNEL, NUM_CLASSES, KERNEL_SIZE, dilation=DILATION, padding=PADDING)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = F.relu(self.conv5(x))
        # x = F.relu(self.conv6(x))
        # x = F.relu(self.conv7(x))
        # x = F.relu(self.conv8(x))
        # x = F.relu(self.conv9(x))
        # x = F.relu(self.conv10(x))
        # x = F.relu(self.conv11(x))
        # x = F.relu(self.conv12(x))
        # x = F.relu(self.conv13(x))
        # x = F.relu(self.conv14(x))
        # x = F.relu(self.conv15(x))
        # x = F.relu(self.conv16(x))
        x = self.last_conv(x)
        return x
