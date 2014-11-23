# -*- coding: utf-8 -*-
"""
Created on Sun Nov 23 13:07:28 2014

@author: Hossein
"""
import pylab
import os
from skimage import data
import matplotlib.pyplot as plt
import Fonctions_Analyse2

#Ce code sauvegarde les graph des images dans un dossier a part, il nomme
#chaque graph en fonction de l image lui correspondant

directory = "graph_images"
compt = 0


#verifie qu'on ne va pas ecraser des donnees
while directory in os.listdir(os.curdir):
    compt=compt+1
    if not os.listdir(directory) == False:
        directory = directory + str(compt)


#cree le dossier s'il n'existait pas
if directory not in os.listdir(os.curdir):
    os.mkdir(directory)

#prend le repertoire contenant les images
ListeFichiers = os.listdir('images')

for i in range(len(ListeFichiers)):
    polDia = data.imread("images\\"+ListeFichiers[i])
    
    x2,y2 = Fonctions_Analyse2.Image_ws_tranche(polDia)
    
    p2=plt.plot(x2,y2[:len(x2)],'ro')
    plt.ylabel("# occurences")
    plt.xlabel("Difference de niveaux de gris (x : image tranchee)")
    plt.title("Difference entre image complete et image tranche")
    
    #enregistre chaque graph avec le bon format
    pylab.savefig(directory+"\\Graph_%s" % ListeFichiers[i])
    
    plt.cla
    plt.close()

