from PIL import Image
import numpy as np
import cv2
from utility import *


img = cv2.imread("Image2.png")  # Reading the image

im = Image.open("Image2.png")  # Opening the image

# Converting the image from RGB(colored) into Gray image

img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

mat = np.array(img)  # Creating an array/matrix from the image


# Creating arrays/matrix filled with zeros that have the same size as the given image

d2y = np.zeros(im.size)
d2x = np.zeros(im.size)
lap = np.zeros(im.size)
l = np.zeros(im.size)


# Getting the dimensions of the image

[n, m] = im.size


d2x = derive2x(mat, m)

d2y = derive2y(mat, m)

lap = laplacian(mat, m)

I = Shadow(mat, m)

mar = np.array(img)

P = expI(mar, m)

R = expI(I, m)

R = normalisation(R, np.amax(mar))

P = np.zeros(im.size)

mar = np.array(img)

l = log(mar, m)

textss = text(l, I, m)

textss = expI(textss, m)

textss = normalisation(textss, np.amax(mat))

# Saving the image with Clean text

new_im7 = Image.fromarray(textss)
if new_im7.mode != 'RGB':
    new_im7 = new_im7.convert('RGB')
new_im7.save("text.png")

# Saving the image with shadow only

new_im6 = Image.fromarray(R)
if new_im6.mode != 'RGB':
    new_im6 = new_im6.convert('RGB')
new_im6.save("font.png")
