import cv2
import numpy as np
import tensorflow as tf

from siammask.config import Config
from siammask.networks.siammask import bboxes_with_scores
from siammask.json_model_utils import load_json
from siammask.tracking import (tracking_init, preprocess, update_bounding_box,
                      _example_wh_to_size, _search_wh_to_size, _create_polygon)

# DATA_LOCATION = 'F:/project/buaa/610_new/python_610/siammask/datasets/tennis/'
# MODEL_PATH = 'F:/project/buaa/610_new\python_610/siammask/saved_model/SiamMask_DAVIS.json'

def run():

    capture = cv2.VideoCapture(0)  # 相机初始化
    ret, image = capture.read()




    cfg = Config()

    search_pl = tf.placeholder(tf.float32,
                               [1, cfg.search_size, cfg.search_size, 3])
    example_pl = tf.placeholder(tf.float32,
                                [1, cfg.exemplar_size, cfg.exemplar_size, 3])
    scores, bboxes = bboxes_with_scores(
        search_pl, example_pl, cfg.anchor.num_anchors)





    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)

    load_json(sess, vars, MODEL_PATH)

    anchors, window = tracking_init(cfg)

    # Hardcoded starting polygon for demo; top left corner as location.
    target = [310, 120, 160, 250]
    x, y, w, h = target
    target_pos = np.array([x + w / 2, y + h / 2])
    target_size = np.array([w, h])

    example_size_ = _example_wh_to_size(target_size, cfg)

    processed_example = preprocess(
        image, target_pos, example_size_, cfg.exemplar_size)

    cv2.namedWindow("SiamMask", cv2.WND_PROP_FULLSCREEN)

    for i in range(100000):
        ret, image = capture.read()
        search_size_, search_scale = _search_wh_to_size(
            target_size, cfg)

        processed_search = preprocess(
            image, target_pos, round(search_size_), cfg.search_size)

        scores_, bboxes_ = sess.run(
            [scores, bboxes],
            feed_dict={search_pl: processed_search,
                       example_pl: processed_example})

        target_pos, target_size = update_bounding_box(
            image, scores_, bboxes_, anchors, window, target_pos, target_size,
            search_scale, cfg)

        polygon = _create_polygon(target_pos, target_size)

        cv2.polylines(image, [polygon], True, (0, 255, 0), 3)
        cv2.imshow('SiamMask', image)

        key = cv2.waitKey(1)
        if key > 0:
            break


class m4_TrackingC:
    def __init__(self, MODEL_PATH):
        self.MODEL_PATH = MODEL_PATH
        self.cfg = Config()

        self.search_pl = tf.placeholder(tf.float32,
                                   [1, self.cfg.search_size, self.cfg.search_size, 3])
        self.example_pl = tf.placeholder(tf.float32,
                                    [1, self.cfg.exemplar_size, self.cfg.exemplar_size, 3])
        self.scores, self.bboxes = bboxes_with_scores(
            self.search_pl, self.example_pl, self.cfg.anchor.num_anchors) # 应该是建立网络




    def m4_TrackingInit(self, image, x, y, w, h):


        self.anchors, self.window = tracking_init(self.cfg)

        # Hardcoded starting polygon for demo; top left corner as location.
        # target = [310, 120, 160, 250]
        # x, y, w, h = target
        self.target_pos = np.array([x + w / 2, y + h / 2])
        self.target_size = np.array([w, h])

        example_size_ = _example_wh_to_size(self.target_size, self.cfg)

        self.processed_example = preprocess(
            image, self.target_pos, example_size_, self.cfg.exemplar_size)

    def m4_TrackingRun(self, image, sess):
        search_size_, search_scale = _search_wh_to_size(
            self.target_size, self.cfg)

        processed_search = preprocess(
            image, self.target_pos, round(search_size_), self.cfg.search_size)

        scores_, bboxes_ = sess.run(
            [self.scores, self.bboxes],
            feed_dict={self.search_pl: processed_search,
                       self.example_pl: self.processed_example})

        self.target_pos, self.target_size = update_bounding_box(
            image, scores_, bboxes_, self.anchors, self.window, self.target_pos, self.target_size,
            search_scale, self.cfg)

        lt_x = int(self.target_pos[0] - self.target_size[0] // 2)
        lt_y = int(self.target_pos[1] - self.target_size[1] // 2)
        br_x = int(self.target_pos[0] + self.target_size[0] // 2)
        br_y = int(self.target_pos[1] + self.target_size[1] // 2)
        return [lt_x, lt_y, br_x, br_y]

        # polygon = _create_polygon(self.target_pos, self.target_size)
        #
        # cv2.polylines(image, [polygon], True, (0, 255, 0), 3)
        # cv2.imshow('SiamMask', image)
        # cv2.waitKey(30)



if __name__ == '__main__':
    sess = tf.InteractiveSession()
    m4_Track = m4_TrackingC(MODEL_PATH)

    tf.global_variables_initializer().run()

    vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)  # 放到总图中收集变量
    track_vars = [var for var in vars if ('Layer1' in var.name or 'Layer2' in var.name or 'Layer3' in var.name
                  or 'Layer4' in var.name or 'Downsample' in var.name or 'Score' in var.name or 'BBox' in var.name)]

    load_json(sess, track_vars, MODEL_PATH)  # 载入模型  # 放到总图中载入模型


    capture = cv2.VideoCapture(0)  # 相机初始化
    ret, image = capture.read()
    m4_Track.m4_TrackingInit(image)
    while 1:
        ret, image = capture.read()
        m4_Track.m4_TrackingRun(image, sess)




