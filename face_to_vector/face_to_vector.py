import face_recognition
import cv2
import glob
import os


vectors_file = 'Vectors/vectors_'
added_file = 'Added_face.txt'
data_dir = 'Dataset'
method = 'cnn'


file_num = 1
dst = open(vectors_file + str(file_num) + '.txt','a')
added = open(added_file, 'a')
k = 0

for dir in glob.glob(data_dir + '/n0*'):
	for file in glob.glob(dir+'/*'):

		if os.path.getsize(file) > 120000:
			print('  --LARGE--  ')
			continue

		if k == 5000:
			dst.close()
			file_num += 1
			dst = open(vectors_file + str(file_num) + '.txt','a')
			k = 0

		k += 1
		print(str(file_num) + '.' + str(k) + '\t' + file)
		
		image = cv2.imread(file)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb, model=method)
		encodings = face_recognition.face_encodings(rgb, boxes)

		if boxes:
			
			dst.write(file[len(data_dir) + 1:-4])

			for i in range(128):
			    dst.write(','+"{0:.10f}".format(encodings[0][i]))

			dst.write('\n')
		else:
			print('  --NO FACE--  ')
			k -= 1

	added.write(dir.split('/')[1])
	added.write('\n')

dst.close()
added.close()
