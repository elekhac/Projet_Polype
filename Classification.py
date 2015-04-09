# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 16:48:35 2015

@author: Elise
"""

print(__doc__)

import VecteurModeleTotal
import VecteurTest
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from mpl_toolkits.mplot3d import Axes3D
from sklearn import svm

vecteur, estPolype = VecteurModeleTotal.generation_vecteur()
vecteur_test,vecteur_entier_test = VecteurTest.generation_vecteur()
mean = vecteur.mean(axis=0)
std = vecteur.std(axis=0)

clf = svm.OneClassSVM(nu=0.5, kernel="poly", degree = 3, gamma=0.0, tol = 0.001 )
clf.fit(vecteur, estPolype)
#print clf.support_vectors_

#pred = clf.decision_function(vecteur_test)
#print pred

y_pred_train = clf.predict(vecteur)
y_pred_test = clf.predict(vecteur_test)
n_error_train = y_pred_train[y_pred_train == -1].size
n_error_test = y_pred_test[y_pred_test == -1].size
print "error", n_error_train, n_error_test

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(vecteur[:, 0], vecteur[:, 1], vecteur[:, 2],c='red')
ax.scatter(vecteur_test[:, 0], vecteur_test[:, 1], vecteur_test[:, 2],c='green')

#Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
#Z = Z.reshape(xx.shape)
#
#plt.title("Novelty Detection")
#
#points_modele = plt.scatter(vecteur[:, 0], vecteur[:, 1], c='white')
#points_test = plt.scatter(vecteur_test_test[:, 0], vecteur_test[:, 1], c='green')
#plt.axis('tight')
#plt.xlim((0, 0.5))
#plt.ylim((0, 260))
#
#plt.show()
#
list = []
for i in range(shape(vecteur_test)[0]):
    if y_pred_test[i] == 1:
        list.append(["Polyp", vecteur_entier_test[i][0],eval(vecteur_entier_test[i][1]), vecteur_entier_test[i][2], vecteur_entier_test[i][4], vecteur_entier_test[i][5]])
    if y_pred_test[i] == -1:
        list.append(["NoPolyp", vecteur_entier_test[i][0],eval(vecteur_entier_test[i][1]), vecteur_entier_test[i][2], vecteur_entier_test[i][4], vecteur_entier_test[i][5]])
#list = []
#for i in range(shape(vecteur_test)[0]):
#    list.append([pred[i], vecteur_entier_test[i][0],eval(vecteur_entier_test[i][1]), vecteur_entier_test[i][3], vecteur_entier_test[i][4], vecteur_entier_test[i][5] ])
with open("results3Dbis3.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(list)
b = clf.get_params(True)
print b
