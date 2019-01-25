import random
import math


def lplFirefly(n, d, gamma, alpha, beta, maxGenerarion, H):
    """"
    :param n: number of agents
    :param d: dimension
    :param gamma: absorption coefficient
    :param alpha: step of motion
    :param beta: attractivity factor
    :param maxGenerarion: number of max generation
    :param H: histogram
    """

    t = 0
    alpha0 = 1.0

    randommatrix = []

    for i in range(n):
        threshold = random.sample(range(1, 255), d)
        threshold.sort()
        randommatrix.append(threshold)

    r = []
    lin = []
    lin.append(0*n)
    for i in range(n):
        r.append(lin)

    Z = []
    Z.append(0*n)

    while(t < maxGenerarion):
        for i in range(n):
            for j in range(n):
                Z[i] = psrAvaliacaoShannon(H, randommatrix[i])
                Z[j] = psrAvaliacaoShannon(H, randommatrix[j])
                r[i][j] = math.sqrt((Z[i] - Z[j]) ** 2)

        for i in range(n):
            # bright evaluation Z[fi]
            for j in range(n):
                if (Z[i] < Z[j]):
                    Z[i], Z[j] = Z[j], Z[i]

            threshold = random.sample(range(1, 255), d)
            threshold.sort()

        t += 1

    return bests


def psrAvaliacaoShannon(histograma, elemento):
    elemento.insert(0, 0)
    elemento.append(255)
    n  = len(elemento)

    a = elemento[0]
    b = elemento[1]

    light = ShannonEntropy(histograma, a, b)

    for i in range(n):
        a = elemento[i] + 1
        b = elemento[i + 1]

        ES = ShannonEntropy(histograma, a, b)
        light += ES

    return light


def ShannonEntropy(histograma, a , b):
    H = histograma[a : b]
    L = len(H)
    S = 0

    for i in range(L):
        if H[i] != 0:
            S += H[i] * math.log10(H[i])

    S *= -1

    return S

