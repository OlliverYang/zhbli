import os
import cv2
import glob
import numpy as np


def run_per_image(image_path, prediction):
    image = cv2.imread(image_path)
    x1, y1, w, h = prediction
    x2 = x1 + w
    y2 = y1 + h
    image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), thickness=8)
    image = cv2.resize(image, (800, 600))
    video_name = image_path.split('/')[-3]
    image_name = image_path.split('/')[-1]
    save_dir = os.path.join(save_root, video_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, image_name)
    res = cv2.imwrite(save_path, image)
    assert res != False


def run_per_video(dataset_dir, prediction_path):
    image_paths = sorted(glob.glob(os.path.join(dataset_dir, 'img', '0*.jpg')))
    prediction = np.loadtxt(prediction_path, delimiter=',')
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        if i % 100 == 0:
            print(image_path)
        run_per_image(image_path, prediction[i])


def main():
    """"""
    dataset_dirs = sorted(glob.glob(os.path.join(dataset_root, '*', '*-*')))
    for dataset_dir in dataset_dirs:
        video_name = dataset_dir.split('/')[-1]
        prediction_path = os.path.join(prediction_root, video_name + '.txt')
        if single_video is not None and single_video != video_name:
            continue
        else:
            run_per_video(dataset_dir, prediction_path)


if __name__ == '__main__':
    prediction_root = '/home/etvuz/projects/language_tracking/logs_tracker/GOT-Benchmark/result/LaSOT/siamfcpp_googlenet'
    dataset_root = '/home/zhbli/Dataset/data3/LASOT'
    save_root = '/tmp/0visualize'
    colors = {'Ours': [0, 255, 0], 'SiamMask': [0, 0, 255], 'SiamFCv2': [255, 0, 0]}  # BGR
    single_video = 'basketball-11'
    main()