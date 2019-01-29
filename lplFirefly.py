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
    alphat = 1.0
    bests = [0]*d
    random.seed(0)  # gera sempre os mesmos numeros aleatorios

    randommatrix = []

    for i in range(n):
        threshold = random.sample(range(1, 255), d)
        threshold.sort()
        randommatrix.append(threshold)

    lin = [0]*n
    r = [lin]*n

    Z = [0]*n

    while t < maxGenerarion:
        for i in range(n):
            for j in range(n):
                Z[j] = psrAvaliacaoShannon(H, randommatrix[j])
                Z[i] = psrAvaliacaoShannon(H, randommatrix[i])
                r[i][j] = math.sqrt((Z[i] - Z[j]) ** 2)
        for i in range(n):
            Z[i] = psrAvaliacaoShannon(H, randommatrix[i])
            for j in range(i, n):
                if Z[i] < Z[j]:
                    threshold = random.sample(range(1, 255), d)
                    threshold.sort()

                    alphat = alpha * alphat
                    betat = beta/math.exp(-gamma*(r[i][j]**2))

                    print(str(betat) + " " + str(alphat))

                    for k in range(d):
                        randommatrix[i][k] = int((1-betat)*randommatrix[i][k] + betat*randommatrix[j][k] +
                                                 alphat*threshold[k])

        for i in range(n):
            Z[i] = psrAvaliacaoShannon(H, randommatrix[i])

        bigger = 0

        for i in range(1, n):
            if Z[bigger] < Z[i]:
                bigger = i

        bests = randommatrix[bigger]

        t += 1

    return bests


def psrAvaliacaoShannon(histograma, elemento):
    elemento.insert(0, 0)
    elemento.append(255)
    n = len(elemento)

    a = elemento[0]
    b = elemento[1]

    light = ShannonEntropy(histograma, a, b)

    for i in range(1, n - 1):
        a = elemento[i] + 1
        b = elemento[i + 1]

        ES = ShannonEntropy(histograma, a, b)
        light += ES

    elemento.remove(0)
    elemento.remove(255)

    return light


def ShannonEntropy(histograma, a, b):
    H = histograma[a:b]
    L = len(H)
    S = 0

    for i in range(L):
        if H[i] != 0:
            S += H[i] * math.log10(H[i])

    S *= -1

    return S

