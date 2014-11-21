# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 14:25:00 2014

"""

import skimage
import cv2
from skimage.filter import rank as rank2
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from skimage import exposure
from skimage.morphology import disk,watershed,closing

# Applique un watershed (et tout le tralala) sur une image, et renvoie
# le nombre d occurence tel que defini par la fct coocurence_liste

def Image_ws(image):
    
    image_mask = Rect_mask(image)
    
    laser = Detect_laser(image_mask)
    
    image_g = skimage.color.rgb2gray(image)
    
    image_med = rank2.median((image_g*255).astype('uint8'),disk(8))
    
    image_clahe = exposure.equalize_adapthist(image_med, clip_limit=0.03)
    image_clahe_stretch = exposure.rescale_intensity(image_clahe, out_range=(0, 256))

    image_grad = rank2.gradient(image_clahe_stretch,disk(3))
    
    image_grad_mark = image_grad<20
    image_grad_forws = rank2.gradient(image_clahe_stretch,disk(1))
    
    image_grad_mark_closed = closing(image_grad_mark,disk(1))
    
    Labelised = (skimage.measure.label(image_grad_mark_closed,8,0))+1
    Watersheded  = watershed(image_grad_forws,Labelised)
    
    cooc = coocurence_liste(Watersheded,laser,5)
    
    x,y = compte_occurences(cooc)
    
    return x,y
    
# Applique un watershed (et tout le tralala) sur une tranche bien choisie de l 
#image, et renvoie le nombre d occurence tel que defini par la fct 
#coocurence_liste

def Image_ws_tranche(image):
    
    image_mask = Rect_mask(image)
    
    laser = Detect_laser(image_mask)
    image_elarg = elarg_image(laser,0)
    laser_tranche = tranche_image(image_elarg,60)
    
    image_g = skimage.color.rgb2gray(image)
    image_g = image_g * laser_tranche
    
    image_med = rank2.median((image_g*255).astype('uint8'),disk(8))
    
    image_clahe = exposure.equalize_adapthist(image_med, clip_limit=0.02)
    image_clahe_stretch = exposure.rescale_intensity(image_clahe, out_range=(0, 256))

    image_grad = rank2.gradient(image_med,disk(3))
    
    image_grad_mark = image_grad<20
    image_grad_forws = rank2.gradient(image_clahe_stretch,disk(1))
    
    image_grad_mark_closed = closing(image_grad_mark,disk(1))
    
    Labelised = (skimage.measure.label(image_grad_mark_closed,8,0))+1
    Watersheded  = watershed(image_grad_forws,Labelised)
    
    cooc = coocurence_liste(Watersheded,laser,5)
    
    x,y = compte_occurences(cooc)
    
    return x,y
    


#fonction qui applique un masque rectangulaire sur une image en couleur
def Rect_mask(image):
    masque = np.zeros(image.shape[:2])
    for i in range(150,400):
        for j in range(350,650):
            masque[i,j] =1
    image = cv2.bitwise_and(image, image, mask = np.uint8(masque))
    return image

#fonction qui recoit une image avec niveau de gris 0-256, et renvoie 
#une image binarise, avec 1 a l'endroit de la couleur verte

def Detect_laser(image):
    hsv= col.rgb_to_hsv((image/255.0))

    laser = np.zeros(image.shape[:2])
    for i in range(150,400):
        for j in range(350,650):
            if  hsv[i,j,1]<0.3 and hsv[i,j,2]>0.85:
                laser[i,j] = 1
    return laser

#fonction qui recoit une image binaire et elargit la zone de 1 d'un facteur l
#de chaque cote (vertical)

def elarg_image(image,l):
    image_copy = image.copy()
    for i in range(150,400):
        for j in range(350,650):
            if image[i,j] ==1:
                for f in range(i-l,i+l):
                    image_copy[f,j] = 1
    return image_copy
    
    
#fonction qui recoit une image binaire et elargit la zone de 1 d'un facteur l
#de chaque cote (horizontal)

def tranche_image(image,l):
    image_copy = image.copy()
    for i in range(150,400):
        for j in range(350,650):
            if image[i,j] ==1 and j>l and j<(image.shape[1]-l):
                for f in range(j-l,j+l):
                    image_copy[i,f] =1
    return image_copy

#fonction qui recoit une image, un model binarise (qui contient les 
# coordonnees a suivre) et un parametre s qui represente l'eloignement
# des points dont on fait la difference et renvoie une liste des differences de
#niveau de gris.

def coocurence_liste(img,model,s):
    liste=[]
    for i in range(150,400):
        for j in range(350,650):
            if model[i,j]==1:
                liste.append(abs(img[i,j+s]*1.0-img[i,j]*1.0))
                liste.append(abs(img[i,j-s]*1.0-img[i,j]*1.0))
    return liste
 
# fonction qui recoit une liste contenant des occurences et renvoie les valeurs
 #dans une premiere liste, et les occurences de ces valeurs dans une deuxieme
 #liste
   
def compte_occurences(liste_occu):
    liste2=[]
    liste3= np.zeros(50)
    for elem in liste_occu:
        if elem not in liste2 and elem !=0:
            liste2.append(elem)
            liste3[liste2.index(elem)] +=1
        elif elem !=0 :
            liste3[liste2.index(elem)] +=1
    return liste2,liste3