import json
import os
import shutil
import requests


def main():
    json_path = './vot2019_rgbd.json'
    save_root = './dataset'
    downloaded = './downloaded'
    with open(json_path, 'r') as f:
        json_file = json.load(f)
    sequences = json_file['sequences']
    sub_dirs = ['annotations', 'color', 'depth']

    """处理每段视频"""
    for sequence in sequences:
        name = sequence['name']
        save_dir = os.path.join(save_root, name)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        """若已经存在完整数据，则该视频成功"""
        if sorted(os.listdir(save_dir)) == sorted(['annotations.zip', 'color.zip', 'depth.zip']):
            continue

        """对于不完整的数据集，打印其链接"""
        for sub_dir in sub_dirs:
            if sub_dir == 'annotations':
                url = sequence[sub_dir]['url']
            else:
                url = sequence['channels'][sub_dir]['url']
            raw_name = url.split('/')[-1]
            downloaded_path = os.path.join(downloaded, raw_name)
            save_path = os.path.join(save_dir, sub_dir+'.zip')
            if os.path.exists(save_path):
                continue
            if os.path.exists(downloaded_path):
                print(sub_dir, 'exist', end=' ')
                shutil.move(downloaded_path, save_path)
            else:
                # print(sub_dir, 'not exist', end=' ')
                print(url)
                # file = requests.get(url)
                # print('downloading')
                # open(save_path, 'wb').write(file.content)
                # print(url, 'downloaded')
            
        

if __name__ == "__main__":
    main()