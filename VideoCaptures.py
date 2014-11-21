# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 22:48:58 2014

@author: Elise
"""
import cv2
import os

dirname = "images"
os.mkdir(dirname)

#ouvre le fichier video
video_capture = cv2.VideoCapture('20141016\\video2.avi')
#extrait le succes(= 0 si fin de la video) et l'image
sucess,image = video_capture.read()


count = 0
while sucess:
    sucess, image = video_capture.read()
    cv2.imwrite(os.path.join(dirname,"image%d.png" % count), image)
    if cv2.waitKey(10) == 27:
        break
    count +=1