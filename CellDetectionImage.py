import cv2
import numpy as np
from psrGrayHistogram import psrGrayHistogram
from matplotlib import pyplot as plt
import SwarmPackagePy


def CellDetectionImage(im0):
    # conversão pra tons de cinza
    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    # equalização histogramica global
    im1 = pshisteq(im1)
    mostra(im1)

    # histograma
    H = psrGrayHistogram(im1)

    print(H)

    # segmentação binaria com firefly
    bests = SwarmPackagePy.fa.get_Gbest(SwarmPackagePy.fa(100, H, 0, 255, 1024, 0.1))

    print(bests)

    # multisegmentação

    # 3x dilatação binaria
    Lin, Col = im1.shape
    kernel = np.ones((Lin, Col), np.uint8)
    im2 = cv2.dilate(im1, kernel, 3)


    # obtem somente a maior região = região de interesse

    # separa somente a maior região de interesse

    # histograma na região de interesse

    # level-set somente na rtegião de interesse

    # normalização

    # colorização randomica das regiões de interesse

    return


def unique(image):
    unique = []

    for i in range(256):
        unique.append(0)

    lin, col = image.shape

    for y in range(lin):
        for x in range(col):
            unique[image[y][x]] = 1

    for i in range(256):
        if unique[i] > 0:
            print(i)

    return

def histograma(image):

    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    cdf = hist.cumsum()

    cdf_normalized = cdf * (hist.max() / cdf.max())
    plt.plot(cdf_normalized, 'b')
    plt.hist(image.flatten(), 256, [0, 256], 'r')
    plt.xlim([0, 256])
    plt.legend(('cdf', 'histogram'), 'upper left')
    plt.show()

    return


def mostra(img, name='Name'):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


def maxmax(image):
    print(max([valor for linha in image for valor in linha]))


def pshisteq(im1):
    H = psrGrayHistogram(im1)

    for i in range(255):
        H[i+1] = H[i+1] + H[i]

    lin, col = im1.shape

    imeq = im1

    for y in range(lin):
        for x in range(col):
            imeq[y, x] = round(H[im1[y, x]]*255)

    return imeq
