import numpy as np

'''Second derivative of x
it takes a matrix as parameter 
and returns a matrix
'''


def derive2x(mat, m):
    d2x = np.zeros((m, m))
    for i in range(0, m-1):
        for j in range(0, m-1):
            d2x[i, j] = float(mat[i+1, j]) + \
                float(mat[i-1, j])-2*float(mat[i, j])
    return d2x


'''Second derivative of y
it takes a matrix as parameter 
and returns a matrix
'''


def derive2y(mat, m):
    d2y = np.zeros((m, m))
    for i in range(0, m-1):
        for j in range(0, m-1):
            d2y[i, j] = float(mat[i, j+1]) + \
                float(mat[i, j-1])-2*float(mat[i, j])
    return d2y


# Calculating the operator Laplacian


def laplacian(mat, m):
    d2x = derive2x(mat, m)
    d2y = derive2y(mat, m)
    lap = np.zeros((m, m))
    for i in range(0, m-1):
        for j in range(0, m-1):
            lap[i, j] = d2x[i, j]+d2y[i, j]
    return lap

# Shadow equation


def Shadow(mat, m):
    l = np.zeros((m, m))
    for i in range(0, m-1):  # Calcul du log
        for j in range(0, m-1):
            l[i, j] = np.log(mat[i, j]+0.00001)

    t = 0.25
    db = np.zeros((m, m))
    db = l
    db2x = np.zeros((m, m))
    for n in range(0, 80):  # calcul du font
        db2x = laplacian(db, m)
        for i in range(0, m-1):
            for j in range(0, m-1):
                db[i, j] = db[i, j]+t*max(0, db2x[i, j])
    return db

# This function calculates the exp of each pixel and returns the matrix


def expI(mat, m):
    R = np.zeros((m, m))
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


def log(mar, m):
    l = np.zeros((m, m))
    for i in range(0, m-1):  # Calcul du log
        for j in range(0, m-1):
            l[i, j] = np.log(mar[i, j]+0.00001)
    return l

# Implementing the text equation   CleanText = initialImage - shadow


def text(mar, R, m):
    textss = np.zeros((m, m))
    for i in range(0, m-1):
        for j in range(0, m-1):
            textss[i, j] = mar[i, j]-R[i, j]

    return textss
