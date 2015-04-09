# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 12:38:21 2015

@author: Elise
"""
import VecteurModele
import VecteurTest
import csv
import numpy as np
import matplotlib.pyplot as plt

vecteur = VecteurModele.generation_vecteur()
v_test,v_entier_test = VecteurTest.generation_vecteur()

list = []
for i in range(shape(vecteur_test)[0]):
    if v_test[i,0]>0.02 and v_test[i,0]< 0.1 and v_test[i,1]>75 and v_test[i,1]<175 and v_test[i,2]>1000 and v_test[i,2]<40000:
        list.append(["Polyp", v_entier_test[i][0],eval(v_entier_test[i][1]), v_entier_test[i][2], v_entier_test[i][4], v_entier_test[i][5]])
    else:
        list.append(["NoPolyp", v_entier_test[i][0],eval(v_entier_test[i][1]), v_entier_test[i][2], v_entier_test[i][4], v_entier_test[i][5]])
with open("results4Dbis_manuel.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(list)