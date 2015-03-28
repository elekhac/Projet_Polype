# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 21:27:23 2015

@author: Elise
"""

import csv

#a = [3,4]
#b = []
#b.append(a)

#cree un nouveau fichier csv
#with open("output.csv", "wb") as f:
#    
#    writer = csv.writer(f)
#    writer.writerows(b)

#ajoute un tableau dans le fichier csv
#with open("output.csv", "a") as f:
#    
#    writer = csv.writer(f)
#    writer.writerows(b)

# affiche les differents tableaux du fichier csv
with open('output.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        print row
