# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 14:25:00 2014

"""

import skimage
from skimage.filter import rank as rank2
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from skimage import exposure
from skimage.morphology import disk,watershed,closing

# Applique un watershed (et tout le tralala) sur une image, et renvoie
# le nombre d occurence tel que defini par la fct coocurence_liste

def Image_ws(image):
    
    laser = Detect_laser(image)
    
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
    
    cooc = coocurence_liste(Watersheded,laser,3)
    
    x,y = compte_occurences(cooc)
    
    return x,y
    
# Applique un watershed (et tout le tralala) sur une tranche bien choisie de l 
#image, et renvoie le nombre d occurence tel que defini par la fct 
#coocurence_liste

def Image_ws_tranche(image):
    
    laser = Detect_laser(image)
    laser_tranche = tranche_image(laser,60)
    
    image_g = skimage.color.rgb2gray(image)
    image_g = image_g * laser_tranche
    
    image_med = rank2.median((image_g*255).astype('uint8'),disk(8))
    
    image_clahe = exposure.equalize_adapthist(image_med, clip_limit=0.03)
    image_clahe_stretch = exposure.rescale_intensity(image_clahe, out_range=(0, 256))

    image_grad = rank2.gradient(image_clahe_stretch,disk(3))
    
    image_grad_mark = image_grad<20
    image_grad_forws = rank2.gradient(image_clahe_stretch,disk(1))
    
    image_grad_mark_closed = closing(image_grad_mark,disk(1))
    
    Labelised = (skimage.measure.label(image_grad_mark_closed,8,0))+1
    Watersheded  = watershed(image_grad_forws,Labelised)
    
    cooc = coocurence_liste(Watersheded,laser,3)
    
    x,y = compte_occurences(cooc)
    
    return x,y
    


    
    

#fonction qui recoit une image avec niveau de gris 0-256, et renvoie 
#une image binarise, avec 1 a l'endroit de la couleur verte

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
    return image_copy

#fonction qui recoit une image, un model binarise (qui contient les 
# coordonnees a suivre) et un parametre s qui represente l'eloignement
# des points dont on fait la difference et renvoie une liste des differences de
#niveau de gris.

def coocurence_liste(img,model,s):
    liste=[]
    for i in range(img.shape[1]):
        for j in range(img.shape[0]):
            if model[j,i]==1:
                liste.append(abs(img[j,i+s]-img[j,i]))
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