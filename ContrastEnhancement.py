# -*- coding: utf-8 -*-

import skimage
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, exposure

img_init = data.imread("polyp.jpg")
img_gray = skimage.color.rgb2gray(img_init)
# meme operation que img_gray multiplie par 256
img_stretch = exposure.rescale_intensity(img_gray,out_range = (0,256))

plt.subplot(4,2,1)
plt.imshow(img_stretch, cmap = plt.cm.gray)
plt.colorbar()

h,bin = np.histogram(img_stretch[:], range(256))
plt.subplot(4,2,2)
plt.plot(h)

# Etirement de contraste : etirement des niveaux de gris dans un certain
# intervalle defini entre deux percentiles  
p1, p99 = np.percentile(img_gray, (1, 99))
img_rescale = exposure.rescale_intensity(img_gray, in_range=(p1, p99), out_range = (0,256))
plt.subplot(4,2,3)
plt.imshow(img_rescale, cmap = plt.cm.gray)
plt.colorbar()

h_rescale,bin_rescale = np.histogram(img_rescale[:],range(256))
plt.subplot(4,2,4)
plt.plot(h_rescale)

# Egalisation  de l'histogramme
img_eq = exposure.equalize_hist(img_gray)
img_eq_stretch = exposure.rescale_intensity(img_eq,out_range = (0,256))
plt.subplot(4,2,5)
plt.imshow(img_eq_stretch, cmap = plt.cm.gray)
plt.colorbar()

h_eq,bin_eq = np.histogram(img_eq_stretch[:],range(256))
plt.subplot(4,2,6)
plt.plot(h_eq)

# Egalisation adaptive a contraste limité (CLAHE) de l'histogramme
# au plus clip_limit est elevee (entre 0 et 1),
# au plus on a de contraste
img_adapteq = exposure.equalize_adapthist(img_gray, clip_limit=0.02)
img_adapteq_stretch = exposure.rescale_intensity(img_adapteq,out_range = (0,256))
plt.subplot(4,2,7)
plt.imshow(img_adapteq_stretch, cmap = plt.cm.gray)
plt.colorbar()

h_adapteq,bin_adapteq = np.histogram(img_adapteq_stretch[:],range(256))
plt.subplot(4,2,8)
plt.plot(h_adapteq)
