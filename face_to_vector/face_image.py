from imutils import paths
import face_recognition
from PIL import Image
import cv2
import os
import glob 


data_dir = 'Dataset'
method = 'cnn'


k = 0

for dir in glob.glob(data_dir + '/n0*'):
	for file in glob.glob(dir+'/*'):

		image = cv2.imread(file)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb, model=method)
		top, right, bottom, left = boxes[0]

		face_image = image[top:bottom, left:right]
		cv2.imshow("", face_image[:,:])
		cv2.waitKey(100)