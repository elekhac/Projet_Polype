# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 15:40:04 2014

"""
from skimage import data
import matplotlib.pyplot as plt
import Fonctions_Analyse

polDia = data.imread("vu_diametre_polyp01.png")

x1,y1 = Fonctions_Analyse.Image_ws(polDia)

x2,y2 = Fonctions_Analyse.Image_ws_tranche(polDia)

p1=plt.plot(x1,y1[:len(x1)],'o')
p2=plt.plot(x2,y2[:len(x2)],'x')
plt.title("Difference entre image complete et image tranche")
plt.show()

