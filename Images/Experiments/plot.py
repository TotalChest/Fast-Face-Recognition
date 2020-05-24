import matplotlib.pyplot as plt 
import numpy as np 

k = np.array([1, 2, 3, 4, 5, 6])

euclid_search = np.array([0.910,0.888,0.849,0.839,0.838,0.811])
euclid_recognition = np.array([0.910,0.915,0.892,0.904,0.919,0.917])
euclid_time = np.array([0.395,0.339,0.365,0.347,0.326,0.343])
index_search = np.array([0.92,0.9012,0.8765,0.8584,0.82122,0.7895])
index_recognition = np.array([0.92,0.924,0.912,0.901,0.881,0.871])
index_time = np.array([0.00624,0.00806,0.006612,0.00687,0.00864,0.00827])
multiindex_search = np.array([0.863,0.7894,0.7731,0.7242,0.70536,0.64173])
multiindex_recognition = np.array([0.863,0.818,0.82,0.782,0.787,0.74])
multiindex_time = np.array([0.002121,0.00182,0.00211,0.00286,0.00284,0.00465])
hierachicalindex_search = np.array([0.884,0.8582,0.8355,0.7817,0.76104,0.71151])
hierarchicalindex_recognition = np.array([0.884,0.882,0.875,0.839,0.82,0.791])
hierarchicalindex_time = np.array([0.00176,0.001816,0.001826,0.001509,0.0016,0.001559])

my_xticks = ['1', '5', '10', '30', '50', '100']
plt.figure(figsize=(10, 8))
plt.xticks(k, my_xticks) 
plt.tick_params(labelsize=16)
plt.plot(k, euclid_time, 's-', color = (0.2, 0.6, 0.2), label="Euclid Serch", lw=5, ms=8)
plt.plot(k, hierarchicalindex_time, 's-', color = (0.7, 0.5, 0), label="Hierarchical Search", lw=5, ms=8)
plt.plot(k, multiindex_time, 's-', color = (0.6, 0.1, 0.1), label="Multi-Index Search", lw=5, ms=8)
plt.plot(k, index_time, 's-', color = (0.2, 0.2, 0.7), label="Index Search", lw=5, ms=8)
plt.grid() 
plt.title('Search Time', fontsize=35)
plt.xlabel('K', fontsize=20)
plt.ylabel('Accuracy', fontsize=20)
plt.legend(loc='center', prop={'size': 25}) 
plt.ylim(0,0.4)
plt.show() 