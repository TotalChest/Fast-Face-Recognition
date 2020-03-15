'''
Поиск похожих лиц по точному евклидовому расстоянию
'''

import numpy as np
d = 64*64       
nb = 13233
nq = 10

def dist(xq,xb):
	c = 0
	for i in range(d):
		c+=(xq[i]-xb[i])*(xq[i]-xb[i])
	return c


f = open('vectors.txt')

xb = np.zeros((nb,d))
xb_ans = []
for i in range(nb):
	X = f.readline().split(',')
	xb[i,:] = X[1:]
	xb_ans.append(X[0])

index = np.random.choice(nb, nq, replace=False)
xq = np.zeros((nq,d))
xq_ans = []
for i in range(nq):
	xq[i,:] = xb[index[i]]
	xq_ans.append(xb_ans[index[i]])


print('SEARCHING...')
k = 100
for j in range(nq):
	print('\n', xq_ans[j])
	I = np.zeros(nb)
	for i in range(nb):
		I[i] = dist(xq[j],xb[i])
	I_new = np.argsort(I)
	for g in range(k):
		print(('   ' if xq_ans[j][:-5] == xb_ans[I_new[g]][:-5] else '') + str(g) + '. ' + str(xb_ans[I_new[g]]) + '\t\t' + str(I[I_new[g]]))
	print()
