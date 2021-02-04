"""
对比不同网络的结果。用于论文的可视化。
"""
import os
import cv2
import glob
import numpy as np


def run_per_image(image_path, prediction_per_image, prediction_names):
    print(image_path)
    image = cv2.imread(image_path)
    for i in range(len(prediction_per_image)):
        prediction = prediction_per_image[i]
        x1, y1, w, h = prediction
        x2 = x1 + w
        y2 = y1 + h
        color = colors[prediction_names[i]]
        image = cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, thickness=12)
    image = cv2.resize(image, (800, 600))
    video_name = image_path.split('\\')[-2]
    image_name = image_path.split('\\')[-1]
    save_dir = os.path.join(save_root, video_name)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_path = os.path.join(save_dir, image_name)
    res = cv2.imwrite(save_path, image)
    assert res != False


def run_per_video(dataset_dir, prediction_paths):
    image_paths = sorted(glob.glob(os.path.join(dataset_dir, '0*.jpg')))
    predictions = [] * len(prediction_paths)
    prediction_names = [] * len(prediction_paths)
    for prediction_path in prediction_paths:
        predictions.append(np.loadtxt(prediction_path, delimiter=','))
        prediction_names.append(prediction_path.split('\\')[-3])
    for i in range(len(image_paths)):
        image_path = image_paths[i]
        prediction_per_image = [] * len(prediction_paths)
        for prediction in predictions:
            prediction_per_image.append(prediction[i])
        run_per_image(image_path, prediction_per_image, prediction_names)


def main():
    """"""
    dataset_dirs = sorted(glob.glob(os.path.join(dataset_root, 'GOT*')))
    for dataset_dir in dataset_dirs:
        video_name = dataset_dir.split('\\')[-1]
        prediction_paths = glob.glob(os.path.join(prediction_root, '*', video_name, '*_001.txt'))
        if single_video is not None and single_video != video_name:
            continue
        else:
            run_per_video(dataset_dir, prediction_paths)


if __name__ == '__main__':
    prediction_root = '.'
    dataset_root = 'D:\\MyDocuments\\datasets\\got10k\\test_data\\test'
    save_root = 'visualize'
    colors = {'Ours': [0, 255, 0], 'SiamMask': [0, 0, 255], 'SiamFCv2': [255, 0, 0]}  # BGR
    single_video = None
    main()
