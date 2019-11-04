import random
import math
import numpy as np


def lplFirefly(n, d, gamma, alpha, beta, maxGeneration, H):
    """"
    :param n: number of agents
    :param d: dimension
    :param gamma: absorption coefficient
    :param alpha: step of motion
    :param beta: attractivity factor
    :param maxGeneration: number of max generation
    :param H: histogram
    """

    t = 0
    alphat = 1.0
    bests = [0]*d
    random.seed(0)  # Reset the random generator

    fireflies = []

    # Generating the initial locations of n fireflies
    for i in range(n):
        threshold = random.sample(range(1, 255), d)
        threshold.sort()
        fireflies.append(threshold)

    # Iterations or pseudo time marching
    r = []
    for i in range(n):
        lin = [0.0]*n
        r.append(lin)

    Z = [0]*n

    while t < maxGeneration:  # Start itarations
        for i in range(n):
            Z[i] = -psrAvaliacaoShannon(H, fireflies[i])

        indice = np.argsort(Z)
        Z.sort()

        Z = [-x for x in Z]

        # Ranking the fireflies by their light intensity
        rank = [0]*n
        for i in range(n):
            rank[i] = fireflies[indice[i]]

        fireflies = rank

        for i in range(n):
            for j in range(n):
                r[i][j] = dist(fireflies[i], fireflies[j])

        alphat = alpha * alphat  # Reduce randomness as iterations proceed

        # Move all fireflies to the better locations
        for i in range(n):
            for j in range(n):
                if Z[i] < Z[j]:
                    threshold = random.sample(range(1, 255), d)
                    threshold.sort()

                    betat = beta*math.exp(-gamma*((r[i][j])**2))

                    if i != n-1:

                        for k in range(d):
                            fireflies[i][k] = int(((1 - betat)*fireflies[i][k] + betat*fireflies[j][k] +
                                                     alphat*threshold[k])/(1+alphat))
                            # fireflies[i][k] = (1 - betat) * fireflies[i][k] + betat * (fireflies[i][k]) + \
                            #                     threshold[k]
                            # fireflies[i][k] = int(fireflies[i][k] / (1 + alphat))

        bests = fireflies[0]

        t += 1

    bests.sort()

    return bests


def psrAvaliacaoShannon(histograma, elemento):
    elemento.insert(0, 0)
    elemento.append(256)
    n = len(elemento)

    a = elemento[0]+1
    b = elemento[1]

    light = ShannonEntropy(histograma, a, b)

    for i in range(1, n - 1):
        a = elemento[i] + 1
        b = elemento[i + 1]

        ES = ShannonEntropy(histograma, a, b)
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
