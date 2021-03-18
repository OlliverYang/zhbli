import numpy as np
import rpack
from utils.utils import xywh2xyxy, xyxy2xywh, bbox_iou
from datetime import datetime
import torch
import cv2


def generate_no_overlap_boxes(img_w, img_h, real_box_xyxy):
    real_x1, real_y1, real_x2, real_y2 = real_box_xyxy[0]
    real_w = real_x2 - real_x1 + 1
    real_h = real_y2 - real_y1 + 1

    """随机生成需要平铺的数量"""
    real_box_size = real_w * real_h
    img_size = img_w * img_h
    max_new_box_num = img_size // real_box_size - 1
    if max_new_box_num <= 0:
        return np.array([])
    n = np.random.randint(max_new_box_num//4, max_new_box_num*2, 1, dtype=np.int)
    n = np.minimum(n, 128)

    """生成需要平铺的边框 w h"""
    w = np.random.randint(real_w/2, real_w*2, n)
    h = np.random.randint(real_h/2, real_h*2, n)
    boxes_wh = np.stack((w, h), axis=1)


    """对边框进行平铺"""
    positions = rpack.pack(boxes_wh.tolist())  # w, h, ret: x1 y1
    positions = np.array(positions)
    try:
        x1 = positions[:, 0]
    except Exception:
        return np.array([])
    y1 = positions[:, 1]

    """得到边框的xyxy格式"""
    y2 = y1 + h
    x2 = x1 + w

    """删除越界框"""
    selected = np.logical_and(x2 < img_w, y2 < img_h)
    w = w[selected]
    h = h[selected]
    x1 = x1[selected]
    y1 = y1[selected]
    x2 = x2[selected]
    y2 = y2[selected]

    """计算右边界"""
    if len(x2) == 0:
        return np.array([])
    max_x2 = np.max(x2)
    max_y2 = np.max(y2)

    scale_w = img_w / max_x2
    scale_h = img_h / max_y2

    """计算cx, cy"""
    cx = x1 + w / 2
    cy = y1 + h / 2

    """平铺到整个画面"""
    cx_full = cx * scale_w
    cy_full = cy * scale_h
    boxes_full_cxywh = np.stack([cx_full, cy_full, w, h], axis=1)

    """删除与原始box重叠的边框"""
    ious = bbox_iou(torch.from_numpy(real_box_xyxy).float(),
                    torch.from_numpy(boxes_full_cxywh).float(), x1y1x2y2=False)
    boxes_full_cxywh = boxes_full_cxywh[ious.numpy()[0] == 0]

    """返回新box"""
    return boxes_full_cxywh


def display(boxes, format, img_w, img_h):
    img = np.ones((img_h, img_w))
    for box in boxes:
        if format == 'xyxy':
            x1, y1, x2, y2  = [int(var) for var in box]
        elif format == 'cxywh':
            cx, cy, w, h = [int(var) for var in box]
            x1 = cx - w//2
            y1 = cy - h//2
            x2 = cx + w//2
            y2 = cy + h//2
        img = cv2.rectangle(img, (x1,y1), (x2,y2), (255,0,0))
    cv2.imwrite('/tmp/00/000.jpg', img)


def main():
    img_w = 1088
    img_h = 688
    real_box_xyxy = np.array([[20, 40, 256, 256]])
    boxes_full_cxywh = generate_no_overlap_boxes(img_w, img_h, real_box_xyxy)
    display(boxes_full_cxywh, 'cxywh', img_w, img_h)


if __name__ == '__main__':
    main()