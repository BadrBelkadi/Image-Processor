from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from skimage import color
import math
from tkinter import *
from tkinter import filedialog
import os
import tkinter as tk
from PIL import Image, ImageTk


img = cv2.imread("448.png")  # Lecture de l'image

im = Image.open("448.png")  # Ouverture de l'image

# Converstion de l'image en mode blanc et noir
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

mat = np.array(img)  # Transformation de l'image en matrice


# Creation des matrices replis par des zéros
dx = np.zeros(im.size)
dy = np.zeros(im.size)
d2y = np.zeros(im.size)
d2x = np.zeros(im.size)
lap = np.zeros(im.size)
db = np.zeros(im.size)
l = np.zeros(im.size)

# Extraction des dimensions de l'image

[n, m] = im.size


def derive2x(mat):
    for i in range(0, m-1):      # Dérivée deuxiéme de x
        for j in range(0, m-1):
            d2x[i, j] = float(mat[i+1, j]) + \
                float(mat[i-1, j])-2*float(mat[i, j])
    return d2x


d2x = derive2x(mat)


def derive2y(mat):
    for i in range(0, m-1):      # Dérivée deuxiéme de y
        for j in range(0, m-1):
            d2y[i, j] = float(mat[i, j+1]) + \
                float(mat[i, j-1])-2*float(mat[i, j])
    return d2y


d2y = derive2y(mat)


def laplacian(mat):
    d2x = derive2x(mat)
    d2y = derive2y(mat)
    for i in range(0, m-1):      # Laplacian
        for j in range(0, m-1):
            lap[i, j] = d2x[i, j]+d2y[i, j]
    return lap


lap = laplacian(mat)


for i in range(0, m-1):  # Calcul du log
    for j in range(0, m-1):
        l[i, j] = np.log(mat[i, j]+0.00001)


def font(mat):

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


I = font(mat)


def expI(mat):
    R = np.zeros(im.size, dtype=float)
    for i in range(0, m-1):
        for j in range(0, m-1):
            R[i, j] = np.exp(mat[i, j])

    return R


def normalisation(I, MaxI):
    deca = 0
    maxI = np.amax(np.amax(I))
    minI = np.amin(np.amin(I))
    I = MaxI*(I-minI)/(deca+(maxI-minI))
    return I


mar = np.array(img)
P = expI(mar)

R = expI(I)
R = normalisation(R, np.amax(mar))
P = np.zeros(im.size)


new_im6 = Image.fromarray(R)  # Engeristrement de  (image)
if new_im6.mode != 'RGB':
    new_im6 = new_im6.convert('RGB')
new_im6.save("font.png")


mar = np.array(img)


def log(mar):
    l = np.zeros(im.size, dtype=float)
    for i in range(0, m-1):  # Calcul du log
        for j in range(0, m-1):
            l[i, j] = np.log(mar[i, j]+0.00001)
    return l


l = log(mar)


def text(mar, R):
    textss = np.zeros(im.size, dtype=float)
    for i in range(0, m-1):
        for j in range(0, m-1):
            textss[i, j] = mar[i, j]-I[i, j]

    return textss


textss = text(l, I)
textss = expI(textss)

textss = normalisation(textss, np.amax(mat))


new_im7 = Image.fromarray(textss)  # Engeristrement de  (image)
if new_im7.mode != 'RGB':
    new_im7 = new_im7.convert('RGB')
new_im7.save("text.png")


def showimage():
    file = filedialog.askopenfilename(initialdir="/", title="choisir une image", filetypes=(
        ("JPG files", ".jpg"), ("PNG files", ".png"), ("All files", ".")))
    img = Image.open(file)  # Ouverture de l'image uploadé
    img.thumbnail((300, 300))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img

    return True


def text():
    img = Image.open('text.png')
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img
    return True


def font():
    img = Image.open('font.png')
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img
    return True


'''
root = Tk()

frm = Frame(root)
frm.pack(side=BOTTOM, padx=15, pady=15)

lbl = Label(root)
lbl.pack()

btn = Button(frm, text="Ajouter une image", command=showimage)
btn.pack(side=tk.LEFT)


btn = Button(frm, text="Afficher le texte", command=lambda: text())
btn.pack(side=tk.LEFT, padx=10)

btn = Button(frm, text="Afficher le font", command=lambda: font())
btn.pack(side=tk.LEFT, padx=10)


btn = Button(frm, text="Exit", command=lambda: exit())
btn.pack(side=tk.LEFT, padx=20)


root.title("PFE")
root.geometry("600x500")
root.mainloop()
'''
