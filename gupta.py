from __future__ import division
import random, functions
from deap import creator, base, tools, algorithms

TamPop = 60 #Tamanho da populacao
W1, W2, W3 = 0.4, 0.3, 0.3

CXPB, MUTPB = 0.5, 0.3

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # indica que irei maximizar a funcao fitness
creator.create("Individuo", list, fitness=creator.FitnessMax)
# a linha acima cria um individuo que herda as propriedades de 'list' e tem um atributo de fitness do tipo 'FitnessMax'

toolbox = base.Toolbox()  # a 'toolbox' armazena funcoes e seus metodos

# define 'attr_bool' como um atributo ou gene'), e preencho com numeros inteiros entre 0 e 1
toolbox.register("attr_bool", random.randint, 0, 1)

# define o individuo consistindo de n genes, informados no ultimo parametro
toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.attr_bool, n=functions.K)

# define a populacao como uma lista de individuoa
toolbox.register("populacao", tools.initRepeat, list, toolbox.individuo)


# a funcao objetivo, fitness, que sera maximizada
def Fitness(individuo):
    obj1 = functions.objetivo1(individuo)
    obj2 = functions.objetivo2(individuo)
    obj3 = functions.objetivo3(individuo)
    return ((W1*(1.0 - obj1)) + (W2 * obj2) + (W3 * obj3)),


# operadores -----------------------------

# registro da funcao fitness
toolbox.register("evaluate", Fitness)

# registro do operador de crossover
toolbox.register("mate", tools.cxOnePoint)

# registro do operador de mutacao, e sua probabilidade de ocorrer
toolbox.register("mutate", tools.mutFlipBit, indpb=MUTPB)

# registro do operador de selecao
toolbox.register("select", tools.selRoulette, k=TamPop)

# inicializa a populacao com n individuos
populacao = toolbox.populacao(n=TamPop)

random.seed(64)

print("Inicio da evolucao")

# Avalia a popualacao inteira
fitnesses = list(map(toolbox.evaluate, populacao))
for ind, fit in zip(populacao, fitnesses):
    ind.fitness.values = fit

print("  Avaliados %i individuos" % len(populacao))

# Pegas todos os valores de fitness
fits = [ind.fitness.values[0] for ind in populacao]
print (fits)

# Variavel que guarda o numero de geracoes
g = 0

while max(fits) < 0.94 and g < 100:
    # nova geracao
    g = g + 1
    print("-- Geracao %i --" % g)

    # Seleciona a nova geracao de individuos
    offspring = toolbox.select(populacao)
    # Cola os individuos selecionados
    offspring = list(map(toolbox.clone, offspring))

    # Aplicando a mutacao e o crossover no offspring
    for child1, child2 in zip(offspring[::2], offspring[1::2]):

        # Cruza 2 individuos com a probabilidade CXPB
        if random.random() < CXPB:
            toolbox.mate(child1, child2)

            # o valor de fitness das filhos
            # deve ser recalculado depois
            del child1.fitness.values
            del child2.fitness.values

    for mutant in offspring:

        # Muta um individuo com a probabilidade MUTPB
        if random.random() < MUTPB:
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Avalia um individuo com fitness invalido
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    print("  Avaliados %i individuos" % len(invalid_ind))

    # A populacao e substituida pelo seu offspring
    populacao[:] = offspring

    # junta todos os fitness numa lista e printa os status
    fits = [ind.fitness.values[0] for ind in populacao]

    length = len(populacao)
    mean = sum(fits) / length
    sum2 = sum(x * x for x in fits)

    print("  Min %s" % min(fits))
    print("  Max %s" % max(fits))
    print("  Avg %s" % mean)

    """Essa funcao aplica a parte de variacao da populacao
    (crossover e mutacao)"""
    # offspring = algorithms.varAnd(populacao, toolbox, cxpb=0.5, mutpb=0.3)
    # fits = toolbox.map(toolbox.evaluate, offspring)
    # print (fits)
    # for fit, ind in zip(fits, offspring):
    #     ind.fitness.values = fit
    # populacao = toolbox.select(offspring, k=len(populacao))

print("-- Fim da Evolucao --")

top10 = tools.selBest(populacao, k=1)
fits = [ind.fitness.values[0] for ind in top10]
teste = []
points = top10[0]
print (points, '\n', fits)
for key, plo in enumerate(points):
    if (plo == 1):
        teste.append(functions.PP[key])

plotax = []
plotay = []
for t in teste:
    plotax.append(t[0])
    plotay.append(t[1])

alvosx = []
alvosy = []
for a in functions.alvos:
    alvosx.append(a[0])
    alvosy.append(a[1])

ppx = []
ppy = []
for p in functions.PP:
    ppx.append(p[0])
    ppy.append(p[1])

import matplotlib.pyplot as plt

plt.plot(plotax, plotay, 'ro', ms=50)
# plt.plot(plotax, plotay, 'ro')
plt.plot(alvosx, alvosy, 'bo')
plt.plot(ppx, ppy, 'g^')
plt.axis([0, 300, 0, 300])
plt.ylabel('some numbers')
plt.show()

