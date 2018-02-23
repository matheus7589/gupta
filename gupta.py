from __future__ import division
import random, functions, points_random
from deap import creator, base, tools, algorithms
# from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import multiprocessing


TamPop = 60 #Tamanho da populacao
W1, W2, W3 = 0.4, 0.3, 0.3

CXPB, MUTPB = 0.5, 0.03

list_km = ['k2m1', 'k3m1', 'k2m2', 'k2m3', 'k1m2', 'k1m3', 'k3m2', 'k3m3']

list_pp = ['100', '200', '300', '400', '500']


functions.calculate_distances()
functions.calculate_pp_distances()

if __name__ == "__main__":

    for i in range(0, 30):

        # Armazenamento de informacao sobre a execucao
        melhores = []
        melhores_global = []
        points_global = []

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
        # toolbox.register("mate", functions.swap_area_crossover)
        toolbox.register("mate", tools.cxOnePoint)

        # registro do operador de mutacao, e sua probabilidade de ocorrer
        toolbox.register("mutate", functions.mutFlipToZero, indpb=MUTPB)
        # toolbox.register("mutate", tools.mutFlipBit, indpb=MUTPB)

        # registro do operador de selecao
        toolbox.register("select", tools.selTournament, tournsize=3)
        # toolbox.register("select", tools.selRoulette)

        # Inicia o Multithreading
        pool = multiprocessing.Pool()
        toolbox.register("map", pool.map)

        # inicializa a populacao com n individuos
        populacao = toolbox.populacao(n=TamPop)


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

        # random.seed(64)

        while max(fits) < 0.99 and g < 400:
            # nova geracao
            g = g + 1
            print("-- Geracao %i --" % g)

            # Seleciona a nova geracao de individuos
            offspring = toolbox.select(populacao, len(populacao))

            # Clona os individuos selecionados
            offspring = list(map(toolbox.clone, offspring)) # retorna uma lista aplicando a funcao clone em cada individuo da populacao

            # offspring = algorithms.varAnd(offspring, toolbox, cxpb=CXPB, mutpb=0.03)

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

            # length = len(populacao)
            # mean = sum(fits) / length
            # sum2 = sum(x * x for x in fits)
            #
            # print("  Min %s" % min(fits))
            # print("  Max %s" % max(fits))
            # print("  Avg %s" % mean)

            # Armazena o informacoes referentes a cada execucao
            melhores.append(max(fits))


        print("-- Fim da Evolucao --")


        top10 = tools.selBest(populacao, k=1)
        fits = [ind.fitness.values[0] for ind in top10]
        teste = []
        points = top10[0]

        # melhores globais
        melhores_global.append(max(fits))
        points_global.append(sum(points))

        print(points, '\n', fits)
        print("numero de sensores implantados", sum(points))

        for key, plo in enumerate(points):
            if plo == 1:
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

        '''Cria o diretorio para salvar os testes realizados'''
        directory = functions.create_directory(i)

        plt.figure()

        # Demostra a posicao dos pontos
        plt.plot(plotax, plotay, 'ro', ms=115, alpha=0.2)
        # plt.plot(plotax, plotay, 'yo', ms=100, alpha=0.1)
        # plt.plot(plotax, plotay, 'ro')
        plt.plot(alvosx, alvosy, 'bo')
        plt.plot(ppx, ppy, 'g^')
        plt.axis([0, 300, 0, 300])
        plt.ylabel('Representacao do Melhor Individuo')
        path = directory + "/evolucao_" + str(i + 1) + ".png"
        plt.savefig(path)
        # plt.show()

        # Cria uma nova instancia de figura para separar os plots
        plt.figure()

        # Grafico de convergencia
        plt.plot(melhores)
        plt.ylabel('Grau de Precisao')
        plt.xlabel('Numero de Geracoes')
        path_converg = directory + "/convergencia_" + str(i + 1) + ".png"
        plt.savefig(path_converg)


        # Escrevendo informacoes da execucao
        f = open(directory + '/info.txt', 'w')
        f.write('Media = ' + str(sum(melhores)/len(melhores)) + '\n' + 'Variancia = ' + str(functions.np.var(melhores)) +
                '\n' + 'Numero de Sensores implantados = ' + str(sum(points)) + '\n' + 'Avaliacao do Melhor Individuo = ' +
                str(max(fits)) + '\n' + 'Melhor individuo = ' + str(points))
        f.close()

        # Encerra o multithreading
        pool.close()

    directory_global = "/home/matheus/Documentos/Projeto_de_Graduacao/results/k1m1/100_pontos"

    # Escrevendo informacoes da execucao global
    f = open(directory_global + '/info_global.txt', 'w')
    f.write('Media = ' + str(sum(melhores_global)/len(melhores_global)) + '\n' + 'Variancia = ' +
            str(functions.np.var(melhores_global)) + '\n' + 'Media de Sensores implantados = ' +
            str(sum(points_global)/len(points_global)) + '\n' + 'Melhor execucao = ' + str(max(melhores_global)) )
    f.close()



    #Voronoi
    # vor = Voronoi(points_random.alvos1)
    #
    # voronoi_plot_2d(vor)
    #
    #
    # path = directory + "/evolucao_" + str(i+1) + ".png"
    # plt.savefig(path)

    # plt.show()


