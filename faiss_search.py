'''
Поиск похожих лиц с помощью Faiss по точному евклидовому расстоянию
'''

import numpy as np
d = 128              
nb = 100000                
nq = 1                        


f = open('vectors.txt')

xb = np.zeros((nb,d)).astype('float32')
xb_ans = np.zeros(nb)
for i in range(nb):
	X = f.readline().split(',')
	xb[i,:] = list(map(float,X[1:]))
	xb_ans[i] = X[0]

xq = np.zeros((nq,d)).astype('float32')
xq_ans = np.zeros(nq)
for i in range(nq):
	#X = f.readline().split(',')
	xq[i,:] = list(map(float,X[1:]))
	xq_ans[i] = X[0]


print('LEARNING...')
import faiss             
index = faiss.IndexFlatL2(d) 
print(index.is_trained) 

print(xb.shape)
print('ADDING...')
index.add(xb)     
print(index.ntotal)


print('SEARCHING...')
k = 12                 
D, I = index.search(xq, k)
print(I)   
print(D)

print('VECTORS:')
for i in range(nq):
	for j in range(k):
		print(xq_ans[i], ':', xb_ans[I[i,j]], end='   ')
	print()

