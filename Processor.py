from PIL import Image
import numpy as np
import cv2


'''Second derivative of x
it takes a matrix as parameter 
and returns a matrix
'''


def derive2x(mat):
    for i in range(0, m-1):
        for j in range(0, m-1):
            d2x[i, j] = float(mat[i+1, j]) + \
                float(mat[i-1, j])-2*float(mat[i, j])
    return d2x


'''Second derivative of y
it takes a matrix as parameter 
and returns a matrix
'''


def derive2y(mat):
    for i in range(0, m-1):
        for j in range(0, m-1):
            d2y[i, j] = float(mat[i, j+1]) + \
                float(mat[i, j-1])-2*float(mat[i, j])
    return d2y


# Calculating the operator Laplacian


def laplacian(mat):
    d2x = derive2x(mat)
    d2y = derive2y(mat)
    for i in range(0, m-1):
        for j in range(0, m-1):
            lap[i, j] = d2x[i, j]+d2y[i, j]
    return lap

# Shadow equation


def Shadow(mat):

    for i in range(0, m-1):  # Calcul du log
        for j in range(0, m-1):
            l[i, j] = np.log(mat[i, j]+0.00001)

    t = 0.25
    db = l

    for n in range(0, 80):  # calcul du font
        db2x = laplacian(db)
        for i in range(0, m-1):
            for j in range(0, m-1):
                db[i, j] = db[i, j]+t*max(0, db2x[i, j])
    return db

# This function calculates the exp of each pixel and returns the matrix


def expI(mat):
    R = np.zeros(im.size, dtype=float)
    for i in range(0, m-1):
        for j in range(0, m-1):
            R[i, j] = np.exp(mat[i, j])

    return R

# This function makes sure we don't go over the 256 pixel


def normalisation(I, MaxI):
    deca = 0
    maxI = np.amax(np.amax(I))
    minI = np.amin(np.amin(I))
    I = MaxI*(I-minI)/(deca+(maxI-minI))
    return I

# This function calculates the log of every pixel of the image/matrix and returns it


def log(mar):
    l = np.zeros(im.size, dtype=float)
    for i in range(0, m-1):  # Calcul du log
        for j in range(0, m-1):
            l[i, j] = np.log(mar[i, j]+0.00001)
    return l

# Implementing the text equation   CleanText = initialImage - shadow


def text(mar, R):
    textss = np.zeros(im.size, dtype=float)
    for i in range(0, m-1):
        for j in range(0, m-1):
            textss[i, j] = mar[i, j]-R[i, j]

    return textss


img = cv2.imread("Image2.png")  # Reading the image

im = Image.open("Image2.png")  # Opening the image

# Converting the image from RGB(colored) into Gray image

img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

mat = np.array(img)  # Creating an array/matrix from the image


# Creating empty arrays/matrix that have the same size as the given image
dx = np.zeros(im.size)
dy = np.zeros(im.size)
d2y = np.zeros(im.size)
d2x = np.zeros(im.size)
lap = np.zeros(im.size)
l = np.zeros(im.size)

# Getting the dimensions of the image

[n, m] = im.size


d2x = derive2x(mat)

d2y = derive2y(mat)

lap = laplacian(mat)

I = Shadow(mat)

mar = np.array(img)

P = expI(mar)

R = expI(I)

R = normalisation(R, np.amax(mar))

P = np.zeros(im.size)

mar = np.array(img)

l = log(mar)

textss = text(l, I)

textss = expI(textss)

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
