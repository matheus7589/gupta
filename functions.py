from __future__ import division
import points
import math, numpy as np

K = len(points.pp_400)  # numero de nos possiveis para implantacao(total de genes)
k = 3  # k-cobertura
m = 2  # m-conectividade
# N = 100  # numero total de alvos

Rsen = 50.0
Rcom = 100.0

# posicoes_potenciais = []
# posicoes_potenciais.append(np.random.randint(0, 300, size=(1, 100)))
# print (posicoes_potenciais)


alvos = [(1, 273), (60, 255), (286, 282), (175, 260), (240, 240), (20, 162), (165, 28),
         (135, 121), (85, 156), (264, 81), (20, 171), (285, 52), (221, 77), (227, 53),
         (183, 0), (146, 16), (10, 36), (202, 176), (217, 228), (17, 208),
         (242, 138), (17, 57), (156, 94), (112, 8), (265, 271), (12, 8), (140, 173),
         (177, 32), (44, 93), (105, 257), (247, 165), (272, 127), (158, 281),
         (39, 127), (131, 231), (256, 253), (268, 16), (253, 150), (182, 181), (86, 55),
         (126, 268), (159, 159), (128, 244), (242, 183), (38, 168), (250, 91),
         (58, 121), (52, 31), (115, 64), (191, 215)]

# alvos = [(10, 40), (10, 97), (175, 257), (220, 168)]

PP = points.pp_400

# PP = [(25, 25), (25, 50), (25, 75), (25, 100), (25, 125), (25, 150), (25, 175), (25, 200), (25, 225), (25, 250),
#       (25, 275),
#       (50, 25), (50, 50), (50, 75), (50, 100), (50, 125), (50, 150), (50, 175), (50, 200), (50, 225), (50, 250),
#       (50, 275),
#       (75, 25), (75, 50), (75, 75), (75, 100), (75, 125), (75, 150), (75, 175), (75, 200), (75, 225), (75, 250),
#       (75, 275),
#       (100, 25), (100, 50), (100, 75), (100, 100), (100, 125), (100, 150), (100, 175), (100, 200), (100, 225),
#       (100, 250), (100, 275),
#       (125, 25), (125, 50), (125, 75), (125, 100), (125, 125), (125, 150), (125, 175), (125, 200), (125, 225),
#       (125, 250), (125, 275),
#       (150, 25), (150, 50), (150, 75), (150, 100), (150, 125), (150, 150), (150, 175), (150, 200), (150, 225),
#       (150, 250), (150, 275),
#       (175, 25), (175, 50), (175, 75), (175, 100), (175, 125), (175, 150), (175, 175), (175, 200), (175, 225),
#       (175, 250), (175, 275),
#       (200, 25), (200, 50), (200, 75), (200, 100), (200, 125), (200, 150), (200, 175), (200, 200), (200, 225),
#       (200, 250), (200, 275),
#       (225, 25), (225, 50), (225, 75), (225, 100), (225, 125), (225, 150), (225, 175), (225, 200), (225, 225),
#       (225, 250), (225, 275),
#       (250, 25), (250, 50), (250, 75), (250, 100), (250, 125), (250, 150), (250, 175), (250, 200), (250, 225),
#       (250, 250), (250, 275),
#       (275, 25), (275, 50), (275, 75), (275, 100), (275, 125), (275, 150), (275, 175), (275, 200), (275, 225),
#       (275, 250), (275, 275)]


# Funcoes para avaliar o individuo --------------------------------------------------

def dist_conn(alvo):
    distancia = []
    xalvo = alvo[0]
    yalvo = alvo[1]
    for sensor in PP:
        xsensor = sensor[0]
        ysensor = sensor[1]
        distancia.append(math.sqrt(math.pow((xsensor - xalvo), 2) + math.pow((ysensor - yalvo), 2)))
    return distancia


def dist_cov(alvo):
    distancia = []
    xalvo = alvo[0]
    yalvo = alvo[1]
    for sensor in PP:
        xsensor = sensor[0]
        ysensor = sensor[1]
        distancia.append(math.sqrt(math.pow((xsensor - xalvo), 2) + math.pow((ysensor - yalvo), 2)))
    return distancia


def Cov(alvo, individuo):
    distance = dist_cov(alvo)
    cont = 0
    for key, ind in enumerate(individuo):
        if ind == 1:
            if distance[key] < Rsen:
                cont += 1
    return cont


def CovCost(alvo, individuo):
    coverage = Cov(alvo, individuo)
    return k if coverage >= k else (coverage - k)  # abs e o absolute, o modulo do numero


def Com(sensor, individuo):
    distance = dist_conn(sensor)
    cont = 0
    for key, ind in enumerate(individuo):
        if ind == 1:
            if distance[key] > 0.0:
                if distance[key] <= Rcom:
                    cont += 1
    return cont


def ConnCost(sensor, individuo):
    connected = Com(sensor, individuo)
    return m if connected >= m else (connected - m)


def objetivo1(individuo):
    M = 0
    for gene in individuo: # usar funcao sum() ao inves do for
        if gene == 1:
            M += 1
    return (M / K)


def objetivo2(individuo):
    soma = 0
    N = 0
    for alvo in alvos:
        covcost = CovCost(alvo, individuo)
        soma += covcost
        if covcost > 0:
            N += 1
    if N == 0:
        return 0
    # print (soma, (soma / (N * k)), N*k)
    return (soma / (N * k))


def objetivo3(individuo):
    soma = 0
    M = 0
    for key, gene in enumerate(individuo):
        if gene == 1:
            concost = ConnCost(PP[key], individuo)
            soma += concost
            if concost > 0:
                M += 1
    if M == 0:
        return 0
    # print (soma / (M * m), soma, M*m)
    return (soma / (M * m))
