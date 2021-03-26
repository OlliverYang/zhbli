# -*- coding: utf-8 -*-

import cv2
import numpy as np

from videoanalyst.pipeline.utils.misc import tensor_to_imarray, tensor_to_numpy


def show_img_FCOS(training_data,
                  distractor_boxes_recentered=[],
                  dataset='untitled'):
    r"""
    Visualize training data
    """

    target_img = tensor_to_imarray(training_data["im_z"])
    image_rand_focus = tensor_to_imarray(training_data["im_x"])

    gt_datas = [
        training_data["cls_gt"], training_data["ctr_gt"],
        training_data["box_gt"]
    ]

    '''设定超参数'''
    IM_H = 768
    IM_W = 1024
    STRIDE = 8
    x_size_h = IM_H
    x_size_w = IM_W
    score_size_h = IM_H // STRIDE
    score_size_w = IM_W // STRIDE

    total_stride = STRIDE

    '''得到 gt box'''
    # cx, cy, w, h = training_data['bbox_x'][0].data.cpu().numpy()
    # x1 = int(cx - w / 2)
    # y1 = int(cy - h / 2)
    # x2 = int(cx + w / 2)
    # y2 = int(cy + h / 2)
    box = training_data['bbox_x'][0].data.cpu().numpy()
    x1, y1, x2, y2 = [int(var) for var in box]

    '''计算 cls_gt'''
    cls_gt = (training_data['cls_gt'][0].data.cpu().numpy().reshape((score_size_h, score_size_w))*255).astype(np.uint8)  # 12288, 1, 0 or 1
    cv2.imwrite('/tmp/cls.jpg', cls_gt)

    """读入图片"""
    show_img = cv2.resize(image_rand_focus, (x_size_w, x_size_h))
    show_img_h, show_img_w = show_img.shape[:2]

    show_img = cv2.rectangle(show_img, (x1, y1), (x2, y2), (255, 0, 0))
    cv2.imwrite('/tmp/search_img.jpg', show_img)

    gt_datas = [tensor_to_numpy(t) for t in gt_datas]
    gt_target = np.concatenate(gt_datas, axis=-1)
    if gt_target.ndim == 3:
        gt_target = gt_target[0]

    """计算 ctr_gt"""
    cls_gt = (training_data['ctr_gt'][0].data.cpu().numpy().reshape((score_size_h, score_size_w)) * 255).astype(
        np.uint8)  # 12288, 1, 0 or 1
    cv2.imwrite('/tmp/ctr.jpg', cls_gt)

    score_offset = 0

    color = dict()
    color['pos'] = (0, 0, 255)
    color['ctr'] = (0, 255, 0)
    color['neg'] = (255, 0, 0)
    color['ign'] = (255, 255, 255)
    # to prove the correctness of the gt box and sample point
    gts = gt_target[gt_target[:, 0] == 1, :][:, 2:]

    fm_margin = score_offset

    gt_indexes = (gt_target[:, 0] == 1)
    if gt_indexes.any():
        gt = gt_target[gt_indexes, :][0, 2:]
        cv2.rectangle(show_img, (int(gt[0]), int(gt[1])),
                      (int(gt[2]), int(gt[3])), color['pos'])

    pos_cls_gt = (gt_target[:, 0] == 1)
    pos_indexes = np.argsort(pos_cls_gt)[len(gt_target) - np.sum(pos_cls_gt):]

    ctr_gt = gt_target[:, 1]

    ign_cls_gt = (gt_target[:, 0] == -1)
    ign_indexes = np.argsort(ign_cls_gt)[len(gt_target) - np.sum(ign_cls_gt):]

    neg_cls_gt = (gt_target[:, 0] == 0)
    neg_indexes = np.argsort(neg_cls_gt)[len(gt_target) - np.sum(neg_cls_gt):]

    '''画正样本点'''
    for index in pos_indexes:  # 遍历 ctr 特征图的每个位置

        """将特征图的位置转化为原始图像的位置"""
        # note that due to ma 's fcos implementation, x and y are switched
        pos = (score_offset + (index % score_size_w) * total_stride,
               score_offset + (index // score_size_w) * total_stride)  # x, y。原始代码公式很明显是错的。因为原来用的是正方形，错误没有显现。

        ctr = ctr_gt[index]  # 0 到 1 的值
        color_pos = tuple(
            (np.array(color['pos']) + ctr * np.array(color['ctr'])).astype(
                np.uint8).tolist())
        cv2.circle(show_img, pos, 2, color_pos, -1)

    '''画负样本点'''
    for index in neg_indexes:
        # note that due to ma 's fcos implementation, x and y are switched
        pos = (score_offset + (index % score_size_w) * total_stride,
               score_offset + (index // score_size_w) * total_stride)
        ctr = ctr_gt[index]
        color_neg = tuple(
            (np.array(color['neg']) + ctr * np.array(color['ctr'])).astype(
                np.uint8).tolist())
        cv2.circle(show_img, pos, 2, color_neg, -1)

    '''画忽略的点'''
    for index in ign_indexes:
        # note that due to ma 's fcos implementation, x and y are switched
        pos = (score_offset + (index % score_size_w) * total_stride,
               score_offset + (index // score_size_w) * total_stride)
        cv2.circle(show_img, pos, 2, color['ign'], -1)

    cv2.putText(show_img, 'pos', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                color['pos'])
    cv2.putText(show_img, 'neg', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                color['neg'])
    cv2.putText(show_img, 'ign', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                color['ign'])

    cv2.putText(show_img, dataset, (20, show_img_h - 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

    print('distractor_boxes:', len(distractor_boxes_recentered))
    if len(distractor_boxes_recentered) > 0:
        for box in distractor_boxes_recentered:
            cv2.rectangle(show_img, (int(box[0]), int(box[1])),
                          (int(box[2]), int(box[3])), color['neg'])
    cv2.imwrite('/tmp/search.jpg', show_img)
    cv2.imwrite('/tmp/target.jpg', target_img)
    return
