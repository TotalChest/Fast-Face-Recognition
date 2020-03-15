import numpy as np
m = 29030
n0 = 80
n =  n0*n0


def featureNormalize(X):
    mu = np.mean(X, axis=0)
    X_norm = X - mu
    sigma = np.std(X_norm, axis=0, ddof=1)
    X_norm /= sigma
    return X_norm, mu, sigma


def pca(X):
    m, n = X.shape
    U = np.zeros(n)
    S = np.zeros(n)
    Cov = (1/m) * np.dot(X.T,X)
    U, S, V = np.linalg.svd(Cov)
    return U, S
 

src = open('vectors_4096.txt')
X = np.zeros((m,n))
for i in range(m):
	X[i,:] = src.readline().split(',')

mu_f = open('U_mu.txt', 'w')
sigma_f = open('U_sigma.txt', 'w')
print('Normalize...')
X_norm, mu, sigma = featureNormalize(X)
for j in range(n):
	mu_f.write(str(mu[j])+('' if j==(n-1) else ','))
for j in range(n):
	sigma_f.write(str(sigma[j])+('' if j==(n-1) else ','))



print('PCA...')
U, S = pca(X_norm)
dst = open('U_matrix.txt', 'w')
for i in range(n):
	for j in range(n):
		dst.write(str(U[i,j])+('' if j==(n-1) else ','))
	dst.write('\n')
