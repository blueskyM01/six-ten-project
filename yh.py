import cv2
import numpy as np
from matplotlib import pyplot as plt


def fun1():
    img = cv2.imread('F:/project/buaa/610_new/python_610/parachute_tracking_610/yolo/p2.jpeg', cv2.IMREAD_GRAYSCALE)
    # bins->图像中分为多少格；range->图像中数字范围
    plt.hist(img.ravel(), bins=256, range=[0, 256]);
    plt.show()


def fun2():
    img = cv2.imread('F:/project/buaa/610_new/python_610/parachute_tracking_610/yolo/p2.jpeg', cv2.IMREAD_COLOR)
    color = ('b', 'g', 'r')
    for i, col in enumerate(color):
        histr = cv2.calcHist([img], [i], None, [256], [0, 256])


        plt.plot(histr, color=col)
    plt.xlim([0, 256])
    plt.show()


fun2()
