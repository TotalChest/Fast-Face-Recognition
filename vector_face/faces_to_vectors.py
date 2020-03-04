import os
import glob  
import numpy as np  
import cv2  
import tensorflow as tf  
from fr_utils import *  
from inception_blocks_v2 import *  
from keras import backend as K
    

def img_to_encoding(image_path, model):
	image = cv2.imread(image_path, 1)
	image = cv2.resize(image, (96, 96))
	img = image[...,::-1]
	img = np.around(np.transpose(img, (2,0,1))/255.0, decimals=12)
	x_train = np.array([img])
	embedding = model.predict_on_batch(x_train)
	return embedding


def triplet_loss(y_true, y_pred, alpha = 0.3):
	anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
	pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,positive)), axis=-1)
	neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,negative)), axis=-1)
	basic_loss = tf.add(tf.subtract(pos_dist, neg_dist), alpha)
	loss = tf.reduce_sum(tf.maximum(basic_loss, 0.0))
	return loss


def prepare_database():
	dst = open('vectors.txt','a')
	count = 0
	for dir in glob.glob('n0*'):
		print('\t', dir)
		for file in glob.glob(dir+'/*'):
			print(file)
			dst.write(str(int(dir[1:])))
			vector = img_to_encoding(file, FRmodel)
			for j in range(128):
				dst.write(','+str("{0:.10f}".format(vector[0][j])))
			dst.write('\n')
	dst.close()


K.set_image_data_format('channels_first')
FRmodel = faceRecoModel(input_shape=(3, 96, 96))
FRmodel.compile(optimizer = 'adam', loss = triplet_loss, metrics = ['accuracy'])  
load_weights_from_FaceNet(FRmodel)
prepare_database()
    
