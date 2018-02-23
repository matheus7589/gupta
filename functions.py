from __future__ import division
import points_grid, points_random
import math, numpy as np, random as rand
from scipy.spatial import distance
import os
import errno
# from matplotlib import pyplot as plt

K = len(points_random.pp_100)  # numero de nos possiveis para implantacao(total de genes)
k = 1  # k-cobertura
m = 1  # m-conectividade
# N = 100  # numero total de alvos

Rsen = 50.0
Rcom = 100.0


# posicoes_potenciais = []
# posicoes_potenciais.append(np.random.randint(0, 300, size=(1, 100)))
# print (posicoes_potenciais)
alvos = points_random.alvos1



PP = points_random.pp_100
#
# def set(argument):
#     switcher = {
#         '100': points_random.pp_100,
#         '200': points_random.pp_200,
#         '300': points_random.pp_300,
#         '400': points_random.pp_400,
#         '500': points_random.pp_500,
#     }
#
#     PP = switcher.get(argument)
# print("aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii\n")
# print(PP)

# Calcular distancias uma unica vez
dist_alvos_pontos = [[0 for i in range(len(PP))] for j in range(len(alvos))]

dist_pontos_pontos = [[0 for i in range(len(PP))] for j in range(len(PP))]

def calculate_distances():
    for key_a, value_a in enumerate(dist_alvos_pontos):
        for key_p, value_p in enumerate(value_a):
            dist_alvos_pontos[key_a][key_p] = dist(alvos[key_a], PP[key_p])


def calculate_pp_distances():
    for key_a, value_a in enumerate(dist_pontos_pontos):
        for key_p, value_p in enumerate(value_a):
            dist_pontos_pontos[key_a][key_p] = dist(PP[key_a], PP[key_p])



# Funcao para criar diretorio

def create_directory(i):
    directory = "/home/matheus/Documentos/Projeto_de_Graduacao/results/k1m1/100_pontos/exec_" + str(i + 1)
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    return directory


# Funcao completar posicoes potenciais

def complete_pp(potential_points, length):
    need = length - len(potential_points)
    x = np.random.uniform(0.0, 300.0, need)
    y = np.random.uniform(0.0, 300.0, need)
    for key, value in enumerate(x):
        potential_points = potential_points + ((value, y[key]),)

    return (potential_points)


# Funcao de pertubacao

def pertubation_point(ponto, raio):
    rad = raio
    num = 1

    t = np.random.uniform(0.0, 2.0 * np.pi, num)
    r = rad * np.sqrt(np.random.uniform(0.0, 1.0, num))
    x = r * np.cos(t)
    y = r * np.sin(t)

    # plt.plot(ponto[0], ponto[1], "bo", ms=10)
    # plt.plot(x+ponto[0], y+ponto[1], "ro", ms=1)
    # plt.axis([-15, 15, -15, 15])
    # plt.show()
    return (x + ponto[0]), (y + ponto[1])

# Funcao de crossover baseada no Flexible algorith paper

def swap_area_crossover(ind1, ind2):
    ativos = []
    for key, value in enumerate(ind1):
        if value == 1:
            ativos.append(key)
    indexes = rand.choices(ativos, k=2)
    p = ponto_medio(PP[indexes[0]], PP[indexes[1]])
    raio = (distance.euclidean(PP[indexes[0]], PP[indexes[1]]))/2
    for key, value in enumerate(ind1):
        if dist_swap(p, PP[key]) <= raio:
            aux = ind1[key]
            ind1[key] = ind2[key]
            ind2[key] = aux

    return ind1, ind2

# Funcao de mutacao

def mutFlipToZero(individual, indpb):

    for i in range(len(individual)):
        if rand.random() < indpb:
            individual[i] = 0

    return individual,


def ponto_medio(p1, p2):
    return (p1[0]+p2[0])/2, (p1[1]+p2[1])/2

# Funcoes para avaliar o individuo --------------------------------------------------

def dist(alvo, individuo):
    distancia = distance.euclidean(alvo, individuo)
    return distancia


def dist_swap(alvo, individuo):
    distancia = distance.euclidean(alvo, individuo)
    return distancia


# funcoes nao usadas
########################################################
# def dist_conn(alvo, individuo):
#     distancia = distance.euclidean(alvo, individuo)
#     return distancia
#
#
# def dist_cov(alvo, individuo):
#     # print (alvo, individuo)
#     distancia = distance.euclidean(alvo, individuo)
#     return distancia
########################################################


def Cov(alvo, individuo):
    cont = 0
    for key, ind in enumerate(individuo):
        if ind == 1:
            # distance = dist_cov(alvo, PP[key])
            distance = dist_alvos_pontos[alvo][key]
            if distance <= Rsen:
                cont += 1
    return cont


def CovCost(alvo, individuo):
    coverage = Cov(alvo, individuo)
    return k if coverage >= k else (coverage - k)  # abs e o absolute, o modulo do numero


def Com(sensor, individuo):
    cont = 0
    for key, ind in enumerate(individuo):
        if ind == 1:
            # distance = dist_conn(sensor, PP[key])
            distance = dist_pontos_pontos[sensor][key]
            if distance > 0.0: # evita o mesmo individuo
                if distance <= Rcom:
                    cont += 1
    return cont



def ConnCost(sensor, individuo):
    connected = Com(sensor, individuo)
    return m if connected >= m else (connected - m)


def objetivo1(individuo):
    M = sum(individuo)
    return (M / K)


def objetivo2(individuo):
    soma = 0
    N = 0
    for key, alvo in enumerate(points_random.alvos1):
        covcost = CovCost(key, individuo)
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
            # concost = ConnCost(PP[key], individuo)
            concost = ConnCost(key, individuo)
            soma += concost
            if concost > 0:
                M += 1
    if M == 0:
        return 0
    # print (soma / (M * m), soma, M*m)
    return (soma / (M * m))
