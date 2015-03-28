# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 14:54:16 2015

@author: Elise
"""

""" 
ensemble des traitements appliques sur l image avant la labelisationde l'image
et l extraction des proprietes
"""

import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt
from skimage import data
from skimage.morphology import disk, skeletonize
from skimage.measure import label

import Detecte_laser


def label_image(image):
    
    ROI = np.zeros((470,400,3), dtype=np.uint8)
    for c in range(3):
        for i in range(50,520):
            for j in range(240,640):
                ROI[i-50,j-240,c] = image[i,j,c]

    # ROI en gris utilise pour Otsu
    gray_ROI = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY)
    
    # ROI flou puis converti en gris pour avoir la tranche autour du laser    
    ROI_flou = cv2.medianBlur((ROI).astype('uint8'),3)
    plt.subplot(3,3,1)
    plt.title("ROI flou")
    plt.imshow(ROI_flou)
    plt.colorbar()
    
    gray_ROI_flou = cv2.medianBlur((gray_ROI).astype('uint8'),3)
    
    Laser = Detecte_laser.Detect_laser(ROI_flou)
    plt.subplot(3,3,2)
    plt.title("laser")
    plt.imshow(Laser)
    plt.colorbar()
    
    open_laser = cv2.morphologyEx(Laser, cv2.MORPH_DILATE, disk(3))
    plt.subplot(3,3,3)
    plt.title("open laser")
    plt.imshow(open_laser)
    plt.colorbar()
    
    skel = skeletonize(open_laser > 0)
    plt.subplot(3,3,4)
    plt.title("Squelette")
    plt.imshow(skel)
    plt.colorbar()
    
    tranche = Detecte_laser.tranche(skel,90,30)
    plt.subplot(3,3,5)
    plt.title("tranche on open laser")
    plt.imshow(tranche)
    plt.colorbar()
    
    ret, thresh = cv2.threshold(gray_ROI*tranche.astype('uint8'),0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh01 = thresh.copy()
    for i in range(gray_ROI_flou.shape[0]):
        for j in range(gray_ROI_flou.shape[1]):
            if thresh[i,j] > 200:
                thresh01[i,j] = 0
            else:
                thresh01[i,j] = 1
    plt.subplot(3,3,6)
    plt.title("Otsu")
    plt.imshow(thresh01)
    plt.colorbar()
    
    #ouverture de l'image binaire obtenue apres Otsu, permet de separer 
    #le laser et polype lorsqu'ils sont colles (sous segmentation)
    open_thresh = cv2.morphologyEx(thresh01, cv2.MORPH_OPEN, disk(10))
    plt.subplot(3,3,7)
    plt.title("open_Otsu")
    plt.imshow(open_thresh)
    plt.colorbar()
    
    
    labelised = (label(open_thresh,8,0))+1
    plt.subplot(3,3,8)
    plt.title("label")
    plt.imshow(labelised)
    plt.colorbar()
    
    image_tranche_finale = open_thresh*gray_ROI_flou
    plt.subplot(3,3,9)
    plt.title("image tranchee finale")
    plt.imshow(image_tranche_finale)
    plt.colorbar()
    
    return gray_ROI,labelised

image = data.imread("image_data\\image1_2 (9).png")
intensity_img,labelised_img = label_image(image)