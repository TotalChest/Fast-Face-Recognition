import numpy as np

vectors_file = 'Vectors/vectors_1.txt'
d = 128        
count = 2150
q_count = 1

def dist(xq, xb):
	c = 0
	for i in range(d):
		c += (xq[i] - xb[i]) * (xq[i] - xb[i])
	return c


f = open(vectors_file)

vectors = np.zeros((count, d))
vectors_ans = []
for i in range(count):
	X = f.readline().split(',')
	vectors[i,:] = X[1:]
	vectors_ans.append(X[0])

index = np.random.choice(count, q_count, replace=False)
q_vectors = np.zeros((q_count, d))
q_ans = []
for i in range(q_count):
	q_vectors[i,:] = vectors[index[i]]
	q_ans.append(vectors_ans[index[i]])


print('SEARCHING...')
k = 50
for j in range(q_count):
	print('\n\n')
	print(q_ans[j])
	I = np.zeros(count)
	for i in range(count):
		I[i] = dist(q_vectors[j], vectors[i])
	I = np.argsort(I)
	for g in range(k):
		if vectors_ans[I[g]][:7] == q_ans[j][:7]:
			print('   ' + vectors_ans[I[g]])
		else:
			print(vectors_ans[I[g]])
	
