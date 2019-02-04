import numpy as np
import math

def levelset_ivc2013(im, w = 0, ini = 0):
    """"
        :param im: input 2D gray image;
        :param w: coefficient cordinating local and global forces
        :param ini: initial level set contour
    """
    img = im.copy()

    imgn = 255*(img-img.min())/(img.max()-img.min())

    # get the size
    nrow, ncol = img.shape

    if nargin < 2 or w < 0:
        rho = 3

        rf = rangefilt(imgn, np.ones((15, 15), np.uint8))
        ct = rf/(imgn.max())

        w = rho*mean(mean(ct))*(1-ct)

    if nargin < 3:
        u = sdf2circle(nrow, ncol, nrow / 2, ncol / 2, min(nrow / 8, ncol / 8))

    elif ini == 0:
        e = imellipse(gca)
        imgbk = createMask(e, h_im)

        u = 2*(0.5-imgbk)
    else:
        u = 2*(0.5-(ini > 0.5))

    enta = 0.0001
    numIter = 1000
    timestep = 2

    #imgfilt =
    imgfilt = imgfilt - img

    imgrec = u

    # start level set evolution
    u10 = 0
    tcost = 0
    for k in range(numIter):
        # update level set function
        u = EVOL_BGFRLS(img, imgfilt, u, w, timestep)
        ul = sum(sum(u >= 0))
        if abs(ul - ul0) / ul <= enta:
            break
        ul0 = ul

    imgls = u

    return imgls, tcost, imgrec


def EVOL_BGFRLS(img, imgfilt, imgini, w, timestep):
    # This function updates the level set function according to Eq(22)
    phi = imgini
    phi = NeumannBoundCond(phi)

    phi = (phi>0) - (phi<0)

    Hphi = Heaviside(phi)

    c1, c2 = binaryfit(img, Hphi)
    p1 = (img-(c1 + c2)/2)/(c1 - c2)

    m1, m2 = binaryfit(imgfilt, Hphi)
    p2 = (img - (m1 + m2) / 2) / (m1 - m2)

    # updating the phi function   # Original CV2001 paper
    phi = phi + timestep*(w*p1+(1-w)*p2)

    #phi = imfilter()

    return phi


def binaryfit(Img, H_phi):
    a = Img * H_phi
    numer_1 = sum(a)
    denom_1 = sum(H_phi)
    C1 = numer_1/denom_1

    b = (1 - H_phi) * Img
    numer_2 = sum(b)
    c = 1 - H_phi
    denom_2 = sum(c)
    C2 = numer_2 / denom_2

    return C1, C2


def NeumannBoundCond(f):
    # Make a function satisfy Neumann boundary condition
    nrow, ncol = f.shape
    g = f
    g([1 nrow],[1 ncol]) = g([3 nrow-2],[3 ncol-2])
    g([1 nrow],2:end-1) = g([3 nrow-2],2:end-1)
    g(2:end-1,[1 ncol]) = g(2:end-1,[3 ncol-2])

    return g


def Heaviside(phi):
    return 0.5 * (1 + phi)


def sdf2circle(nrow, ncol, ci, cj, rd):
    # computes the signed distance to a circle
    a = [i+1 for i in range(ncol)]
    b = [i+1 for i in range(nrow)]
    X, Y = np.meshgrid(a, b)
    f = math.sqrt((X-cj)**2+(Y-ci)**2)-rd

    return f
