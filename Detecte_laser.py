# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 10:55:18 2015

@author: Hossein
"""

import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
from skimage import data
import matplotlib.colors as col
from skimage.morphology import disk
from skimage import morphology


# Avec ça on trouve tout le laser

def Detect_laser(image):
    hsv= col.rgb_to_hsv((image/255.0))

    laser = np.zeros(image.shape[:2])
    for i in range(laser.shape[0]):
        for j in range(laser.shape[1]):
            if hsv[i,j,0] < 0.5 and hsv[i,j,2]> 0.6:
                laser[i,j] = 1
    open_laser = laser
    return open_laser



#def Detect_laser(image):
#    hsv= col.rgb_to_hsv((image/255.0))
#
#    laser = np.zeros(image.shape[:2])
#    for i in range(laser.shape[0]):
#        for j in range(laser.shape[1]):
#            if  hsv[i,j,1]<0.25 and hsv[i,j,2]>0.85:
#                laser[i,j] = 1
#    open_laser = laser
#    return open_laser

    
def tranche(image,l,largeur):
    image_copy = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] == 1:
                for s in range(-l,l):
                    if (j-s)> 0 and (j+s)<400:
                        image_copy[i,j+s] = 1
                    for t in range(-largeur,largeur):
                        if (i-t)> 0 and (i+t)<470 and (j-s)> 0 and (j+s)<400:
                            image_copy[i+t,j+s] = 1
    return image_copy
            

#img = data.imread("image_data\\image0 (1).png")
#
#plt.subplot(3,3,1)
#plt.title("img")
#plt.imshow(img)
#plt.colorbar()
#
#ROI = np.zeros((470,400,3), dtype=np.uint8)
#
#for c in range(3):
#    for i in range(50,520):
#        for j in range(240,640):
#            ROI[i-50,j-240,c] = img[i,j,c]
#
#plt.subplot(3,3,2)
#plt.title("ROI")
#plt.imshow(ROI)
#plt.colorbar()
#
#ROI_flou = cv2.GaussianBlur((ROI).astype('uint8'),(9,9),0)
#
#plt.subplot(3,3,3)
#plt.title("ROI_flou")
#plt.imshow(ROI_flou)
#plt.colorbar()
#
#Laser = Detect_laser(ROI_flou)
#
#
#
#plt.subplot(3,3,4)
#plt.title("laser")
#plt.imshow(Laser)
#plt.colorbar()
#
#open_laser = cv2.morphologyEx(Laser, cv2.MORPH_DILATE, disk(2))
#
#plt.subplot(3,3,5)
#plt.title("open laser")
#plt.imshow(open_laser)
#plt.colorbar()

#skel_laser = morphology.skeletonize(Laser > 0)
#
#plt.subplot(3,3,6)
#plt.title("skeleton laser")
#plt.imshow(skel_laser)
#plt.colorbar()
#
#
#tranche1 = tranche(skel_laser,50,30)
#
#plt.subplot(3,3,7)
#plt.title("tranche on skeleton laser")
#plt.imshow(tranche1)
#plt.colorbar()


#tranche2 = tranche(open_laser,70,30)
#
#plt.subplot(3,3,8)
#plt.title("tranche on open laser")
#plt.imshow(tranche2)
#plt.colorbar()
