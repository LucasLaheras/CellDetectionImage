import cv2
import numpy as np
from psrGrayHistogram import psrGrayHistogram
from matplotlib import pyplot as plt
from lplFirefly import lplFirefly
from psrMultiLimiarizacao import psrMultiLimiarizacao
from levelsetITK import levelset

def CellDetectionImage(im0):
    # conversão pra tons de cinza
    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    # equalização histogramica global
    im1 = lplHisteq(im1)

    # histograma
    H = psrGrayHistogram(im1)
    # H = cv2.equalizeHist(im1)

    # gaus2
    # H = [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0002, 0.0002, 0.0003, 0.0003, 0.0003, 0.0004, 0.0004, 0.0005, 0.0006, 0.0006, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011, 0.0012, 0.0014, 0.0015, 0.0016, 0.0018, 0.0020, 0.0022, 0.0024, 0.0026, 0.0028, 0.0030, 0.0032, 0.0035, 0.0037, 0.0040, 0.0043, 0.0046, 0.0049, 0.0052, 0.0055, 0.0058, 0.0061, 0.0064, 0.0067, 0.0070, 0.0072, 0.0075, 0.0078, 0.0081, 0.0083, 0.0086, 0.0088, 0.0090, 0.0092, 0.0094, 0.0095, 0.0097, 0.0098, 0.0099, 0.0099, 0.0100, 0.0100, 0.0100, 0.0099, 0.0099, 0.0098, 0.0097, 0.0095, 0.0094, 0.0092, 0.0090, 0.0088, 0.0086, 0.0083, 0.0081, 0.0078, 0.0075, 0.0072, 0.0070, 0.0067, 0.0064, 0.0061, 0.0058, 0.0055, 0.0052, 0.0049, 0.0046, 0.0043, 0.0040, 0.0037, 0.0035, 0.0032, 0.0030, 0.0028, 0.0026, 0.0024, 0.0022, 0.0020, 0.0018, 0.0016, 0.0015, 0.0014, 0.0012, 0.0011, 0.0010, 0.0009, 0.0008, 0.0007, 0.0006, 0.0006, 0.0005, 0.0004, 0.0004, 0.0003, 0.0003, 0.0003, 0.0002, 0.0002, 0.0002, 0.0002, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0002, 0.0002, 0.0002, 0.0002, 0.0003, 0.0003, 0.0003, 0.0004, 0.0004, 0.0005, 0.0006, 0.0006, 0.0007, 0.0008, 0.0009, 0.0010, 0.0011, 0.0012, 0.0014, 0.0015, 0.0016, 0.0018, 0.0020, 0.0022, 0.0024, 0.0026, 0.0028, 0.0030, 0.0032, 0.0035, 0.0037, 0.0040, 0.0043, 0.0046, 0.0049, 0.0052, 0.0054, 0.0058, 0.0061, 0.0064, 0.0067, 0.0070, 0.0072, 0.0075, 0.0078, 0.0081, 0.0083, 0.0086, 0.0088, 0.0090, 0.0092, 0.0094, 0.0095, 0.0097, 0.0098, 0.0099, 0.0099, 0.0100, 0.0100, 0.0100, 0.0099, 0.0099, 0.0098, 0.0097, 0.0095, 0.0094, 0.0092, 0.0090, 0.0088, 0.0086, 0.0083, 0.0081, 0.0078, 0.0075, 0.0072, 0.0070, 0.0067, 0.0064, 0.0061, 0.0058, 0.0054, 0.0052, 0.0049, 0.0046, 0.0043, 0.0040, 0.0037, 0.0035, 0.0032, 0.0030, 0.0028, 0.0026, 0.0024, 0.0022, 0.0020, 0.0018, 0.0016, 0.0015, 0.0014, 0.0012, 0.0011, 0.0010, 0.0009, 0.0008, 0.0007, 0.0006, 0.0006, 0.0005, 0.0004, 0.0004, 0.0003, 0.0003, 0.0003, 0.0002, 0.0002, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001]

    # gaus3
    # H = [0.0008, 0.0009, 0.0010, 0.0011, 0.0012, 0.0013, 0.0015, 0.0016, 0.0017, 0.0019, 0.0020, 0.0022, 0.0024, 0.0025, 0.0027, 0.0058, 0.0060, 0.0061, 0.0063, 0.0064, 0.0065, 0.0066, 0.0066, 0.0067, 0.0067, 0.0068, 0.0068, 0.0068, 0.0067, 0.0067, 0.0066, 0.0066, 0.0065, 0.0064, 0.0063, 0.0061, 0.0060, 0.0058, 0.0057, 0.0055, 0.0053, 0.0051, 0.0049, 0.0047, 0.0045, 0.0044, 0.0042, 0.0040, 0.0038, 0.0036, 0.0034, 0.0032, 0.0030, 0.0028, 0.0027, 0.0025, 0.0024, 0.0022, 0.0021, 0.0020, 0.0019, 0.0018, 0.0017, 0.0016, 0.0016, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0016, 0.0016, 0.0017, 0.0018, 0.0019, 0.0020, 0.0021, 0.0022, 0.0023, 0.0025, 0.0026, 0.0028, 0.0030, 0.0031, 0.0033, 0.0035, 0.0037, 0.0039, 0.0041, 0.0043, 0.0045, 0.0047, 0.0048, 0.0050, 0.0052, 0.0054, 0.0056, 0.0057, 0.0059, 0.0060, 0.0061, 0.0063, 0.0064, 0.0064, 0.0065, 0.0066, 0.0066, 0.0066, 0.0067, 0.0066, 0.0066, 0.0066, 0.0065, 0.0064, 0.0064, 0.0063, 0.0061, 0.0060, 0.0059, 0.0057, 0.0056, 0.0054, 0.0052, 0.0050, 0.0048, 0.0047, 0.0045, 0.0043, 0.0041, 0.0039, 0.0037, 0.0035, 0.0033, 0.0031, 0.0030, 0.0028, 0.0026, 0.0025, 0.0023, 0.0022, 0.0021, 0.0020, 0.0019, 0.0018, 0.0017, 0.0016, 0.0016, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0015, 0.0016, 0.0016, 0.0017, 0.0018, 0.0019, 0.0020, 0.0021, 0.0022, 0.0024, 0.0025, 0.0027, 0.0028, 0.0030, 0.0032, 0.0033, 0.0035, 0.0037, 0.0039, 0.0041, 0.0043, 0.0045, 0.0047, 0.0049, 0.0051, 0.0053, 0.0054, 0.0056, 0.0058, 0.0059, 0.0061, 0.0062, 0.0063, 0.0064, 0.0065, 0.0066, 0.0066, 0.0067, 0.0067, 0.0067, 0.0067, 0.0067, 0.0066, 0.0066, 0.0065, 0.0064, 0.0063, 0.0062, 0.0061, 0.0059, 0.0058, 0.0056, 0.0054, 0.0053, 0.0051, 0.0049, 0.0047, 0.0045, 0.0043, 0.0041, 0.0039, 0.0037, 0.0035, 0.0033, 0.0031, 0.0029, 0.0027, 0.0025, 0.0023, 0.0022, 0.0020, 0.0019, 0.0017, 0.0016, 0.0015, 0.0013, 0.0012, 0.0011, 0.0010, 0.0009, 0.0008, 0.0007, 0.0007, 0.0006, 0.0005, 0.0005]

    # gaus4
    # H = [0.0001, 0.0001, 0.0001, 0.0002, 0.0003, 0.0003, 0.0004, 0.0006, 0.0007, 0.0009, 0.0011, 0.0014, 0.0016, 0.0020, 0.0024, 0.0028, 0.0032, 0.0037, 0.0043, 0.0049, 0.0055, 0.0061, 0.0067, 0.0072, 0.0078, 0.0083, 0.0088, 0.0092, 0.0095, 0.0098, 0.0099, 0.0100, 0.0099, 0.0098, 0.0095, 0.0092, 0.0088, 0.0083, 0.0078, 0.0072, 0.0067, 0.0061, 0.0055, 0.0049, 0.0043, 0.0037, 0.0032, 0.0028, 0.0024, 0.0020, 0.0016, 0.0014, 0.0011, 0.0009, 0.0007, 0.0006, 0.0004, 0.0003, 0.0003, 0.0002, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0002, 0.0003, 0.0003, 0.0004, 0.0006, 0.0007, 0.0009, 0.0011, 0.0014, 0.0016, 0.0020, 0.0024, 0.0028, 0.0032, 0.0037, 0.0043, 0.0049, 0.0054, 0.0060, 0.0067, 0.0072, 0.0078, 0.0083, 0.0088, 0.0092, 0.0095, 0.0098, 0.0099, 0.0100, 0.0099, 0.0098, 0.0095, 0.0092, 0.0088, 0.0083, 0.0078, 0.0072, 0.0067, 0.0060, 0.0054, 0.0049, 0.0043, 0.0037, 0.0032, 0.0028, 0.0024, 0.0020, 0.0016, 0.0014, 0.0011, 0.0009, 0.0007, 0.0006, 0.0004, 0.0003, 0.0003, 0.0002, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0002, 0.0003, 0.0003, 0.0004, 0.0006, 0.0007, 0.0009, 0.0011, 0.0014, 0.0016, 0.0020, 0.0024, 0.0028, 0.0032, 0.0037, 0.0043, 0.0049, 0.0054, 0.0060, 0.0067, 0.0072, 0.0078, 0.0083, 0.0088, 0.0092, 0.0095, 0.0098, 0.0099, 0.0100, 0.0099, 0.0098, 0.0095, 0.0092, 0.0088, 0.0083, 0.0078, 0.0072, 0.0067, 0.0060, 0.0054, 0.0049, 0.0043, 0.0037, 0.0032, 0.0028, 0.0024, 0.0020, 0.0016, 0.0014, 0.0011, 0.0009, 0.0007, 0.0006, 0.0004, 0.0003, 0.0003, 0.0002, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0002, 0.0002, 0.0003, 0.0003, 0.0004, 0.0006, 0.0007, 0.0009, 0.0011, 0.0014, 0.0016, 0.0020, 0.0024, 0.0028, 0.0032, 0.0037, 0.0043, 0.0049, 0.0054, 0.0061, 0.0067, 0.0072, 0.0078, 0.0083, 0.0088, 0.0092, 0.0095, 0.0098, 0.0099, 0.0100, 0.0099, 0.0098, 0.0095, 0.0092, 0.0088, 0.0083, 0.0078, 0.0072, 0.0067, 0.0061, 0.0054, 0.0049, 0.0043, 0.0037, 0.0032, 0.0028, 0.0024, 0.0020, 0.0016, 0.0014, 0.0011, 0.0009, 0.0007, 0.0006, 0.0004, 0.0003, 0.0003, 0.0002, 0.0001, 0.0001, 0.0001, 0.0001]

    # gaus5
    # H = [0.0005, 0.0006, 0.0007, 0.0009, 0.0011, 0.0013, 0.0016, 0.0019, 0.0022, 0.0026, 0.0030, 0.0035, 0.0039, 0.0044, 0.0049, 0.0054, 0.0058, 0.0063, 0.0067, 0.0071, 0.0074, 0.0077, 0.0079, 0.0080, 0.0080, 0.0080, 0.0079, 0.0077, 0.0074, 0.0071, 0.0067, 0.0063, 0.0058, 0.0054, 0.0049, 0.0044, 0.0039, 0.0035, 0.0030, 0.0026, 0.0023, 0.0019, 0.0016, 0.0014, 0.0012, 0.0010, 0.0009, 0.0008, 0.0007, 0.0007, 0.0007, 0.0008, 0.0009, 0.0010, 0.0012, 0.0014, 0.0016, 0.0019, 0.0022, 0.0026, 0.0030, 0.0034, 0.0039, 0.0044, 0.0048, 0.0053, 0.0058, 0.0062, 0.0067, 0.0070, 0.0074, 0.0076, 0.0078, 0.0079, 0.0080, 0.0079, 0.0078, 0.0076, 0.0074, 0.0070, 0.0067, 0.0062, 0.0058, 0.0053, 0.0048, 0.0044, 0.0039, 0.0034, 0.0030, 0.0026, 0.0022, 0.0019, 0.0016, 0.0014, 0.0012, 0.0010, 0.0009, 0.0008, 0.0007, 0.0007, 0.0007, 0.0008, 0.0009, 0.0010, 0.0012, 0.0014, 0.0016, 0.0019, 0.0022, 0.0026, 0.0030, 0.0034, 0.0039, 0.0044, 0.0048, 0.0053, 0.0058, 0.0062, 0.0067, 0.0070, 0.0074, 0.0076, 0.0078, 0.0079, 0.0080, 0.0079, 0.0078, 0.0076, 0.0074, 0.0070, 0.0067, 0.0062, 0.0058, 0.0053, 0.0048, 0.0044, 0.0039, 0.0034, 0.0030, 0.0026, 0.0022, 0.0019, 0.0016, 0.0014, 0.0012, 0.0010, 0.0009, 0.0008, 0.0007, 0.0007, 0.0007, 0.0008, 0.0009, 0.0010, 0.0012, 0.0014, 0.0016, 0.0019, 0.0022, 0.0026, 0.0030, 0.0034, 0.0039, 0.0044, 0.0048, 0.0053, 0.0058, 0.0062, 0.0067, 0.0070, 0.0074, 0.0076, 0.0078, 0.0079, 0.0080, 0.0079, 0.0078, 0.0076, 0.0074, 0.0070, 0.0067, 0.0062, 0.0058, 0.0053, 0.0048, 0.0044, 0.0039, 0.0034, 0.0030, 0.0026, 0.0022, 0.0019, 0.0016, 0.0014, 0.0012, 0.0010, 0.0009, 0.0008, 0.0007, 0.0007, 0.0007, 0.0008, 0.0009, 0.0010, 0.0012, 0.0014, 0.0016, 0.0019, 0.0022, 0.0026, 0.0030, 0.0034, 0.0039, 0.0044, 0.0048, 0.0053, 0.0058, 0.0063, 0.0067, 0.0070, 0.0074, 0.0076, 0.0078, 0.0079, 0.0080, 0.0079, 0.0078, 0.0076, 0.0074, 0.0070, 0.0067, 0.0063, 0.0058, 0.0053, 0.0048, 0.0044, 0.0039, 0.0034, 0.0030, 0.0026, 0.0022, 0.0019, 0.0016, 0.0013, 0.0011, 0.0009, 0.0007, 0.0006, 0.0004, 0.0004, 0.0003, 0.0002, 0.0002, 0.0001, 0.0001, 0.0001]

    # segmentação binaria com firefly
    bests = lplFirefly(50, 1, 1, 0.97, 1, 100, H)

    # multisegmentação
    im2 = psrMultiLimiarizacao(im1, bests)

    # 3x dilatação binaria
    kernel = np.ones((3, 3), np.uint8)
    im2 = cv2.dilate(im2, kernel, iterations=3)

    # obtem somente a maior região = região de interesse
    ret, thresh = cv2.threshold(im2, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    idx = 0
    for i in range(1, len(contours)):
        if len(contours[idx]) < len(contours[i]):
            idx = i

    # separa somente a maior região de interesse
    lin, col = im2.shape
    im3 = np.zeros([lin, col], dtype=np.uint8)

    cv2.drawContours(im3, contours, idx, 255, -1)

    # histograma na região de interesse
    im4 = histLocalEq(im3, im0)

    mostra(im4)

    M = cv2.moments(im4)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # level-set somente na região de interesse
    im5 = levelset(im4, cX, cY)
    mostra(im5)

    # normalização
    maior = im5.max
    menor = im5.min
    im5 = 255 - (((im5 - menor) / (maior - menor)) * 255)

    # binarização das regiões de interesse
    for y in range(lin):
        for x in range(col):
            if im5[y, x] < 128:
                im5[y, x] = 0
            else:
                im5[y, x] = 255

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
    cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return


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
