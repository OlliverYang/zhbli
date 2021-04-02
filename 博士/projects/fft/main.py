import cv2
import numpy as np
import matplotlib.pyplot as plt


THRESHOLD = 9

# 读取图像
img = cv2.imread('1.jpg', 0)
 
# 傅里叶变换
fimg = np.fft.fft2(img)
fshift = np.fft.fftshift(fimg)

# fft 结果是复数，其绝对值结果是振幅
fshift_abs = np.log(np.abs(fshift))
 
# 设置高通滤波器
rows, cols = img.shape
crow, ccol = int(rows/2), int(cols/2)
# fshift[crow-30:crow+30, ccol-30:ccol+30] = 0
fshift[fshift_abs<THRESHOLD] = 0
fshift_abs[fshift_abs<THRESHOLD] = 0
print(fshift_abs[fshift_abs>=THRESHOLD].size)
 
# 傅里叶逆变换
ishift = np.fft.ifftshift(fshift)
iimg = np.fft.ifft2(ishift)
iimg = np.abs(iimg)
 
# 显示原始图像和高通滤波处理图像
plt.subplot(221), plt.imshow(img, 'gray'), plt.title('gray Image')
plt.axis('off')
plt.subplot(222), plt.imshow(iimg, 'gray'), plt.title('Result Image')
plt.axis('off')
plt.subplot(223), plt.imshow(fshift_abs, 'gray'), plt.title('fshift_abs')
plt.axis('off')
plt.show()