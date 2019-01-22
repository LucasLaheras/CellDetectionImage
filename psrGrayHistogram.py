def psrGrayHistogram(im):

    Lin, Col= im.shape
    H = []
    for i in range(256):
        H.append(0)
    for y in range(Lin):
        for x in range(Col):
            H[im[y, x]] = H[im[y, x]] + 1

    # normalization
    soma = sum(H)
    size = len(H)
    for i in range(size):
        H[i] = H[i] / soma

    # print(H)

    return H
