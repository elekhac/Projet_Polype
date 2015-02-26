# -*- coding: utf-8 -*-
"""
Created on Thu Feb 26 23:17:56 2015

@author: Hossein
"""

import numpy as np
import cv2 as cv2
import matplotlib.colors as col


def Analyse_Hough(image):
    
    # transforme en image en niveau de gris
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    # seuillage d'otsu sur l'image de base
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    # a la base thresh vaut 0 ou 256, plus maitenant (0 1) 
    thresh01 = binarise_image(thresh)
    
    # selectionne ce qu'otsu selectionne
    graynew = gray.copy()
    graynew = gray*thresh01
    
    # detecte laser + elargit autour    
    img_vert = Detect_laser(image)
    img_vert_elargi = tranche_image(img_vert,40)

    # on isole la partie qui ete selectionnee par otsu et qui est proche du laser
    graynew2 = graynew.copy()
    graynew2 = graynew*img_vert_elargi

    # applique filtre median
    graynew_flou = cv2.medianBlur((graynew2).astype('uint8'),5)

    # Applique transformee de Hough , voir doc pour les parametres
    circles = cv2.HoughCircles(graynew_flou,cv2.cv.CV_HOUGH_GRADIENT,1,20,
                            param1=50,param2=27,minRadius=5,maxRadius=150)

    # verifie qu'il y a au moins un cercle, puis les compte
    sum = 0
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            sum += 1

    return sum




# prends une image , et renvoie l'image binarisee par rapport au niveau 200

def binarise_image(image):
    image01 = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if image[i,j] > 200:
                image01[i,j] = 0
            else:
                image01[i,j] = 1
    return image01
           


def Detect_laser(image):
    hsv= col.rgb_to_hsv((image/255.0))

    laser = np.zeros(image.shape[:2])
    target=0.29 #green
    seuil=0.05 
    for i in range(laser.shape[0]):
        for j in range(laser.shape[1]):
            if abs(hsv[i,j,0] - target) < seuil and hsv[i,j,1]>0.2 and hsv[i,j,2]>0.1:
                laser[i,j] = 1
    return laser
    
    
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