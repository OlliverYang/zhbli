from torch.utils.data import Dataset
import pickle
import random
import cv2

class GOT10k(Dataset):
    def __init__(self, transforms, cfg):
        with open('/home/zhbli/Dataset/data2/got10k/train.pkl', "rb") as f:
            self.data_dict = pickle.load(f)
            self.transforms = transforms
            self.cfg = cfg
        return

    def __getitem__(self, index):
        video_name = random.choice(list(self.data_dict.keys()))
        #print('no video random', end=' '); video_name = list(self.data_dict.keys())[0]
        image_id = random.randint(0, len(self.data_dict[video_name]['img_files']) - 1)
        img_path = self.data_dict[video_name]['img_files'][image_id]
        anno_xywh = self.data_dict[video_name]['anno'][image_id]
        image_np = cv2.imread(img_path)
        img_h, img_w = image_np.shape[:2]
        image_np = cv2.resize(image_np, (self.cfg['IMG_SIZE'], self.cfg['IMG_SIZE']))
        image = self.transforms(image_np).cuda()
        return (image, anno_xywh, img_h, img_w)

    def __len__(self):
        return 10000
