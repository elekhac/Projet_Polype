
# coding: utf-8

import skimage
from skimage.filter import rank as rank2
import matplotlib.pyplot as plt
import matplotlib.colors as col
import numpy as np
from skimage import data, exposure
from skimage.morphology import disk,watershed,closing

polDia = data.imread("vu_diametre_polyp01.png")

#Plot de l'image initiale

plt.subplot(3,3,1)
plt.title("Image initiale")
plt.imshow(polDia)
plt.colorbar()

#detection du laser a l'aide du hsv

hsv= col.rgb_to_hsv((polDia/255.0))

laser = np.zeros(polDia.shape[:2])
target=0.29 #green
seuil=0.05 
for i in range(laser.shape[0]):
    for j in range(laser.shape[1]):
        if abs(hsv[i,j,0] - target) < seuil and hsv[i,j,1]>0.2 and hsv[i,j,2]>0.1:
            laser[i,j] = 1

plt.subplot(3,3,9)
plt.title("laser detecte par hsv")
plt.imshow(laser)
plt.colorbar()


# determination de l intervalle autour du laser

laser_copy = laser.copy()
for i in range(252):
    for j in range(315):
        if laser[i,j] ==1 and j>60 and j<255:
            for f in range(j-60,j+60):
                laser_copy[i,f] =1



#Transformation en image en niveau de gris

polDia_g = skimage.color.rgb2gray(polDia)

polDia_g = polDia_g * laser_copy

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
polDia_clahe = exposure.equalize_adapthist(polDia_med, clip_limit=0.03)
polDia_clahe_stretch = exposure.rescale_intensity(polDia_clahe, out_range=(0, 256))
#revient a faire polDia_clahe multiplie par 256

plt.subplot(3,3,4)
plt.title("CLAHE")
plt.imshow(polDia_clahe_stretch,cmap = plt.cm.gray)
plt.colorbar()


# applique un gradient sur l'image floutee : mise en evidence des changements
#de niveau abrupt

polDia_grad = rank2.gradient(polDia_clahe_stretch,disk(3))

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

