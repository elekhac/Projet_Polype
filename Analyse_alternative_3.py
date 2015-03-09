# -*- coding: utf-8 -*-
"""
Created on Mon Mar 09 17:49:28 2015

@author: Hossein
"""

import numpy as np
import cv2 as cv2
from matplotlib import pyplot as plt
from skimage import data
import matplotlib.colors as col
from skimage.morphology import disk
import math

plt.close()

def Detect_laser(image):
    hsv= col.rgb_to_hsv((image/255.0))

    laser = np.zeros(image.shape[:2])
#    target=0.29 #green
#    seuil=0.05 
    for i in range(laser.shape[0]):
        for j in range(laser.shape[1]):
            if  hsv[i,j,1]<0.25 and hsv[i,j,2]>0.85:
                laser[i,j] = 1
    open_laser = cv2.morphologyEx(laser, cv2.MORPH_OPEN, disk(2))
    return open_laser
    
    
#fonction qui recoit une image binaire et elargit la zone de 1 d'un facteur l
#de chaque cote

def tranche_image(image,l):
    image_copy = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] ==1 and j>l and j<(image.shape[1]-l):
                for f in range(j-l,j+l):
                    image_copy[i,f] =1
                if i >20 and i<230:
                    for s in range(i-20,i+20):
                        image_copy[s,j] =1
    return image_copy

#def poids_cercle(image,cercle):
#    center_x = cercle[0]
#    print center_x
#    center_y = cercle[1]
#    print center_y
#    radius = cercle[2]
#    print radius
#    ng = 0
#    for i in range(center_x-radius,center_x+radius):
#        for j in range(center_y-radius,center_y+radius):
#            ng +=image[i,j]
#    ng = float(ng) / (radius**2)
#    return ng

def poids_cercle(image,cercle):
    center_x = cercle[0]
    center_y = cercle[1]
    radius = cercle[2]
    ng = 0
    for i in range(150,450):
        for j in range(260,640):
            if ((j - center_x)**2 + (i - center_y)**2 < radius**2):
                ng +=image[i,j]
    ng = ng / (2* math.pi * radius)
    return ng
        
        

img = data.imread("images\\Nopolyp\\image0.png")

plt.subplot(3,3,1)
plt.title("img")
plt.imshow(img)
plt.colorbar()

ROI = np.zeros((470,400,3), dtype=np.uint8)

for c in range(3):
    for i in range(50,520):
        for j in range(240,640):
            ROI[i-50,j-240,c] = img[i,j,c]

plt.subplot(3,3,2)
plt.title("ROI")
plt.imshow(ROI)
plt.colorbar()

ROI_flou = cv2.medianBlur((ROI).astype('uint8'),5)

plt.subplot(3,3,3)
plt.title("ROI_flou")
plt.imshow(ROI_flou)
plt.colorbar()

Laser = Detect_laser(ROI_flou)


Zone_elargit = tranche_image(Laser,50)

gray = cv2.cvtColor(ROI_flou,cv2.COLOR_BGR2GRAY)

plt.subplot(3,3,4)
plt.title("Zone_elargit")
plt.imshow(Zone_elargit)
plt.colorbar()



ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

thresh01 = thresh.copy()

for i in range(gray.shape[0]):
    for j in range(gray.shape[1]):
        if thresh[i,j] > 200:
            thresh01[i,j] = 0
        else:
            thresh01[i,j] = 1

graynew = gray.copy()

graynew = gray*thresh01

plt.subplot(3,3,5)
plt.title("Selection Otsu")
plt.imshow(graynew)
plt.colorbar()



gray_elargit = graynew * Zone_elargit

plt.subplot(3,3,6)
plt.title("Zone_elargit")
plt.imshow(gray_elargit)
plt.colorbar()


circles = cv2.HoughCircles(gray_elargit.astype('uint8'),cv2.cv.CV_HOUGH_GRADIENT,1,20,
                            param1=40,param2=20,minRadius=10,maxRadius=120)




gray_copy = gray.copy()

if circles is not None:
    #imprime la liste des cercles candidats
    print circles[0,:,:]
    circles = np.uint16(np.around(circles))
    good_circle = None
    ng_max = 0
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(gray,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(gray,(i[0],i[1]),2,(0,0,255),3)
    for i in range(circles.shape[1]):
        ng = poids_cercle(gray_elargit,circles[0,i,:])
        #imprime le total des ng de chaque cercle pondere par taille
        print ng
        if ng > ng_max:
            ng_max = ng
            good_circle = circles[0,i,:]

plt.subplot(3,3,8)
plt.title("Hough Circle Transform")
plt.imshow(gray)
plt.colorbar()


if good_circle != None: 
    # draw the outer circle
    cv2.circle(gray_copy,(good_circle[0],good_circle[1]),good_circle[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(gray_copy,(good_circle[0],good_circle[1]),2,(0,0,255),3)
    
plt.subplot(3,3,9)
plt.title("Le bon cercle")
plt.imshow(gray_copy)
plt.colorbar()