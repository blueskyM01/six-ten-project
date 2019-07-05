from __future__ import division, print_function

import tensorflow as tf
import numpy as np
import argparse
import cv2
import time
from yolo.misc_utils import parse_anchors, read_class_names
from yolo.nms_utils import gpu_nms
from yolo.plot_utils import get_color_table, plot_one_box
from yolo.model import yolov3
from yolo.vgg16 import Vgg16
from scipy.spatial.distance import pdist
from yolo.IOU import x1_IOU

class m4_Switch_Track:
    def __init__(self, anchors, classes):
        self.anchors = parse_anchors(anchors)
        self.classes = read_class_names(classes)
        self.num_class = len(self.classes)
        self.new_size = [416, 416]

        color_table = get_color_table(self.num_class)

        self.input_data = tf.placeholder(tf.float32, [1, self.new_size[1], self.new_size[0], 3], name='input_data')
        yolo_model = yolov3(self.num_class, self.anchors)
        with tf.variable_scope('yolov3'):
            pred_feature_maps = yolo_model.forward(self.input_data, False)
        pred_boxes, pred_confs, pred_probs = yolo_model.predict(pred_feature_maps)
        pred_scores = pred_confs * pred_probs
        self.boxes, self.scores, self.labels = gpu_nms(pred_boxes, pred_scores, self.num_class,
                                        max_boxes=30, score_thresh=0.01,
                                        nms_thresh=0.5)  # score_thresh=0.01, nms_thresh=0.35

    def m4_feat_extracter(self, image_):
        feat = cv2.resize(image_, (224, 224), interpolation=cv2.INTER_CUBIC)
        feat_np = np.asarray([feat])
        [m4_feat_] = self.sess.run([self.m4_feat], feed_dict={self.image_bgr: feat_np})
        return m4_feat_

    def m4_detect(self, sess, img_ori, is_search_p, track_box_):
        '''

        :param sess:
        :param img_ori:
        :param is_search_p:
        :param track_box: [lt_x, lt_y, br_x, br_y]
        :return: 存储这样点[lt_x, lt_y, w, h]的list
        '''

        track_box = track_box_.copy()
        height_ori, width_ori = img_ori.shape[:2]
        img = cv2.resize(img_ori, tuple(self.new_size))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.asarray(img, np.float32)
        img = img[np.newaxis, :] / 255.

        boxes_, scores_, labels_ = sess.run([self.boxes, self.scores, self.labels], feed_dict={self.input_data: img})
        # boxes_:[lt_x, lt_y, w, h]

        # rescale the coordinates to the original image
        boxes_[:, 0] *= (width_ori / float(self.new_size[0]))
        boxes_[:, 2] *= (width_ori / float(self.new_size[0]))
        boxes_[:, 1] *= (height_ori / float(self.new_size[1]))
        boxes_[:, 3] *= (height_ori / float(self.new_size[1]))

        m4_FilterBoxes = []
        track_box[2] = track_box[2] - track_box[0]
        track_box[3] = track_box[3] - track_box[1]
        for boxes in boxes_:
            boxes[2] = boxes[2] - boxes[0]
            boxes[3] = boxes[3] - boxes[1]
            m4_IouScore = x1_IOU(track_box, boxes)
            if m4_IouScore < 0.3:
                m4_FilterBoxes.append(boxes)
        return m4_FilterBoxes

    def m4_compute_similar(self, temp_feat, feat):
        '''

        :param temp_feat: np.array([[1,2,...]])
        :param feat:  np.array([[1,2,...]])
        :return:
        '''
        distance = 1 - pdist(np.append(temp_feat, feat, axis=0), 'cosine')
        return distance[0]

    def m4_cutImage(self, image, box_):
        '''
        :param image:
        :param box: [lt_x, lt_y, w, h]
        :return:
        '''
        box = box_.copy()
        box[2] = box[0] + box[2]
        box[3] = box[1] + box[3]
        lt_x = max(0, int(box[0]))
        lt_y = max(0, int(box[1]))
        br_x = max(0, int(box[2]))
        br_y = max(0, int(box[3]))
        cut = image[lt_y:br_y, lt_x:br_x, :]
        return cut