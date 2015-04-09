# -*- coding: utf-8 -*-
"""
Created on Mon Apr 06 12:55:08 2015

@author: Elise
"""
import csv
import numpy as np

def generation_vecteur():
    PeriSurAire = []
    IntensiteMax = []
    IntensiteMoyenne = []
    Aire= []
    Centroide = []
    NomImage = []
    nombreImages = 0
    
    # Dans le fichier output_9premiers, seules les lignes 0,1,3 nous interessent
    with open('output_ET_bon.csv') as f:
        reader = csv.reader(f)
        for ligne in reader:
            PeriSurAire.append(ligne[8])
            IntensiteMax.append(ligne[4])
            IntensiteMoyenne.append(ligne[5])
            Aire.append(ligne[2])
            NomImage.append(ligne[0])
            Centroide.append(ligne[1])
            nombreImages +=1
    vecteur = np.zeros((nombreImages,3))
    vecteur_entier = []
    for i in range(nombreImages):
        vecteur[i,0] = PeriSurAire[i]
        #vecteur[i,1] = IntensiteMax[i]
        vecteur[i,1] = IntensiteMoyenne[i]
        vecteur[i,2] = Aire[i]
        vecteur_entier.append([NomImage[i],Centroide[i],PeriSurAire[i],IntensiteMax[i], IntensiteMoyenne[i],Aire[i]])

    return vecteur,vecteur_entier

#v,v1 = generation_vecteur()
#print v1
#print shape(v1)
#centroid = eval(v1[0][1])
#print centroid
