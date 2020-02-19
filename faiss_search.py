import numpy as np
d = 128                        # dimension
nb = 1000000                  # database size
nq = 1                      # nb of queries
np.random.seed(1234)             # make reproducible
xb = np.random.random((nb, d)).astype('float32')
#xb[:, 0] += np.arange(nb) / 1000.
#xq = np.random.random((nq, d)).astype('float32')*100
xq = np.zeros((1,d)).astype('float32')
xq[0,127]=1
xq += xb[:1,:]
#xq[:, 0] += np.arange(nq) / 1000.

print('LEARNING...')

import faiss                   # make faiss available
index = faiss.IndexFlatL2(d)   # build the index
print(index.is_trained)      
print('ADDING...')
index.add(xb)           # add vectors to the index
print(index.ntotal)


print('SEARCHING...')
k = 10                         # we want to see 4 nearest neighbors
#D, I = index.search(xb[:1], k)
D, I = index.search(xq, k)      # actual search
print(I)   
print(D)                # neighbors of the 5 first queries 
print('VECTORS:')
print(xq[0,:])
print(xb[I[0,0],:])

