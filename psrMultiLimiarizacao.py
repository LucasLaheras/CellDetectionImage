def psrMultiLimiarizacao(im, limiares):

    limiares.insert(0, 0)
    limiares.append(255)

    im1 = im.copy()

    L = len(limiares)

    Lim = [round(i*255/(L-2)) for i in range(L-1)]

    lin, col = im.shape

    for y in range(lin):
        for x in range(col):

            t1 = limiares[0]
            t2 = limiares[1]

            if im1[y, x] >= t1 and im1[y, x] <= t2:
                im1[y, x] = Lim[0]
            else:
                i = 1
                clust = 1
                while clust:
                    t1 = limiares[i]
                    t2 = limiares[i+1]
                    if im1[y, x] >= t1 and im1[y, x] <= t2:
                        clust = 0
                        im1[y, x] = Lim[i]
                    i += 1

    limiares.remove(0)
    limiares.remove(255)

    return im1
