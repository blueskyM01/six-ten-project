# import m4_target_detection as det
# import cv2
# from scipy.spatial.distance import pdist
# import numpy as np
#
# image1 = cv2.imread('H:/demo/yolo3_tensorflow_610/p-temp.png')
# m4_temp_feat = det.m4_feat_extracter(image1)
# boxes_temp = det.m4_detect(image1, True)
#
#
#
#
# def m4_compute_similar(temp_feat, feat):
#     distance = 1 - pdist(np.append(m4_temp_feat, m4_feat, axis=0), 'cosine')
#     return distance[0]
#
# def m4_cutImage(image, box):
#     lt_x = max(0, int(box[0]))
#     lt_y = max(0, int(box[1]))
#     br_x = max(0, int(box[2]))
#     br_y = max(0, int(box[3]))
#     cut = image[lt_y:br_y ,lt_x:br_x, :]
#     return cut
#
#
#
# vid = cv2.VideoCapture('F:/project/buaa/610_new/jzs.mp4')
# while 1:
#     ret, img_ori = vid.read()
#     boxes = det.m4_detect(img_ori, True)
#
#     for i in range(len(boxes)):
#         # print('kkk:',i)
#         # print(boxes[i])
#
#         cut = m4_cutImage(img_ori, boxes[i])
#         m4_feat = det.m4_feat_extracter(cut)
#
#         m4_simlar = m4_compute_similar(m4_feat, m4_temp_feat)
#         print(m4_simlar)
#         if m4_simlar>0.7:
#             cv2.rectangle(img_ori, (boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3]), (255,255,255), 4)
#         else:
#             cv2.rectangle(img_ori, (boxes[i][0], boxes[i][1]), (boxes[i][2], boxes[i][3]), (0,255,0), 2)
#
#     cv2.imshow('show',img_ori)
#     cv2.waitKey(20)
#
#
#
# vid.release()



import ctypes
lib = ctypes.cdll.LoadLibrary("F:/project/buaa/610_new\python_610/m4_dll_test/x64/Debug/m4_dll_test.dll")
lib.myFun()
















