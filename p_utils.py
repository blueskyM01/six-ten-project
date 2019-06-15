import numpy as np
import cv2

def m4_CoordinateConvert(x0, y0, x1, y1, win_width, win_heigh, image_width, image_heigh):
    '''
    :param x0: 矩形框的左上点x坐标(窗口上的）
    :param y0: 矩形框的左上点y坐标(窗口上的）
    :param x1: 矩形框的右下点x坐标(窗口上的）
    :param y1: 矩形框的右下点y坐标(窗口上的）
    :param win_width: 显示窗口的长度
    :param win_heigh: 显示窗口的宽度
    :param image_width: 图像的宽度
    :param image_heigh: 图像的宽度
    :return: 图像上对应的坐标
    '''
    m4_ratioX = image_width / win_width
    m4_ratioY = image_heigh / win_heigh

    x_tl = x0 * m4_ratioX
    y_tl = y0 * m4_ratioY
    x_br = x1 * m4_ratioX
    y_br = y1 * m4_ratioY
    m4_Coordinate = (int(x_tl), int(y_tl), int(x_br), int(y_br))
    return m4_Coordinate



