'''
Поиск похожих лиц по точному евклидовому расстоянию
'''

import numpy as np
d = 256        
nb = 20000
nq = 50

def dist(xq,xb):
	c = 0
	for i in range(d):
		c+=(xq[i]-xb[i])*(xq[i]-xb[i])
	return c


f = open('vectors_128.txt')

xb = np.zeros((nb,d))
xb_ans = np.zeros(nb)
for i in range(nb):
	X = f.readline().split(',')
	xb[i,:] = X[1:]
	xb_ans[i] = X[0]

index = np.random.choice(nb, nq, replace=False)
xq = np.zeros((nq,d))
xq_ans = np.zeros(nq)
for i in range(nq):
	xq[i,:] = xb[index[i]]
	xq_ans[i] = xb_ans[index[i]]


print('SEARCHING...')
k = 10
for j in range(nq):
	print('\n', xq_ans[j])
	I = np.zeros(nb)
	for i in range(nb):
		I[i] = dist(xq[j],xb[i])
	I = np.argsort(I)
	for g in range(k):
		print(xb_ans[I[g]])
	print()
