# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 13:30:24 2014

@author: Hossein
"""

import os
import matplotlib.pyplot as plt
from skimage import data

#Ce code crée plot avec a gauche, l'image ( qui est dans images)
#et a droite le graph de l'image lui correspondant( qui est dans graph_images) 

def Comparer_image_plot(NumImg):
    
    liste1 = os.listdir("images")
    for i in liste1:
        if str(NumImg) in i:
            ImgPolyp = i
            break
    liste2 = os.listdir("graph_images12")
    for j in liste2:
        if str(NumImg) in j:
            PlotPolyp = j
            break
    
    polDia = data.imread("images\\"+ ImgPolyp)
    
    polDia_plot = data.imread("graph_images12\\"+ PlotPolyp)
    
    plt.subplot(1,2,1)
    plt.title("Image initiale:" + ImgPolyp)
    plt.imshow(polDia)
    
    plt.subplot(1,2,2)
    plt.title("Graph image apres analyse:"+ PlotPolyp)
    plt.imshow(polDia_plot)
    plt.show()


Comparer_image_plot("image44") 
    
    