import cv2
import numpy as np
from psrGrayHistogram import psrGrayHistogram
from matplotlib import pyplot as plt


def CellDetectionImage(im0):
    # cnversão pra tons de cinza
    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    # equalização histogramica global
    im1 = cv2.equalizeHist(im1)

    # max(max(im1))
    print(max([valor for linha in im1 for valor in linha]))

    unique(im1)

    mostra(im1)

    # histograma
    H = psrGrayHistogram(im1)

    # segmentação binaria com firefly

    # multisegmentação

    # 3x dilatação binaria
    Lin, Col = im1.shape
    kernel = np.ones((Lin, Col), np.uint8)
    im2 = cv2.dilate(im1, kernel, 3)

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


def mostra(img, name='Name'):
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return
