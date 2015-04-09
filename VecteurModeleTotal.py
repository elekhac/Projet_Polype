# -*- coding: utf-8 -*-
"""
Created on Mon Apr 06 12:38:16 2015

@author: Elise
"""

import csv
import numpy as np

# Generation d'un vecteur comprenant le rapport Perimetre/Aire
# et intensite des polypes d'apprendtissage

def generation_vecteur():
    PeriSurAire = []
    IntensiteMax = []
    IntensiteMoyenne = []
    Aire = []
    estPolype = [1,1,0,1,0,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,1,1,1,0,0,1,0,1]
    nombreImages = 0
    
    # Dans le fichier output_9premiers, seules les lignes 0,1,3 nous interessent
    with open('output_9premiers.csv') as f:
        reader = csv.reader(f)
        for ligne in reader:
            PeriSurAire.append(ligne[8])
            #IntensiteMax.append(image_data[4])
            IntensiteMoyenne.append(ligne[5])
            Aire.append(ligne[2])
            nombreImages +=1
    
    #ceux-ci sont ceux qui nom pas
    # de terme "pb" dans leur nom dans le fichier csv
    
    
    with open('output.csv') as f:
        reader = csv.reader(f)
        for ligne in reader:
            if len(ligne) >1:  #evite les 9 premieres lignes mal encodees dans le csv
                PeriSurAire.append(ligne[8])
                #IntensiteMax.append(ligne[4])
                IntensiteMoyenne.append(ligne[5])
                Aire.append(ligne[2])
                nombreImages +=1
    PeriSurAire.pop(13)        #Elimination du 13eme element car copie du 14eme
    #IntensiteMax.pop(5)
    IntensiteMoyenne.pop(13)
    Aire.pop(13)
    PeriSurAire.pop()        #Elimination du dernier element car descriptif, pas donnees
    #IntensiteMax.pop()
    IntensiteMoyenne.pop()
    Aire.pop()
    nombreImages -=2
    
    vecteur = np.zeros((nombreImages,3))
    for i in range(nombreImages):
        vecteur[i,0] = PeriSurAire[i]
        #vecteur[i,1] = IntensiteMax[i]
        vecteur[i,1] = IntensiteMoyenne[i]
        vecteur[i,2] = Aire[i]
    return vecteur, estPolype
