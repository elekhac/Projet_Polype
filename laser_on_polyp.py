# -*- coding: utf-8 -*-
"""
Created on Mon Mar 02 23:10:37 2015

@author: Elise
"""
import numpy as np
import cv2 as cv2
import matplotlib.colors as col
import matplotlib.pyplot as plt
from skimage.morphology import disk
import Fonctions_Analyse_Hough
from math import sqrt

# detecte le laser en fonction de sa saturation et brillance 
def Detect_laser(image):
    hsv= col.rgb_to_hsv((image/255.0))
    laser = np.zeros(image.shape[:2])
    for i in range(150,450):
        for j in range(260,640):
            if  hsv[i,j,1]<0.25 and hsv[i,j,2]>0.85:
                laser[i,j] = 1
    open_laser = cv2.morphologyEx(laser, cv2.MORPH_OPEN, disk(2))
    return open_laser

#retourne les coordonnees du laser qui se trouve sur le polype
# vu le traitement pour detecter le laser, normalement ca nous retournera
# le meme laser de Detect_laser
def laser_on_polyp(laser,center_x,center_y,radius):
    coord = []
    for i in range(150,450):
        for j in range(260,640):
            if laser[i,j] == 1 and ((j - center_x)**2 + (i - center_y)**2 < radius**2):
                coord.append((i,j))
    return coord

#retourne les 2 points extremes du laser dans le polype
def extreme_points(coord):
    max = 0
    x1=0
    y1=0
    x2=0
    y2=0
    for i in range(len(coord)):
        for j in range(len(coord)): 
            dist = sqrt((abs(coord[i][0]-coord[j][0]))**2 + (abs(coord[i][1]-coord[j][1]))**2)
            if (dist>max):
                max = dist
                x1,y1 = coord[i]
                x2,y2 = coord[j]
    return (x1,y1),(x2,y2)
                

    
    
img = cv2.imread('Images_Polypes//Polyps//image3284.png')
laser = Detect_laser(img)
#circle = Fonctions_Analyse_Hough.Analyse_Hough(img)
#if circle != None:
#    center_x = circle[0,0,0]
#    center_y = circle[0,0,1]
#    radius = circle[0,0,2]
#    coord =  laser_on_polyp(laser,center_x,center_y,radius)
#    points = extreme_points(coord)
#    print points

plt.subplot(2,1,1)
plt.imshow(laser)
plt.subplot(2,1,2)
plt.imshow(img)
