import cv2
import numpy as np
from psrGrayHistogram import psrGrayHistogram
from matplotlib import pyplot as plt
from lplFirefly import lplFirefly
from psrMultiLimiarizacao import psrMultiLimiarizacao
from lplLevelset_ivc2013 import lpllevelset_ivc2013
import random

def CellDetectionImage(im0):
    # conversion to grayscale
    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    # global histogrammic equalization
    im1 = lplHisteq(im1)

    # histogram
    H = psrGrayHistogram(im1)
    # H = cv2.equalizeHist(im1)

    # binary segmentation with firefly
    bests = lplFirefly(50, 1, 1, 0.97, 1, 100, H)

    # multisegmentation
    im2 = psrMultiLimiarizacao(im1, bests)

    # 3x binary dilation
    kernel = np.ones((3, 3), np.uint8)
    im2 = cv2.dilate(im2, kernel, iterations=3)

    # get only the largest region = region of interest
    ret, thresh = cv2.threshold(im2, 127, 255, 0)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    idx = 0
    for i in range(1, len(contours)):
        if len(contours[idx]) < len(contours[i]):
            idx = i

    # separates only the region of interest
    lin, col = im2.shape
    im3 = np.zeros([lin, col], dtype=np.uint8)

    cv2.drawContours(im3, contours, idx, 255, -1)

    # histogram in the region of interest
    im4 = histLocalEq(im3, im0)

    # level-set in the region of interest
    im5, _, _ = lpllevelset_ivc2013(im4)

    # normalization
    maior = im5.max()
    menor = im5.min()
    im5 = 255 - (((im5 - menor) / (maior - menor)) * 255)

    # binarization of the regions of interest
    im5[im5 < 128] = 0
    im5[im5 >= 128] = 255

    im5 = im5.astype(np.uint8)

    # random colorization of the regions of interest
    im_out = individualregioncolor(im5)

    mostra(im_out)

    return im_out


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


def histograma(image):

    hist, bins = np.histogram(image.flatten(), 256, [0, 256])
    cdf = hist.cumsum()

    cdf_normalized = cdf * (hist.max() / cdf.max())
    plt.plot(cdf_normalized, 'b')
    plt.hist(image.flatten(), 256, [0, 256], 'r')
    plt.xlim([0, 256])
    plt.legend(('cdf', 'histogram'), 'upper left')
    plt.show()


def mostra(img, name='Name'):
    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def maxmax(image):
    print(max([valor for linha in image for valor in linha]))


def lplHisteq(im1):
    H = psrGrayHistogram(im1)

    for i in range(255):
        H[i+1] = H[i+1] + H[i]

    lin, col = im1.shape

    imeq = im1

    for y in range(lin):
        for x in range(col):
            imeq[y, x] = round(H[im1[y, x]]*255)

    return imeq


def individualregioncolor(im1):
    try:
        _, _ = im1.shape
        im2 = im1
    except:
        im2 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)

    im2 = cv2.threshold(im2, 127, 255, cv2.THRESH_BINARY)[1]  # ensure binary
    ret, labels = cv2.connectedComponents(im2)

    # Map component labels to hue val
    label_hue = np.uint8(179 * labels / (np.max(labels)/10))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])

    # cvt to BGR for display
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)

    # set bg label to black
    labeled_img[label_hue == 0] = 0

    return labeled_img


def histLocalEq(msk, im0):

    lin, col = msk.shape
    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    H1 = [0]*256
    for y in range(lin):
        for x in range(col):
            if msk[y, x]:
                H1[im1[y, x]] = H1[im1[y, x]] + 1

    for i in range(1, 256):
        H1[i] = H1[i] + H1[i-1]

    H1 = [x/H1[255] for x in H1]

    im2 = np.zeros([lin, col], dtype=np.uint8)
    for y in range(lin):
        for x in range(col):
            if msk[y, x]:
                im2[y, x] = int(round(H1[im1[y, x] + 1]*255))
                if im2[y, x] > 255:
                    im2[y, x] = 255

    return im2
