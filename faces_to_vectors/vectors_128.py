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
    #cv2.waitKey(1000)

    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    for (x, y, w, h) in faces:
        image = image[y: y + h, x: x + w]
        image = cv2.resize(image, (n0, n0))
        #cv2.imshow("", image[:,:])
        #cv2.waitKey(1000)
        image = image.reshape(-1)
        return image, 1
    return None, 0


def featureNormalize(X, mu, sigma):
    X_norm = X - mu
    X_norm /= sigma
    return X_norm


def projectData(X, U, K):
    Z = np.zeros((X.shape[0], K))
    Z = np.dot(X,  U[:, :K])
    return Z


mu = np.array(list(map(float, open('U_mu.txt').readline().split(','))))
sigma = np.array(list(map(float, open('U_sigma.txt').readline().split(','))))

K = 256
n0 = 80

U = np.zeros((n0*n0, n0*n0))
matrix_f = open('U_matrix.txt')
for i in range(n0):
    U[i,:] = matrix_f.readline().split(',')


dst = open('vectors_128.txt','a')
for dir in glob.glob('n0*'):
    for file in glob.glob(dir+'/*'):
        img, stasus= get_images(file)
        if stasus:
            print(file)
            dst.write(str(int(dir[1:])))
            img_norm = featureNormalize(img, mu, sigma)
            Z = projectData(img_norm, U, K)
            for j in range(K):
                dst.write(','+str(img[j]))
            dst.write('\n')
dst.close()