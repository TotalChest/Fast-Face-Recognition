from imutils import paths
import face_recognition
import cv2
import os
import glob 


vectors_file = 'vectors_128.txt'
data_dir = 'Dataset'
method = 'cnn'


dst = open(vectors_file,'a')
k = 0

for dir in glob.glob(data_dir + '/n0*'):
	for file in glob.glob(dir+'/*'):
		k += 1;
		print(str(k) + '.\t' + file)
		name = file.split('/')[1]
		dst.write(name)

		image = cv2.imread(file)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb, model=method)
		encodings = face_recognition.face_encodings(rgb, boxes)

		for i in range(128):
		    dst.write(','+"{0:.10f}".format(encodings[0][i]))
		dst.write('\n')
dst.close()