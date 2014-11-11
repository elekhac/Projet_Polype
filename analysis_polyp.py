
# coding: utf-8

import skimage
from skimage.filter import rank as rank2
import matplotlib.pyplot as plt
import numpy as np
from skimage import data
from skimage.morphology import disk
from skimage.morphology import watershed




polDia = data.imread("vu_diametre_polyp01.png")

#Plot de l'image initiale

plt.subplot(3,2,1)
plt.title("Image initiale")
plt.imshow(polDia)
plt.colorbar()

#Transformation en image en niveau de gris

polDia_g = skimage.color.rgb2gray(polDia)

plt.subplot(3,2,2)
plt.title("Image en gris")
plt.imshow(polDia_g,cmap = plt.cm.gray)
plt.colorbar()


# applique un filtre median sur l'image en niveau de gris, ceci afin
#de flouter et lisser les bords

polDia_med = rank2.median((polDia_g*255).astype('uint8'),disk(5))

plt.subplot(3,2,3)
plt.title("Image apres filtre median")
plt.imshow(polDia_med,cmap = plt.cm.gray)
plt.colorbar()
type(polDia_med)


# applique un gradient sur l'image floutee : mise en evidence des changements
#de niveau abrupt

polDia_grad = rank2.gradient(polDia_med,disk(3))

plt.subplot(3,2,4)
plt.title("Suivi d'un filtre gradient")
plt.imshow(polDia_grad,cmap = plt.cm.gray)
plt.colorbar()
type(polDia_grad)


# Binarisation de l'image en la partie inferieur a un certain gradient
#et l'autre

plt.subplot(3,2,5)
plt.title("Selection d'un grandient mini")
plt.imshow(polDia_grad<10,cmap = plt.cm.gray)
plt.colorbar()


# Filtre gradient le plus fin qui sera utilise par le watershed comme
#base

polDia_grad_forws = rank2.gradient(polDia_med,disk(1))
#title("Image de base pour le watershed")
#subplot(4,2,6)
#imshow(polDia_grad,cmap = plt.cm.gray)
#colorbar()


# labelisation de l'image binarise, puis watershed de l'image labelise, en 
#partant de l'image de gradient la plus fine

polDia_grad_mark = polDia_grad<10

Labelised = (skimage.measure.label(polDia_grad_mark,8,0))+1

Watersheded  = watershed(polDia_grad_forws,Labelised)

plt.subplot(3,2,6)
plt.title("Image apres watershed")
plt.imshow(Watersheded)
plt.colorbar()

