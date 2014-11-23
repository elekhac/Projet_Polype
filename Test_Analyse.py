# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 15:40:04 2014

"""
from skimage import data
import matplotlib.pyplot as plt
import Fonctions_Analyse2



polDia = data.imread("images\\image311.png")

x1,y1 = Fonctions_Analyse2.Image_ws(polDia)

x2,y2 = Fonctions_Analyse2.Image_ws_tranche(polDia)
figure(2)
p1=plt.plot(x1,y1[:len(x1)],'o')
p2=plt.plot(x2,y2[:len(x2)],'x')
plt.title("Difference entre image complete et image tranche")
plt.show()
