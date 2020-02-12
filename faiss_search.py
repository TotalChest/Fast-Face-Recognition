import numpy as np
d = 128                        # dimension
nb = 10000000                    # database size
nq = 10                      # nb of queries
np.random.seed(1234)             # make reproducible
xb = np.random.random((nb, d)).astype('float32')
xb[:, 0] += np.arange(nb) / 1000.
xq = np.random.random((nq, d)).astype('float32')
xq[:, 0] += np.arange(nq) / 1000.

print('START LEARNING')

import faiss                   # make faiss available
index = faiss.IndexFlatL2(d)   # build the index
print(index.is_trained)      
index.add(xb)           # add vectors to the index
print(index.ntotal)


k = 10                         # we want to see 4 nearest neighbors
D, I = index.search(xb[:5], k)     # actual search
print(I)   
print(D)                # neighbors of the 5 first queries 
