'''
Demo of Multi-Aperture Turbulence Simulation.

Nicholas Chimitt and Stanley H. Chan "Simulating anisoplanatic turbulence
by sampling intermodal and spatially correlated Zernike coefficients," Optical Engineering 59(8), Aug. 2020

ArXiv:  https://arxiv.org/abs/2004.11210

Nicholas Chimitt and Stanley Chan
Copyright 2021
Purdue University, West Lafayette, In, USA.
'''

from matplotlib import pyplot as plt
import numpy as np
import TurbSim_v1_main as util


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])


img = rgb2gray(plt.imread('./data/chart.png'))
N = 225 # size of the image -- assumed to be square (pixels)
D = 0.2 # length of aperture diameter (meters)
L = 7000 # length of propagation (meters)
r0 = 0.2 # the Fried parameter r0. The value of D/r0 is critically important! (See associated paper)
wvl = 0.525e-6 # the mean wavelength -- typically somewhere suitably in the middle of the spectrum will be sufficient
obj_size = 2.06*1 # the size of the object in the object plane (meters). Can be different the Nyquist sampling, scaling
                  # will be done automatically.

param_obj = util.p_obj(N, D, L, r0, wvl, obj_size) # generating the parameter object, some other things are computed within this
                                                   # function, see the def for details
print(param_obj['N'] * param_obj['delta0'], param_obj['smax'], param_obj['scaling'])
#print('hi')
#print(param_obj['spacing'])
#print('hi')
S = util.gen_PSD(param_obj) # finding the PSD, see the def for details
param_obj['S'] = S # appending the PSD to the parameter object for convenience

for i in range(100):
    img_tilt, _ = util.genTiltImg(img, param_obj) # generating the tilt-only image
    img_blur = util.genBlurImage(param_obj, img_tilt)
    plt.imshow(img_tilt,cmap='gray',vmin=0,vmax=1)
    plt.show()
    plt.imshow(img_blur, cmap='gray', vmin=0, vmax=1)
    plt.show()
