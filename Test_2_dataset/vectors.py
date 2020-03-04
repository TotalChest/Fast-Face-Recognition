import cv2, os
import numpy as np
from PIL import Image
import glob 


def get_images(path):

	gray = Image.open(path).convert('L')
	image = np.array(gray, 'uint8')

	#cv2.imshow("", image[:,:])
	#cv2.waitKey(1000)
	
	image = image.reshape(-1)

	return image


dst = open('vectors.txt','a')
for file in glob.glob('faces/*'):

	print(file)
	dst.write(file[6:-4])

	img = get_images(file)

	for j in range(64*64):
		dst.write(',' +str(img[j]))
	dst.write('\n')

	print('+++++   ' + file)

dst.close()
