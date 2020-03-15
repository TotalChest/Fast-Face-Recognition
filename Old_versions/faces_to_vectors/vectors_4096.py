import cv2, os
import numpy as np
from PIL import Image
import glob 

# Для детектирования лиц используем каскады Хаара
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def get_images(path):

    gray = Image.open(path).convert('L')
    image = np.array(gray, 'uint8')

    #cv2.imshow("", image[:,:])
    #cv2.waitKey(30)

    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    for (x, y, w, h) in faces:
        image = image[y: y + h, x: x + w]
        image = cv2.resize(image, (n0, n0))
        #cv2.imshow("", image[:,:])
        #cv2.waitKey(30)
        image = image.reshape(-1)
        return image, 1
    return None, 0

n0 = 80

dst = open('vectors_4096.txt','a')
for dir in glob.glob('n0*'):
    for file in glob.glob(dir+'/*'):
        img, stasus= get_images(file)
        if stasus:
            print(file)
            for j in range(n0*n0):
                dst.write((',' if j!=0 else '')+str(img[j]))
            dst.write('\n')
dst.close()