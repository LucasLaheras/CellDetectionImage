def psrMultiLimiarizacao(im, limiares):

    limiares.insert(0, 0)
    limiares.append(255)

    im1 = im

    L = len(limiares)

    Lim = []
    for i in range(L):
        Lim
    Lim = round((Lim - min(Lim)) / (max(Lim) - min(Lim)) * 255)

    lin, col = im.shape

    for y in range(lin):
        for x in range(col):

            t1 = limiares[0]
            t2 = limiares[1]

            if im1[y, x] >= t1 and im1[y, x] <= t2:
                im1[y, x] = Lim[0]
            else:
                i = 2
                clust = 1
                while clust:
                    t1 = limiares[i]
                    t2 = limiares[i+1]
                    if im1[y, x] >= t1 and im1[y, x] <= t2:
                        clust = 0
                        im1[y, x] = Lim[i]
                    i += 1

    return im1