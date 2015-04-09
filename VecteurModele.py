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
    nombreImages = 0
    
    # Dans le fichier output_9premiers, seules les lignes 0,1,3 nous interessent
    with open('output_9premiers.csv') as f:
        reader = csv.reader(f)
        for i in range(4):
            image_data = reader.next()
            PeriSurAire.append(image_data[8])
            #IntensiteMax.append(image_data[4])
            IntensiteMoyenne.append(image_data[5])
            Aire.append(image_data[2])
            nombreImages +=1
    PeriSurAire.pop(2)        #Elimination du 3eme element car problème dans image
    #IntensiteMax.pop(2)
    IntensiteMoyenne.pop(2)
    Aire.pop(2)
    nombreImages -=1
    
    #ceux-ci sont ceux qui nom pas
    # de terme "pb" dans leur nom dans le fichier csv
    
    
    with open('output.csv') as f:
        reader = csv.reader(f)
        for ligne in reader:
            if len(ligne) >1:  #evite les 9 premieres lignes mal encodees dans le csv
                nom_image = ligne[0]
                if "pb" not in nom_image :
                    PeriSurAire.append(ligne[8])
                    #IntensiteMax.append(ligne[4])
                    IntensiteMoyenne.append(ligne[5])
                    Aire.append(ligne[2])
                    nombreImages +=1
    PeriSurAire.pop(5)        #Elimination du 3eme element car copie du suivant
    #IntensiteMax.pop(5)
    IntensiteMoyenne.pop(5)
    Aire.pop(5)
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
    return vecteur
