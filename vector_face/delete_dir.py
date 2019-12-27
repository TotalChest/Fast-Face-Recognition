import os
import glob
import shutil

directory = '.'
vec_txt = open('vectors.txt','r')
vectors = vec_txt.read()
image_set = set()

for line in vectors.split('\n'):
	if line.split(',')[0] != '':
		 image_set.add(int(line.split(',')[0]))

for files in os.listdir(directory):
	if files in glob.glob('n*'):
		if int(files[1:]) in image_set:
			shutil.rmtree(files)
	
