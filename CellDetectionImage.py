import cv2
import numpy as np
from psrGrayHistogram import psrGrayHistogram
from matplotlib import pyplot as plt
from lplFirefly import lplFirefly
from psrMultiLimiarizacao import psrMultiLimiarizacao
from lplLevelset_ivc2013 import lpllevelset_ivc2013
import random
from scipy import ndimage


def histeq(im, nbr_bins=256):
  """  Histogram equalization of a grayscale image. """

  # get image histogram
  imhist, bins = np.histogram(im.flatten(), nbr_bins, normed=True)
  cdf = imhist.cumsum() # cumulative distribution function
  cdf = 255 * cdf / cdf[-1] # normalize

  # use linear interpolation of cdf to find new pixel values
  im2 = np.interp(im.flatten(),bins[:-1],cdf)

  return im2.reshape(im.shape), cdf


def CellDetectionImage(im0):
    # conversion to grayscale
    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    #print(np.unique(im1))
    #mostra(im1)
    #im1 = im0

    # global histogrammic equalization
    im1 = lplHisteq(im1)

    cv2.imwrite('histeq.png', im1)
    #im1 = cv2.equalizeHist(im1)
    #im1, _ = histeq(im1)
    #print(np.unique(im1))
    #mostra(im1)

    #im1 = cv2.equalizeHist(im1)

    # histogram
    H = psrGrayHistogram(im1)
    H = np.around(H, decimals=4)

    # H = cv2.equalizeHist(im1)

    # binary segmentation with firefly
    bests = lplFirefly(150, 3, 1, 0.97, 1, 100, H)
    #bests = [211, 225, 250]

    # print(bests)

    # multisegmentation
    im2 = psrMultiLimiarizacao(im1, bests)

    #print(np.unique(im1))

    # print(np.unique(im2))

    #todo diferent
    # 3x binary dilation
    #im2 = ndimage.binary_dilation(im2)
    im2[im2 > 0] = 255
    kernel = np.ones((3, 3), np.uint8)
    im2 = cv2.dilate(im2, kernel, iterations=3)

    # print(np.unique(im2))

    # get only the largest region = region of interest
    ret, thresh = cv2.threshold(im2, 128, 255, 0)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    idx = 0
    for i in range(1, len(contours)):
        if len(contours[idx]) < len(contours[i]):
            idx = i

    # separates only the region of interest
    lin, col = im2.shape
    im3 = np.zeros([lin, col], dtype=np.uint8)

    #TODO configure set bigger region
    im3 = cv2.drawContours(im3, contours, idx, 1, -1)

    #print(np.unique(im3))

    #mostra(im3*255)

    # histogram in the region of interest
    im4 = histLocalEq(im3, im0)

    #im4 = cv2.imread("histogramaLocal.png", 0)

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
    img1 = img.copy()

    img1 = img1.astype(np.uint8)

    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, img1)
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
    label_hue = np.uint8(179 * labels / (np.max(labels)))
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

    H1 = [0] * 256
    for y in range(lin):
        for x in range(col):
            if msk[y, x]:
                H1[im1[y, x]] = H1[im1[y, x]] + 1

    for i in range(1, 256):
        H1[i] = H1[i] + H1[i - 1]

    H1 = [x / H1[255] for x in H1]

    im2 = np.zeros([lin, col], dtype=np.uint8)
    for y in range(lin):
        for x in range(col):
            if msk[y, x]:
                im2[y, x] = int(round(H1[im1[y, x]] * 255))
                if im2[y, x] > 255:
                    im2[y, x] = 255

    return im2
