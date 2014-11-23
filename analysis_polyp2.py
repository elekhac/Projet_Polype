
# coding: utf-8

import skimage
import cv2
from skimage.filter import rank as rank2
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from skimage import data, exposure
from skimage.morphology import disk,watershed,closing

polDia = data.imread("images\\image36.png")

#Plot de l'image initiale

plt.subplot(3,3,1)
plt.title("Image initiale")
plt.imshow(polDia)
plt.colorbar()

#application d'un masque rectangle sur l'image
carre = np.zeros(polDia.shape[:2])
for i in range(150,400):
    for j in range(350,650):
        carre[i,j] =1
polDia = cv2.bitwise_and(polDia, polDia, mask = np.uint8(carre))

#detection du laser a l'aide du hsv

hsv= col.rgb_to_hsv((polDia/255.0))

laser = np.zeros(polDia.shape[:2])
for i in range(150,400):
    for j in range(350,650):
        if  hsv[i,j,1]<0.3 and hsv[i,j,2]>0.85:
            laser[i,j] = 1

plt.subplot(3,3,9)
plt.title("laser detecte par hsv")
plt.imshow(laser)
plt.colorbar()

# elargissement de la zone verticale par rapport au laser (seulement si on veut
# un watershed du polype entier)
zone = laser.copy()
for i in range(150,400):
    for j in range(350,650):
        if laser[i,j] ==1:
            for f in range(i-1,i+1):
                zone[f,j] = 1

# determination de l intervalle horizontal autour du laser
zone_copy = zone.copy()
for i in range(150,400):
    for j in range(350,650):
        if zone[i,j] ==1 and j>80 and j<polDia.shape[1]:
            for f in range(j-80,j+80):
                zone_copy[i,f] =1


#Transformation en image en niveau de gris

polDia_g = skimage.color.rgb2gray(polDia)

polDia_g = polDia_g * zone_copy

plt.subplot(3,3,2)
plt.title("Image en gris")
plt.imshow(polDia_g,cmap = plt.cm.gray)
plt.colorbar()


# applique un filtre median sur l'image en niveau de gris, ceci afin
#de flouter et lisser les bords

polDia_med = rank2.median((polDia_g*255).astype('uint8'),disk(8))

plt.subplot(3,3,3)
plt.title("Image apres filtre median")
plt.imshow(polDia_med,cmap = plt.cm.gray)
plt.colorbar()
type(polDia_med)


# applique une normalisation adaptive a contraste limitee de l'histogramme
# (CLAHE)
polDia_clahe = exposure.equalize_adapthist(polDia_med, clip_limit=0.02)
polDia_clahe_stretch = exposure.rescale_intensity(polDia_clahe, out_range=(0, 256))
#revient a faire polDia_clahe multiplie par 256

plt.subplot(3,3,4)
plt.title("CLAHE")
plt.imshow(polDia_clahe_stretch,cmap = plt.cm.gray)
plt.colorbar()


# applique un gradient sur l'image floutee : mise en evidence des changements
#de niveau abrupt

polDia_grad = rank2.gradient(polDia_med,disk(3))

plt.subplot(3,3,5)
plt.title("Suivi d'un filtre gradient")
plt.imshow(polDia_grad,cmap = plt.cm.gray)
plt.colorbar()
type(polDia_grad)


# Binarisation de l'image en la partie inferieur a un certain gradient
#et l'autre
polDia_grad_mark = polDia_grad<20

plt.subplot(3,3,6)
plt.title("Selection d'un grandient mini")
plt.imshow(polDia_grad_mark,cmap = plt.cm.gray)
plt.colorbar()

# Filtre gradient le plus fin qui sera utilise par le watershed comme
#base

polDia_grad_forws = rank2.gradient(polDia_clahe_stretch,disk(1))

#polDia_grad_forws = rank2.gradient(polDia_med,disk(1))
#title("Image de base pour le watershed")
#subplot(4,2,6)
#imshow(polDia_grad,cmap = plt.cm.gray)
#colorbar()


# Fermeture de l'image binarisee

polDia_grad_mark_closed = closing(polDia_grad_mark,disk(1))

plt.subplot(3,3,7)
plt.title("Fermeture de l'image binarisee")
plt.imshow(polDia_grad_mark_closed,cmap = plt.cm.gray)
plt.colorbar()


# labelisation de l'image binarise, puis watershed de l'image labelise, en 
#partant de l'image de gradient la plus fine

Labelised = (skimage.measure.label(polDia_grad_mark_closed,8,0))+1

Watersheded  = watershed(polDia_grad_forws,Labelised)

plt.subplot(3,3,8)
plt.title("Image apres watershed")
plt.imshow(Watersheded)
plt.colorbar()

