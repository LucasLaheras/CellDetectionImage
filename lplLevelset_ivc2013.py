import numpy as np
import matplotlib.pyplot as plt
import snake as sn
import cv2
import math
import scipy
from math import pi


def lpllevelset_ivc2013(*args):
    """""
    Matlab code implementing the paper
        'A new level set method for inhomogeneous image segmentation'
        Image and Vision Computing 31(2013) 809 C822
    Argin:
        img: input 2D gray image
        w: coefficient cordinating local and global forces
        ini: initial level set contour
    Argout:
        imgls: final level set surface
        imgrec: evolving level set contours


    V1.0 by LI Bing Nan @ HFUT, Nov 2013
    """""

    img = args[0]
    w = 0
    ini = 0

    if len(args) > 1:
        w = args[1]
    if len(args) > 2:
        ini = args[2]

    # TODO tranformar a imagem em preto e branco

    imgn = np.copy(img)

    # get the size
    nrow, ncol = img.shape

    if len(args) < 2 or w == 0:
        rho = 3

        kernel = np.ones((15, 15), np.uint8)

        # TODO encontrar uma função que funciona como o rangefilt

        rf = cv2.morphologyEx(imgn, cv2.MORPH_GRADIENT, kernel)

        #rf = cv2.morphologyEx(imgn, 1, kernel)

        ct = rf / (imgn.max())

        w = rho * np.mean(np.mean(ct))*(1 - ct)
        w = np.around(w, decimals=4)

    if len(args) < 3:
        #teste = 255*np.ones((nrow, ncol), np.uint8)
        u = sdf2circle(nrow, ncol, nrow/2, ncol/2, min(nrow/8, ncol/8))
        u = np.around(u, decimals=4)

    elif ini == 0:
        h_im = cv2.imshow(img, [])
        e = imellipse(gca)
        imgbk = createMask(e, h_im)

        u = 2 * (0.5 - imgbk)

    else:
        u = 2 * (0.5 - 1*(ini > 0.5))

    enta = 0.0001
    numIter = 1000
    timestep = 2

    # TODO encontrar uma função que funciona como o imfilter (definir dtype=cv2.CV_32S, para ter numeros com maior precisão)
    # imgfilt = scipy.ndimage.filters.median_filter(img, average_filter(25), mode='constant')

    # fspecial('average', 25) = average_filter(25)
    #imgfilt = scipy.misc.imfilter(img, average_filter(25))
    # ‘reflect’,’constant’,’nearest’,’mirror’, ‘wrap’
    #imgfilt = scipy.ndimage.convolve(img, average_filter(25), mode='constant')
    #imgfilt = scipy.ndimage.median_filter(img, size=100)
    #imgfilt = scipy.signal.convolve(img, average_filter(25))

    kernel = average_filter(25)

    imgfilt = cv2.filter2D(img, cv2.CV_64F, kernel, borderType=cv2.BORDER_REFLECT)
    #imgfilt = np.around(imgfilt, decimals=4)
    imgfilt[imgfilt < 0.00001] = 0

    #imgfilt = scipy.ndimage.filters.convolve(img, average_filter(25))

    #imgfilt = cv2.morphologyEx(img, average_filter(25))

    #imgfilt = cv2.imread("testea.png", 0)

    imgfilt = cv2.resize(imgfilt, img.shape)

    #mostra(img)

    imgfilt = cv2.subtract(imgfilt, img, dtype=cv2.CV_64F)

    #mostra(imgfilt)

    #mostra(imgfilt)

    #mostra(u)

    imgrec = np.copy(u)

    # start level set evolution
    ul0 = 0
    tcost = []

    #print("img")
    #print(np.unique(img))

    #mostra(img)
    #mostra(u)
    #mostra(w*255)
    #mostra(imgfilt)
    #print(np.unique(imgfilt))

    for k in range(numIter):
        # update level set function
        u = EVOL_BGFRLS(np.copy(img), np.copy(imgfilt), np.copy(u), np.copy(w), timestep)
        #u = np.around(u, decimals=4)

        ul = sum(sum(1*(u >= 0)))
        tcost.append(abs(ul - ul0) / ul)

        if tcost[k] <= enta:
            break
        ul0 = ul

    imgls = u.copy()

    return imgls, tcost, imgrec


