import cv2

def CellDetectionImage(im0):

    im1 = cv2.cvtColor(im0, cv2.COLOR_BGR2GRAY)

    im1 = cv2.calcHist([im1],[0],None,[256],[0,256])

    H = psrGrayHistogram(im1)

    print(str(H))

    return


def psrGrayHistogram(im):

    Lin, Col= im.shape
    H = []
    for i in range(256):
        H.append(0)
    for y in range(1,Lin+1):
        for x in range(1, Col+1):
            H[im[y, x]+1] = H[im[y, x]+1] + 1
    # normalization
    H = H/(sum(H))
    return H
