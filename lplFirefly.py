import random
import math
import numpy as np


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
    alphat = 1.0
    bests = [0]*d
    # random.seed(0)  # gera sempre os mesmos numeros aleatorios

    randommatrix = []

    for i in range(n):
        threshold = random.sample(range(1, 255), d)
        threshold.sort()
        randommatrix.append(threshold)

    #/
    randommatrix = [[127, 207],
                    [74, 250],
                    [171, 4],
                    [243, 208],
                    [195, 158],
                    [169, 142],
                    [33, 62],
                    [24, 209],
                    [4, 67],
                    [73, 191]]

    for i in range(n):
        randommatrix[i].sort()
    #\

    r = []
    for i in range(n):
        lin = [0.0]*n
        r.append(lin)

    Z = [0]*n

    cont = 0

    while t < maxGenerarion:
        for i in range(n):
            Z[i] = -psrAvaliacaoShannon(H, randommatrix[i])

        # Z = [-12.6875, -11.0184, -10.4205, -9.0533, -9.5667, -9.5923, -11.8446, -11.8295, -10.5504, -12.8493]
        indice = np.argsort(Z)
        Z.sort()

        Z = [-x for x in Z]

        rank = [0]*n
        for i in range(n):
            rank[i] = randommatrix[indice[i]]
        randommatrix = rank

        for i in range(n):
            for j in range(n):
                r[i][j] = dist(randommatrix[i], randommatrix[j])
        alphat = alpha * alphat
        for i in range(n):
            for j in range(n):
                if Z[i] < Z[j]:
                    print("entrou")
                    threshold = random.sample(range(1, 255), d)
                    threshold.sort()
                    cont += 1

                    betat = beta*math.exp(-gamma*((r[i][j])**2))
                    print(betat)

                    if i != n-1:

                        for k in range(d):
                            randommatrix[i][k] = int(((1 - betat)*randommatrix[i][k] + betat*randommatrix[j][k] +
                                                     alphat*threshold[k])/(1+alphat))
                            #randommatrix[i][k] = (1 - betat) * randommatrix[i][k] + betat * (randommatrix[i][k]) + \
                            #                     threshold[k]
                            #randommatrix[i][k] = int(randommatrix[i][k] / (1 + alphat))
                        #print(randommatrix[i])


        bests = randommatrix[0]

        t += 1

    bests.sort()
    print(cont)

    return bests


def psrAvaliacaoShannon(histograma, elemento):
    elemento.insert(0, 0)
    elemento.append(256)
    n = len(elemento)

    a = elemento[0]+1
    b = elemento[1]
    # print(str(a) + " " + str(b))

    light = ShannonEntropy(histograma, a, b)
    # print(light)

    for i in range(1, n - 1):
        a = elemento[i] + 1
        b = elemento[i + 1]
        # print(str(a) + " " + str(b))

        ES = ShannonEntropy(histograma, a, b)
        # print(ES)
        light += ES

    elemento.remove(0)
    elemento.remove(256)

    return light


def ShannonEntropy(histograma, a, b):
    H = histograma[a:b+1]
    s = sum(H)
    if s > 0:
        H = [float(i) / s for i in H]
    L = len(H)
    S = 0

    for i in range(L):
        if H[i] != 0:
            S += H[i] * math.log(H[i])

    S *= -1

    return S


def dist(a, b):
    S = 0
    for k in range(len(a)):
        S += (a[k] - b[k]) ** 2
    S = math.sqrt(S)
    return S