def EVOL_BGFRLS(img, imgfilt, imgini, w, timestep):
    # This function updates the level set function according to Eq(22)
    phi = np.around(imgini.copy(), decimals=4)
    phi = NeumannBoundCond(phi)

    # print(np.unique(phi))

    phi = 1*(phi > 0) - 1*(phi < 0)

    Hphi = Heaviside(phi)

    c1, c2 = binaryfit(img.copy(), Hphi.copy())

    #[c1, c2] = np.around([c1, c2], decimals=4)
    #c1 = 22.0054
    # print("c1 " + str(c1))
    #c2 = 116.3988
    # print("c2 " + str(c2))

    # p1 = (img - (c1 + c2) / 2) / (c1 - c2)

    p1 = np.around(img - (c1 + c2) / 2, decimals=4) / (c1 - c2)
    #p1 = np.around(p1, decimals=4)

    #mostra(imgfilt)
    #print(np.unique(imgfilt))

    m1, m2 = binaryfit(imgfilt.copy(), Hphi.copy())
    #[m1, m2] = np.around([m1, m2], decimals=4)

    #m1 = 1.2387
    #print("m1 " + str(m1))
    #m2 = -24.0932
    #print("m2 " + str(m2))

    # p2 = (imgfilt - (m1 + m2) / 2) / (m1 - m2)
    p2 = np.around(imgfilt - (m1 + m2) / 2, decimals=4) / (m1 - m2)
    #p2 = np.around(p2, decimals=4)

    # updating the phi function
    # Original CV2001 paper
    phi = phi + timestep*(w*p1 + (1 - w)*p2)

    #phi = phi + np.around(timestep*(np.around(w*p1, decimals=4) + np.around((1 - w)*p2, decimals=4)), decimals=4)
    #phi = np.around(phi, decimals=4)

    #mostra(phi)

    #print(np.unique(phi))

    #mostra(phi)

    # TODO encontrar uma função que funciona como o imfilter
    G = np.array([[0.0369, 0.0392, 0.0400, 0.0392, 0.0369], [0.0392, 0.0416, 0.0424, 0.0416, 0.0392],
         [0.0400, 0.0424, 0.0433, 0.0424, 0.0400], [0.0392, 0.0416, 0.0424, 0.0416, 0.0392],
         [0.0369, 0.0392, 0.0400, 0.0392, 0.0369]])
    phi = cv2.filter2D(phi, cv2.CV_64F, G, borderType=cv2.BORDER_REFLECT)
    #phi = np.around(phi, decimals=4)
    #phi = scipy.ndimage.gaussian_filter(phi, 5, mode='reflect') # controlling smoothness

    #-9.849 < x < 7.8675
    #print(np.unique(phi))

    #mostra(phi)

    return phi


def Threshold(L, sg):

    G = [L*2 + 1][L*2 + 1]
    for y in range(-L, L):
        for x in range(-L, L):
            xi = x + L
            yi = y + L

            G[xi, yi] = np.exp(-[x**2 + y**2]/(2*sg**2))

            G[xi, yi] = G[xi, yi]/(2*pi*sg**2)

    return G


def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[h < np.finfo(h.dtype).eps*h.max()] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h


def binaryfit(Img, H_phi):
    a = Img * H_phi
    numer_1 = np.sum(a)
    denom_1 = np.sum(H_phi)
    C1 = numer_1 / denom_1

    b = (1-H_phi) * Img
    numer_2 = np.sum(b)
    c = 1 - H_phi
    denom_2 = np.sum(c)
    C2 = numer_2 / denom_2

    return C1, C2


def NeumannBoundCond(f):
    # Make a function satisfy Neumann boundary condition
    [ny, nx] = f.shape
    g = f.copy()

    g[0, 0] = g[2, 2]
    g[0, nx-1] = g[2, nx-3]
    g[ny-1, 0] = g[ny-3, 2]
    g[ny-1, nx-1] = g[ny-3, nx-3]

    g[0, 1:-1] = g[2, 1:-1]
    g[ny-1, 1:-1] = g[ny-3, 1:-1]

    g[1:-1, 0] = g[1:-1, 2]
    g[1:-1, nx-1] = g[1:-1, nx-3]

    return g


def rangefilt(img, kernel):
    lin, col = img.shape
    linK, colK = kernel.shape

    imgResult = np.copy(img)

    for i in range(lin):
        for j in range(col):

            iniLin = int(i - linK/2)
            fimLin = int(i + linK/2)
            iniCol = int(j - colK/2)
            fimCol = int(j + colK/2)

            if iniLin < 0:
                iniLin = 0
            if fimLin >= lin:
                iniLin = lin-1
            if iniCol < 0:
                iniCol = 0
            if fimCol >= lin:
                fimCol = lin - 1

            kernel = img[iniCol:fimCol, iniLin:fimLin]
            imgResult[j][i] = kernel.max() - kernel.min()

    return imgResult


def mostra(img, name='Name'):

    img1 = img.copy()

    img1 = img1.astype(np.uint8)

    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def Heaviside(phi):
    return 0.5*(1 + phi)


def sdf2circle(nrow, ncol, ic, jc, r):
    x = np.linspace(1, ncol, ncol)
    y = np.linspace(1, nrow, nrow)
    X, Y = np.meshgrid(x, y)
    sdf = np.sqrt((X - ic) ** 2 + (Y - jc) ** 2) - r

    return sdf


def average_filter(num):
    number = 1/(num*num)

    return number * np.ones((num, num))

