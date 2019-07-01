import cv2
import numpy as np

image1 = cv2.imread('H:/demo/yolo3_tensorflow_610/p-temp.png')
def m4_cutImage(image, box):
    lt_x, lt_y, br_x, br_y = box
    cut = image[lt_x:br_x, lt_y:br_y, :]
    return cut

cut = m4_cutImage(image1, [30,10,90,50])
print(cut.shape)
print(len([]))
print(image1.shape)
cv2.imshow('imms',cut)
cv2.waitKey(0)