# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 00:59:57 2015

@author: Elise
"""
import csv
import numpy as np
import cv2 as cv2
import matplotlib.pyplot as plt
from skimage import data
from skimage.morphology import disk, skeletonize
from skimage.measure import label,regionprops

import Detecte_laser


def label_image(image):
    
    ROI = np.zeros((470,400,3), dtype=np.uint8)
    for c in range(3):
        for i in range(50,520):
            for j in range(240,640):
                ROI[i-50,j-240,c] = image[i,j,c]

    
    gray_ROI = cv2.cvtColor(ROI,cv2.COLOR_BGR2GRAY)
    
    ROI_flou = cv2.medianBlur((ROI).astype('uint8'),3)
    
    Laser = Detecte_laser.Detect_laser(ROI_flou)
    
    open_laser = cv2.morphologyEx(Laser, cv2.MORPH_DILATE, disk(3))
    
    skel = skeletonize(open_laser > 0)
    
    tranche = Detecte_laser.tranche(skel,90,30)    
    
    ret, thresh = cv2.threshold(gray_ROI*tranche.astype('uint8'),0,1,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh01 = thresh<1.0
    
    open_thresh = cv2.morphologyEx(thresh01.astype('uint8'), cv2.MORPH_OPEN, disk(10))
    
    labelised = (label(open_thresh,8,0))+1
    
    return gray_ROI,labelised
    
    
name = "image9"
image = data.imread("image_data\\%s.png" %name)
intensity_img,labelised_img = label_image(image)
#coord d'un point du polype, a determiner manuellement
#x=235
#y=240
#intensity_img_cop = intensity_img.copy()
#intensity_img_cop[x,y] = 0
#
#figure()
#plt.imshow(intensity_img_cop)

#trouve le label du polype
polyp_label = labelised_img[x,y]
props = regionprops(labelised_img,intensity_image=intensity_img, cache=True)

list_props = []
for region in props:
    #ajoute les propritetes du polype grace a son label trouve avant
    if region.label == polyp_label:
        polyp_props = []
        polyp_props.append(name)
        polyp_props.append(region.centroid)
        polyp_props.append(region.area)
        polyp_props.append(region.eccentricity)
        polyp_props.append(region.max_intensity)
        polyp_props.append(region.mean_intensity)
        polyp_props.append(region.orientation)
        polyp_props.append(region.perimeter)
        polyp_props.append(region.perimeter/region.area)
        list_props.append(polyp_props)

# ecrire "wb" pour ecraser fichier output.csv, "a" pour ajouter ecrire
#dans la suite du fichier
with open("output_9premiers.csv", "a") as f:
    writer = csv.writer(f)
    writer.writerows(list_props)