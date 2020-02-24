import cv2, os
import numpy as np
from PIL import Image


d = 256        
nb = 29030
n0 = 80

def dist(xq,xb):
	c = 0
	for i in range(d):
		c+=(xq[i]-xb[i])*(xq[i]-xb[i])
	return c


cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

def get_images(path):

    gray = Image.open(path).convert('L')
    image = np.array(gray, 'uint8')

    cv2.imshow("", image[:,:])
    cv2.waitKey(2000)

    faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

    for (x, y, w, h) in faces:
        image = image[y: y + h, x: x + w]
        image = cv2.resize(image, (n0, n0))
        cv2.imshow("", image[:,:])
        cv2.waitKey(2000)
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

U = np.zeros((n0*n0, n0*n0))
matrix_f = open('U_matrix.txt')
for i in range(n0):
    U[i,:] = matrix_f.readline().split(',')


f = open('vectors_128.txt')
xb = np.zeros((nb,d))
xb_ans = np.zeros(nb)
for i in range(nb):
	X = f.readline().split(',')
	xb[i,:] = X[1:]
	xb_ans[i] = X[0]


file = input('Path: ')
img, stasus= get_images(file)
if stasus:
	img_norm = featureNormalize(img, mu, sigma)
	q = projectData(img_norm, U, d)


print('SEARCHING...')
k = 10
I = np.zeros(nb)
for i in range(nb):
	I[i] = dist(q, xb[i])
I = np.argsort(I)
for g in range(k):
	print(xb_ans[I[g]])
print()