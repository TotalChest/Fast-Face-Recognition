import os
import glob  
import numpy as np  
from PIL import Image
import cv2  
import tensorflow as tf  
from fr_utils import *  
from inception_blocks_v2 import *  
from keras import backend as K

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def get_images(path):

	# Переводим изображение в черно-белый формат и приводим его к формату массива
	gray = Image.open(path).convert('L')
	image = np.array(gray, 'uint8')

	#cv2.imshow("", image[:,:])
	#cv2.waitKey(2000)

	# Определяем области где есть лица
	faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))
	# Если лицо нашлось добавляем его в список images, а соответствующий ему номер в список labels
	for (x, y, w, h) in faces:
		image = image[y: y + h, x: x + w]
		cv2.imshow("", image[:,:])
		cv2.waitKey(2000)
		return cv2.imwrite ( 'temp.jpg' , image)
           

	return cv2.imwrite ( 'temp.jpg' , image)

def img_to_encoding(image_path, model):
	print(get_images(image_path))
	cv2.waitKey(10)
	image = cv2.imread('temp.jpg', 1)
	#cv2.imshow("", image[:,:])
	#cv2.waitKey(2000)
	image = cv2.resize(image, (96, 96))
	#cv2.imshow("", image[:,:])
	#cv2.waitKey(2000)
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
	for dir in glob.glob('n0*'):
		print(dir)
		for file in glob.glob(dir+'/*'):

			try:
				img = img_to_encoding(file, FRmodel)
			except:
				continue
			print(file)
			dst.write(str(dir[2:]))

			for j in range(128):
				dst.write(','+str("{0:.10f}".format(img[0][j])))
			dst.write('\n')
	dst.close()


K.set_image_data_format('channels_first')
FRmodel = faceRecoModel(input_shape=(3, 96, 96))
FRmodel.compile(optimizer = 'adam', loss = triplet_loss, metrics = ['accuracy'])  
load_weights_from_FaceNet(FRmodel)

prepare_database()
    
