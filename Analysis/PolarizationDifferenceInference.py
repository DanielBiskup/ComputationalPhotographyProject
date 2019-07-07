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

# some helper functions (internally, images are represented as floats to avoid errors)
def LoadImage(filename):
	return mpimg.imread(filename).astype(np.float)

def SaveImage(img, filename):
	plt.imsave(filename, np.clip(img, 0, 255).astype(np.uint8))

def ShowImage(img, title='image'):
	plt.figure(title)
	assert img.dtype == np.float
	plt.imshow(np.clip(img, 0, 255).astype(np.uint8))

h = LoadImage('h.jpg')
v = LoadImage('v.jpg')

str_parralel = 'parralel polarization'
str_cross = 'cross polarization, indirect light only'
str_sum = 'parrallel + cross polarization, ordinary image'
str_direct = 'parralel - cross polarization, direct light only'

ShowImage(v, str_parralel)
ShowImage(h, str_cross)
ShowImage(h+v, str_sum)
ShowImage(v-h, str_direct)

SaveImage(v, str_parralel)
SaveImage(h, str_cross)
SaveImage(h+v, str_sum)
SaveImage(v-h, str_direct)