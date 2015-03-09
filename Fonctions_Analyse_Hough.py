# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 23:17:56 2015

@author: Hossein
"""

import numpy as np
import cv2 as cv2
import matplotlib.colors as col
import matplotlib.pyplot as plt
from skimage.morphology import disk
import math


def Analyse_Hough(image):

    
    # transforme en image en niveau de gris
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
            
    #detecte laser + elargit autour    
    #laser = Detect_laser(img)
    #img_autour_laser = tranche_image(laser,70,70)
    
    #application d'un masque    
    carre = np.zeros(gray.shape)
    for i in range(150,450):
        for j in range(260,640):
            carre[i,j] =1
        
    img_carre = gray*carre
        
    # seuillage d'otsu sur l'image de base
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # a la base thresh vaut 0 ou 256, plus maitenant (0 1) 
    thresh01 = thresh > 200
    
    # selectionne ce qu'otsu selectionne
    graynew = gray.copy()
    graynew = img_carre*thresh01

    # applique filtre median
    graynew_flou = cv2.medianBlur((graynew).astype('uint8'),5)
    plt.imshow(graynew_flou)

    # Applique transformee de Hough , voir doc pour les parametres
    circles = cv2.HoughCircles(graynew_flou,cv2.cv.CV_HOUGH_GRADIENT,1,20,
                            param1=40,param2=20,minRadius=10,maxRadius=120)
    
    #imprime la liste des cercles candidats
    print circles
                            
    #affiche les cercles
    if circles != None:
        circles = np.uint16(np.around(circles))
        good_circle = circles[0,:,:]
        ng_max = 0
        for i in circles[0,:,:]:
        # draw the outer circle
            cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
            cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
        for i in range(circles.shape[1]):
            ng = poids_cercle(gray,circles[0,i,:])
            #imprime le total des ng de chaque cercle pondere par taille
            print ng
            if ng > ng_max:
                ng_max = ng
                good_circle = circles[0,i,:]
            
    cv2.imshow('detected circles',image)
    
    return good_circle



# detecte le laser en fonction de sa saturation et brillance 
def Detect_laser(image):
    hsv= col.rgb_to_hsv((image/255.0))
    laser = np.zeros(image.shape[:2])
    for i in range(150,450):
        for j in range(260,640):
            if  hsv[i,j,1]<0.25 and hsv[i,j,2]>0.85:
                laser[i,j] = 1
    return laser
    
def tranche_image(image,l1,l2):
#    open_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, disk(5))
    image_copy = image.copy()
    for i in range(150,450):
        for j in range(260,640):
            if image[i,j] ==1:
                for k in range(i-l1,i+l1):
                    image_copy[k,j] = 1
            if image_copy[i,j] ==1:
                for f in range(j-l2,j+l2):
                    image_copy[i,f] =1
    return image_copy

# calcul le niveau de gris pondere de la taille d'un cercle
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
        
    


img = cv2.imread('images//image13.png')
print Analyse_Hough(img)
