# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

# le nom de fichier texte contenant les coordonées du graph

fichier_txt = "vertex1.txt"

# fct qui renvoie la liste des points sous forme de vecteurs x et y

x,y = np.loadtxt("C:\Users\Hossein\Desktop\PROJET polypes\\fichiers\\"+fichier_txt,unpack=True)

# graph des donnees

plt.plot(x,y,'o')

plt.xlabel("hauteur (m)")
plt.ylabel("profondeur (m)")
plt.title("representation du profil du polyp de l'image :" +fichier_txt)

plt.show()

# calcul la hauteur de la corde ( maximum d'une parabole par rapport a ses extremites)

def hauteur_corde(x,y,x1,x2):
    max = 0    
    coordx1=0
    coordx2=0
    while x[coordx1] <= x1:
        coordx1 += 1
    while x[coordx2] <= x2:
        coordx2 += 1
    for i in range(coordx1, coordx2):
        if (y[i]-y[coordx1])> max:
            max = (y[i]-y[coordx1])
    return max
            


# caclul du diametre a partie de la hauteur de la corde et de la ln de la corde        

def Calcul_diametre(x,y,x1,x2):
    D = 0 
    C = x2-x1
    F = hauteur_corde(x,y,x1,x2)
    try:
        D = 2*((F/2) + ( (C*C)/(8*F) ))
    except:
        print "profil choisi non adapté"
    return D
    
    
print Calcul_diametre(x,y,-0.0028,0.0042)