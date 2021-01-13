"""
用于分析随着迭代数量的增加对性能的影响。
"""

import matplotlib.pyplot as plt


def main():
    #iter_num = [0,1,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
    iter_num = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    FGT_AO=[0.004, 0.002, 0.002, 0.002, 0.002, 0.002, 0.003, 0.007, 0.042, 0.299, 0.668, 0.746, 0.781, 0.798, 0.820, 0.821, 0.818]
    FGT_SR_50 = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.001, 0.005, 0.044, 0.335, 0.749, 0.822, 0.855, 0.872, 0.895, 0.897, 0.890]
    GT_AO=[0.760, 0.757, 0.756, 0.757, 0.757, 0.758, 0.759, 0.753, 0.720, 0.474, 0.150, 0.095, 0.071, 0.041, 0.032, 0.032, 0.035]
    GT_SR_50=[0.897, 0.894, 0.891, 0.893, 0.891, 0.893, 0.896, 0.888, 0.852, 0.559, 0.164, 0.098, 0.066, 0.031, 0.021, 0.022, 0.023]
    SSIM=[1.00, 1.00, 1.00, 1.00, 1.00, 0.99, 0.99, 0.97, 0.93, 0.86, 0.86, 0.87, 0.88, 0.88, 0.88, 0.88, 0.88]
    MSE=[0.00, 0.51, 0.26, 0.32, 0.37, 0.48, 0.84, 2.03, 5.65, 15.10, 25.43, 23.70, 21.89, 20.69, 20.49, 20.03, 20.87]
    
    linewidth = 3
    fig=plt.figure(figsize=(10,4))
    #plt.axes(xscale = "log")   
    start = 8
    plt.plot(iter_num[start:],FGT_AO[start:],linewidth=linewidth, marker='v',markersize='8',alpha=1)
    plt.plot(iter_num[start:],FGT_SR_50[start:],linestyle='-.',linewidth=linewidth, marker='s')
    plt.plot(iter_num[start:],GT_AO[start:],linewidth=linewidth, marker='s',markersize='8',alpha=1)
    plt.plot(iter_num[start:],GT_SR_50[start:],linestyle='-.',linewidth=linewidth, marker='s')
    #plt.plot(iter_num,SSIM)
    #plt.plot(iter_num,MSE)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()