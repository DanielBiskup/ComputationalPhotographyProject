#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 18:51:48 2019

@author: Daniel Biskup
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.sparse
import scipy.sparse.linalg
import os
import glob

# Copy soure image directory
os.system("cp -rf CapturedData TrainingData")

# print your current working directory
start_dir = os.getcwd()

# Change to the output directory
os.chdir('TrainingData') #this will change directory to pwd path.

# Generate list of all datasets to work on:
dataset_dirs = [ os.path.join( os.getcwd(), dataset ) for dataset in os.listdir() ]

# Some helper functions (internally, images are represented as floats to avoid errors)
def LoadImage(filename):
	return mpimg.imread(filename).astype(np.float)

def SaveImage(img, filename):
	plt.imsave(filename, np.clip(img, 0, 255).astype(np.uint8))

def ShowImage(img, title='image'):
	plt.figure(title)
	assert img.dtype == np.float
	plt.imshow(np.clip(img, 0, 255).astype(np.uint8))

str_parallel = 'parallel'
str_crossed = 'crossed'
str_sum = 'sum'
str_direct = 'direct'
str_spacer = '-'

for directory in dataset_dirs:
	os.chdir(directory)
	filenames_parallel = glob.glob('*' + str_parallel + '*')
	filenames_crossed  = glob.glob('*' + str_crossed  + '*')
	filenames_parallel.sort()
	filenames_crossed.sort()
	for i in range(len(filenames_crossed)):
	#for i in range(5):
		img_crossed  = LoadImage(filenames_crossed[i])
		img_parallel = LoadImage(filenames_parallel[i])
		out_name_sum    = "{:02}".format(i) + str_spacer + str_sum    + '.jpg'
		out_name_direct = "{:02}".format(i) + str_spacer + str_direct + '.jpg'
		img_sum = img_crossed+img_parallel
		img_direct = img_parallel-img_crossed
		
		# Apply some scaling to make result better visible. This might have to
		# be removed or changed if you want to produce data sets for
		# deep learning.
		scaled_img_sum = ( img_sum / np.max(img_sum) ) * 255.0
		scaled_img_direct = img_direct * 10.0
		
		SaveImage(scaled_img_sum, out_name_sum)
		SaveImage(scaled_img_direct, out_name_direct)
		
		'''
		ShowImage(img_parallel, str_parallel)
		ShowImage(img_crossed, str_crossed)
		ShowImage(scaled_img_sum, str_sum)
		ShowImage(scaled_img_direct, str_direct)
		'''

# Back to start CWD:
os.chdir(start_dir)