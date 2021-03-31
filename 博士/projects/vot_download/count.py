from zipfile import ZipFile
import os

def main():
    video_number = 0
    image_number = 0
    save_root = './dataset'
    videos = os.listdir(save_root)
    """列出每个文件夹"""
    for video in videos:
        video_number += 1
        """处理每个压缩包"""
        zip_path = os.path.join(save_root, video, 'color.zip')
        with ZipFile(zip_path) as zip:
            files = zip.namelist()
            image_number += len(files)
    print('video_number: ', video_number, '; image_number: ', image_number)


if __name__ == "__main__":
    main()