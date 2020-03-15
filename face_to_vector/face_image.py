import face_recognition
import cv2
import glob 


data_dir = 'Dataset'
method = 'cnn'


k = 0

for dir in glob.glob(data_dir + '/n0*'):
	for file in glob.glob(dir+'/*'):
		print(file)
		image = cv2.imread(file)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb, model=method)

		if boxes:
			top, right, bottom, left = boxes[0]
			face_image = image[top:bottom, left:right]
			cv2.imshow("", face_image[:,:])
			cv2.waitKey(100)
		else:
			print('  --NO FACE--  ')
