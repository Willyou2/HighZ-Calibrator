import os
import sys
import bz2
from bz2 import decompress

def decomp(path):
	filename = path.split('/')[-1]
	folder = '/'.join(path.split('/')[:-1])
	if '.'.join(path.split('.')[:-1]).split('/')[-1] in os.listdir(folder):
		print("Failed: Either already decompressed or nonexistent")
		return
	#print(filename[:-4], folder)
	decompPath = path + '.decompressed'
	with open(decompPath, 'wb') as new_file, bz2.BZ2File(path, 'rb') as file:
		for data in iter(lambda: file.read(100 * 1024), b''):
			new_file.write(data)
	newPath = folder + '/' + filename[:-4]
	os.rename(decompPath, newPath)
	return newPath

#decomp('D:/Documents/Green Bank Stuff/data_70MHz/15294/1529450985/pol0.scio.bz2')
