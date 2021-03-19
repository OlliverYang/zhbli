import os
import numpy as np
import cv2
import argparse


def run_per_frame(video_name, video_path, image_name, gt):
    frame_path = os.path.join(video_path, image_name)
    frame = cv2.imread(frame_path) # h, w, 3
    im_h, im_w = frame.shape[:2]
    x1, y1, w, h = [int(var) for var in gt]
    cx = x1 + w/2
    cy = y1 + h/2
    if phase == 'crop':
        save_root = "/home/zhbli/Dataset/data2/custom/object_ReID/GOT-10k/train"
        img_crop = frame[y1:y1+h, x1:x1+w]
        save_dir = os.path.join(save_root, video_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, image_name)
        if os.path.exists(save_path):
            print('continue', save_path)
            return
        if len(img_crop) != 0:
            cv2.imwrite(save_path, img_crop)
        else:
            print('wrong size')
            cv2.imwrite(save_path, frame)
        print(save_path)
    elif phase == 'gen_label':
        save_root = '/home/etvuz/projects/FairMOT/datasets/GOT-10k/labels_with_ids/train'
        save_dir = os.path.join(save_root, video_name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, image_name[:-4]+'.txt')
        tid_curr = int(video_name[-3:])
        label_str = '0 {:d} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(
            tid_curr, cx / im_w, cy / im_h, w / im_w, h / im_h)
        print(save_path)
        # tid_curr: 即物体的类别。由于 SOT 中一段视频对应一个物体，所以视频名即为 tid_curr
        with open(save_path, 'w') as f:
            f.write(label_str)
    elif phase == 'gen_img':
        save_path = '/home/etvuz/projects/FairMOT/src/data/got10k.train'
        with open(save_path, 'a') as f:
            f.write(frame_path+'\n')


def run_per_video(video_name):
    print(video_name)
    video_path = os.path.join(dataset_root, video_name)
    gt_path = os.path.join(video_path, 'groundtruth.txt')
    gts = np.loadtxt(gt_path, delimiter=',')
    image_names = sorted(os.listdir(video_path))
    for image_name, gt in zip(image_names, gts):
        if image_name[-4:] != '.jpg':
            continue
        run_per_frame(video_name, video_path, image_name, gt)


def main():
    train_video_names = sorted(os.listdir(dataset_root))
    for train_video_name in train_video_names:
        if train_video_name[:3] != 'GOT':
            continue
        run_per_video(train_video_name)


if __name__ == '__main__':
    dataset_root = '/home/etvuz/projects/FairMOT/datasets/GOT-10k/images/train'
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', help='crop gen_label gen_img')
    args = parser.parse_args()
    phase = args.phase
    main()