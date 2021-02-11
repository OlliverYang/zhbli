"""
论文需要展示一下数据集，也就是把每张图像+边框画出来。
"""


import os
import cv2
import glob
import numpy as np


def run_per_image(image_path, gt):
    print(image_path)
    image = cv2.imread(image_path)
    
    x1, y1, w, h = gt
    x2 = x1 + w
    y2 = y1 + h
    
    image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), [0, 255, 0], thickness=12)
    image = cv2.resize(image, (800, 600))
    video_name = image_path.split('\\')[-2]
    image_name = image_path.split('\\')[-1]
    save_path = os.path.join(save_root, video_name + '.jpg')
    res = cv2.imwrite(save_path, image)
    assert res != False
    
    
def run_per_video(dataset_dir, gt_path):
    image_path = os.path.join(dataset_dir, '00000001.jpg')
    gt = np.loadtxt(gt_path, delimiter=',')
    run_per_image(image_path, gt)


def main():
    """"""
    dataset_dirs = sorted(glob.glob(os.path.join(dataset_root, 'GOT*')))
    for dataset_dir in dataset_dirs:
        video_name = dataset_dir.split('\\')[-1]
        gt_path = os.path.join(dataset_root, video_name, 'groundtruth.txt')
        run_per_video(dataset_dir, gt_path)
        
        
if __name__ == '__main__':
    dataset_root = 'D:\\MyDocuments\\datasets\\got10k\\test_data\\test'
    save_root = 'visualize'
    main()