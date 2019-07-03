import tensorflow as tf
import numpy as np
import time, cv2, datetime, os
import classify.networks as networks
from scipy.spatial.distance import pdist
import classify.ops as my_ops

class SimilarityCompute:
    def __init__(self, sess, cfg):
        self.sess = sess
        self.cfg = cfg
        self.weight_decay = cfg.weight_decay
        self.images = tf.placeholder(dtype=tf.float32, shape=[1,self.cfg.image_size[0], self.cfg.image_size[1], 3],
                                                name='input_image')
        self.ResNet18 = networks.ResNet18(self.cfg)
        prelogits, self.embedding = self.inference(self.images)









    def test(self):
        m4_temp = cv2.imread('/home/yang/dcd.png')
        m4_img1 = cv2.imread('/home/yang/plan2.jpeg')

        m4_temp = cv2.resize(m4_temp, (self.cfg.image_size[0], self.cfg.image_size[1]))
        m4_img1 = cv2.resize(m4_img1, (self.cfg.image_size[0], self.cfg.image_size[1]))
        m4_temp_f = m4_temp.astype(np.float32) / 127.5 - 1.0
        m4_img1_f = m4_img1.astype(np.float32) / 127.5 - 1.0

        img1_np = cv2.cvtColor(m4_temp_f, cv2.COLOR_BGR2RGB)
        img2_np = cv2.cvtColor(m4_img1_f, cv2.COLOR_BGR2RGB)

        images_list = [img1_np, img2_np]
        images_np = np.array(images_list)

        images = tf.placeholder(dtype=tf.float32, shape=[2, self.cfg.image_size[0], self.cfg.image_size[1], 3],
                                                name='input_image')
        prelogits, embedding = self.inference(images)

        for i in range(10):
            starttime = time.time()
            [m4_embedding] = self.sess.run([embedding], feed_dict={images: images_np})

            # print(m4_embedding[0])
            # print(m4_embedding[1])
            print(1 - pdist(m4_embedding, 'cosine'))
            endtime = time.time()
            print(endtime - starttime)

    def m4_Similarity(self, images):

        [m4_embedding] = self.sess.run([self.embedding], feed_dict={self.images: images})
        return m4_embedding

    def inference(self, image, reuse=False):
        with tf.variable_scope('similaritycompute610', reuse=reuse) as scope:
            prelogits = self.ResNet18.build_model(image)
            embedding = tf.nn.l2_normalize(prelogits, 1, name='embedding') # 预测时l2正则化，训练时不需要
            return prelogits, embedding

    def load(self, checkpoint_dir, model_folder_name):
        import re
        print(" [*] Reading checkpoints...")
        checkpoint_dir = os.path.join(checkpoint_dir, model_folder_name)

        ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
        if ckpt and ckpt.model_checkpoint_path:
            ckpt_name = os.path.basename(ckpt.model_checkpoint_path)
            self.saver.restore(self.sess, os.path.join(checkpoint_dir, ckpt_name))
            counter = int(next(re.finditer("(\d+)(?!.*\d)", ckpt_name)).group(0))
            print(" [*] Success to read {}".format(ckpt_name))
            time.sleep(3)
            return True, counter
        else:
            print(" [*] Failed to find a checkpoint")
            time.sleep(3)
            return False, 0

    def save(self, checkpoint_dir, step, model_file_name):
        model_name = "ImageNet.model"
        checkpoint_dir = os.path.join(checkpoint_dir, model_file_name)

        # if not os.path.exists(checkpoint_dir):
        #     os.makedirs(checkpoint_dir)

        self.saver.save(self.sess, os.path.join(checkpoint_dir, model_name), global_step=step)
