from __future__ import division
from statistics import mean
import random, functions, points_random, bar_chart, points_grid
from deap import creator, base, tools, algorithms
# from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import shelve as sh
import matplotlib.patches as mpatches
import multiprocessing


TamPop = 60 #Tamanho da populacao
# W1, W2, W3 = 0.1, 0.45, 0.45
W1, W2, W3 = 0.4, 0.3, 0.3

CXPB, MUTPB = 0.5, 0.03

# list_km = ['k3m3']
list_km = ['k1m1', 'k1m2', 'k1m3', 'k2m1', 'k2m2', 'k2m3', 'k3m1', 'k3m2', 'k3m3']

list_pp = ['100', '200', '300', '400', '500']

test_type = ['artigo', 'proposto']

def get_test_type(argument):
    switcher = {
        'artigo': [artigo(), "/home/matheus/Documentos/Projeto_de_Graduacao/results/"],
        'proposto': [proposto(), "/home/matheus/Documentos/Projeto_de_Graduacao/results_alterado/"],
    }
    return switcher.get(argument)

def proposto():
    funcoes = functions.Functions(set_points_altered(pontos_potenciais),
                                  len(set_points_altered(pontos_potenciais)),
                                  set_restrictions(restricoes)[0], set_restrictions(restricoes)[1])

    funcoes.set_pp(funcoes.complete_pp(funcoes.get_pp(),
                                       len(set_points(pontos_potenciais))))  # completa o numero de pontos

    new_pontos = []
    for key, p in enumerate(funcoes.get_pp()):
        new_pontos.append(funcoes.pertubation_point(p, 10, 1))

    funcoes.set_pp(new_pontos)  # seta os pontos com a perturbacao

    return funcoes

def artigo():
    funcoes = functions.Functions(set_points(pontos_potenciais),
                                  len(set_points(pontos_potenciais)),
                                  set_restrictions(restricoes)[0], set_restrictions(restricoes)[1])

    return funcoes


def set_points(argument):
    switcher = {
        '100': points_random.pp_100,
        '200': points_random.pp_200,
        '300': points_random.pp_300,
        '400': points_random.pp_400,
        '500': points_random.pp_500,
    }
    return switcher.get(argument)

def set_points_altered(argument):
    switcher = {
        '100': points_random.pp_voronoi_alvos1,
        '200': points_random.pp_voronoi_alvos1,
        '300': points_random.pp_voronoi_alvos1,
        '400': points_random.pp_voronoi_alvos1,
        '500': points_random.pp_voronoi_alvos1,
    }
    return switcher.get(argument)


def set_restrictions(argument):
    switcher = {
        'k1m1': [1, 1],
        'k2m1': [2, 1],
        'k3m1': [3, 1],
        'k2m2': [2, 2],
        'k2m3': [2, 3],
        'k1m2': [1, 2],
        'k1m3': [1, 3],
        'k3m2': [3, 2],
        'k3m3': [3, 3],
    }
    return switcher.get(argument)


if __name__ == "__main__":

    chart = bar_chart.Chart()
    with sh.open('database.db') as db:
        if 'chart' in db:
            chart = db['chart']
            # db['skip_list_pp'] = 0
            # db['skip_i'] = 28
            # print(db['skip_list_pp'])
            # print(db['skip_i'])
        else:
            db['chart'] = chart

        '''Continue test_types'''
        if 'skip_test_type' in db:
            # if db['skip_test_type'] == len(test_type):
            #     skip_test_type = 0
            # else:
            skip_test_type = db['skip_test_type']
        else:
            skip_test_type = 0
        '''Continue test_types'''

        #tá dentro do shelv with
        for index_type, type in enumerate(test_type):
            # continua o for de onde parou
            if index_type < skip_test_type:
                continue
            db['skip_test_type'] = index_type

            '''Continue da lista de restricoes'''
            if 'skip_list_km' in db:
                # if db['skip_list_km'] == len(list_km):
                #     skip_list_km = 0
                # else:
                skip_list_km = db['skip_list_km']
            else:
                skip_list_km = 0
            '''Continue da lista de restricoes'''

            for index_restricoes, restricoes in enumerate(list_km):
                # continua o for de onde parou
                if index_restricoes < skip_list_km:
                    continue
                db['skip_list_km'] = index_restricoes

                '''Continue dos pontos potenciais'''
                if 'skip_list_pp' in db:
                    # if db['skip_list_pp'] == len(list_pp):
                    #     skip_list_pp = 0
                    # else:
                    skip_list_pp = db['skip_list_pp']
                else:
                    skip_list_pp = 0
                '''Continue dos pontos potenciais'''

                for index_pp, pontos_potenciais in enumerate(list_pp):
                    # continua o for de onde parou
                    if index_pp < skip_list_pp:
                        continue

                    db['skip_list_pp'] = index_pp

                    # Armazenamento de informacao sobre a execucao
                    melhores_global = []
                    worst_global = []
                    best_global = []
                    points_global = []

                    funcoes = get_test_type(type)[0]

                    funcoes.init_distances()
                    funcoes.calculate_distances()
                    funcoes.calculate_pp_distances()

                    '''Continue das 30 execucoes'''
                    if 'skip_i' in db:
                        if db['skip_i'] == 29:
                            skip_i = 0
                        else:
                            skip_i = db['skip_i']
                    else:
                        skip_i = 0
                    '''Continue das 30 execucoes'''

                    for i in range(0, 30):

                        if i < skip_i:
                            continue

                        db['skip_i'] = i

                        # Armazenamento de informacao sobre a execucao
                        melhores = []
                        points_inner = []

                        creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # indica que irei maximizar a funcao fitness
                        creator.create("Individuo", list, fitness=creator.FitnessMax)
                        # a linha acima cria um individuo que herda as propriedades de 'list' e tem um atributo de fitness do
                        # tipo 'FitnessMax'

                        toolbox = base.Toolbox()  # a 'toolbox' armazena funcoes e seus metodos

                        # define 'attr_bool' como um atributo ou gene'), e preencho com numeros inteiros entre 0 e 1
                        toolbox.register("attr_bool", random.randint, 0, 1)

                        # define o individuo consistindo de n genes, informados no ultimo parametro
                        toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.attr_bool, n=funcoes.get_K())

                        # define a populacao como uma lista de individuoa
                        toolbox.register("populacao", tools.initRepeat, list, toolbox.individuo)

                        # a funcao objetivo, fitness, que sera maximizada
                        def Fitness(individuo):

                            obj1 = funcoes.objetivo1(individuo)
                            obj2 = funcoes.objetivo2(individuo)
                            obj3 = funcoes.objetivo3(individuo)
                            # print('Objetivo 1 = ', obj1)
                            # print('Objetivo 2 = ', obj2)
                            # print('Objetivo 3 = ', obj3)

                            return ((W1*(1.0 - obj1)) + (W2 * obj2) + (W3 * obj3)),


                        # operadores -----------------------------

                        # registro da funcao fitness
                        toolbox.register("evaluate", Fitness)

                        # registro do operador de crossover
                        if type == 'proposto':
                            toolbox.register("mate", funcoes.swap_area_crossover)
                        else:
                            toolbox.register("mate", tools.cxOnePoint)

                        # registro do operador de mutacao, e sua probabilidade de ocorrer
                        toolbox.register("mutate", funcoes.mutFlipToZero, indpb=MUTPB)
                        # toolbox.register("mutate", tools.mutFlipBit, indpb=MUTPB)

                        # registro do operador de selecao
                        toolbox.register("select", tools.selTournament, tournsize=3)
                        # toolbox.register("select", tools.selRoulette)

                        # Inicia o Multithreading
                        # pool = multiprocessing.Pool()
                        # toolbox.register("map", pool.map)

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
                        # print(fits)

                        # Variavel que guarda o numero de geracoes
                        g = 0

                        while max(fits) < 1.0 and g < 400:
                            # nova geracao
                            g = g + 1
                            print("-- Geracao %i --" % g)

                            # Seleciona a nova geracao de individuos
                            offspring = toolbox.select(populacao, len(populacao))

                            # Clona os individuos selecionados
                            offspring = list(map(toolbox.clone, offspring)) # retorna uma lista aplicando a funcao clone em cada
                            #  individuo da populacao

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
                            print("  Max %s" % max(fits))
                            # print("  Avg %s" % mean)

                            # Armazena o informacoes referentes a cada execucao
                            melhores.append(max(fits))
                            points_inner.append(tools.selBest(populacao, k=1)[0])

                        print("-- Fim da Evolucao --")

                        top10 = tools.selBest(populacao, k=1)
                        worst = tools.selWorst(populacao, k=1)
                        fits = [ind.fitness.values[0] for ind in top10]
                        fit_worst = [ind.fitness.values[0] for ind in worst]
                        teste = []
                        points = top10[0]
                        points_worst = worst[0]


                        # melhores globais
                        #se não for o inicio do loop e se as listas estiverem vazias eu atribuo os valores do banco
                        if i != 0:
                            if 'melhores_global' in db and not melhores_global:
                                melhores_global = db['melhores_global']
                            if 'worst_global' in db and not worst_global:
                                worst_global = db['worst_global']
                            if 'best_global' in db and not best_global:
                                best_global = db['best_global']
                            if 'points_global' in db and not points_global:
                                points_global = db['points_global']

                        melhores_global.append(max(fits))
                        worst_global.append([sum(points_worst), fit_worst[0]])
                        best_global.append([sum(points), fits[0]])
                        points_global.append(sum(points))

                        db['melhores_global'] = melhores_global
                        db['worst_global'] = worst_global
                        db['best_global'] = best_global
                        db['points_global'] = points_global

                        # print(worst_global)

                        # print(points, '\n', fits)
                        # print("numero de sensores implantados", sum(points))

                        for key, plo in enumerate(points):
                            if plo == 1:
                                teste.append(funcoes.get_pp()[key])

                        plotax = []
                        plotay = []
                        for t in teste:
                            plotax.append(t[0])
                            plotay.append(t[1])

                        alvosx = []
                        alvosy = []
                        for a in funcoes.get_alvos():
                            alvosx.append(a[0])
                            alvosy.append(a[1])

                        ppx = []
                        ppy = []
                        for p in funcoes.get_pp():
                            ppx.append(p[0])
                            ppy.append(p[1])

                        '''Cria o diretorio para salvar os testes realizados'''
                        directory = funcoes.create_directory(i, restricoes, pontos_potenciais, get_test_type(type)[1])

                        figura_inner = plt.figure()

                        # Demostra a posicao dos pontos
                        plt.plot(plotax, plotay, 'ro', ms=115, alpha=0.2, label="Raio de Detecção")
                        # plt.plot(plotax, plotay, 'yo', ms=100, alpha=0.1)
                        # plt.plot(plotax, plotay, 'ro')
                        plt.plot(alvosx, alvosy, 'bo', label="Alvos")
                        plt.plot(ppx, ppy, 'g^', label="Posições Potenciais")
                        plt.axis([0, 300, 0, 300])
                        plt.ylabel('Representacao do Melhor Individuo')
                        legenda = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                        ncol=3,  mode="expand", borderaxespad=0.)
                        for handle in legenda.legendHandles:
                            handle._legmarker.set_markersize(10)
                        path = directory + "/evolucao_" + str(i + 1) + ".png"
                        plt.savefig(path)
                        plt.close(figura_inner)
                        # plt.show()

                        # Cria uma nova instancia de figura para separar os plots
                        figura_inner_2 = plt.figure()

                        # Grafico de convergencia
                        converg = plt.plot(melhores, label="Convergência")
                        plt.ylabel('Grau de Precisao')
                        plt.xlabel('Numero de Geracoes')
                        plt.legend(handles=converg, loc=0)
                        path_converg = directory + "/convergencia_" + str(i + 1) + ".png"
                        plt.savefig(path_converg)
                        plt.close(figura_inner_2)

                        # Escrevendo informacoes da execucao
                        f = open(directory + '/info.txt', 'w')
                        f.write('Media Fits = ' + str(sum(melhores)/len(melhores)) + '\n' + 'Variancia = ' +
                                str(functions.np.var(points_inner)) + '\n' + 'Numero de Sensores implantados = ' +
                                str(sum(points)) + '\n' + 'Avaliacao do Melhor Individuo = ' +
                                str(max(fits)) + '\n' + 'Melhor individuo = ' + str(points))
                        f.close()

                        # Encerra o multithreading
                        # pool.close()

                    directory_global = get_test_type(type)[1] + str(restricoes) +\
                                       "/" + str(pontos_potenciais)

                    # Escrevendo informacoes da execucao global
                    f = open(directory_global + '/info_global.txt', 'w')
                    f.write('Media Fits = ' + str(sum(melhores_global)/len(melhores_global)) + '\n' + 'Variancia = ' +
                            str(functions.np.var(points_global)) + '\n' + 'Media de Sensores implantados = ' +
                            str(mean(points_global)) + '\n' + 'Melhor Fit das execucoes = ' +
                            str(max(melhores_global)) + '\n' + 'Menor quantidade de pontos selecionados = ' +
                            str(min(points_global)))
                    f.close()
                    del funcoes
                    #dependendo da condicao(type) adicionar no proposto ou artigo a media
                    #no for externo, tirar a media dos pontos adicionados e adicionar na tupla final
                    if type == 'artigo':
                        chart.add_temp_modificado(mean(points_global), functions.np.std(points_global))
                        chart.add_temp_modificado_best(max(best_global, key=lambda x: x[1]),
                                                       functions.np.std(best_global, axis=0))
                        chart.add_temp_modificado_worst(min(worst_global, key=lambda x: x[1]),
                                                        functions.np.std(worst_global, axis=0))
                    else:
                        chart.add_temp_proposto(mean(points_global), functions.np.std(points_global))
                        chart.add_temp_proposto_best(max(best_global, key=lambda x: x[1]),
                                                     functions.np.std(best_global, axis=0))
                        chart.add_temp_proposto_worst(min(worst_global, key=lambda x: x[1]),
                                                      functions.np.std(worst_global, axis=0))
                    db['chart'] = chart

                if type == 'artigo':
                    chart.add_modificado_means(mean(chart.get_temp_modificado()))
                    chart.add_modificado_std(mean(chart.get_temp_modificado_std()))
                    chart.add_modificado_best(max(chart.get_temp_modificado_best(), key=lambda x: x[1])[0])
                    chart.add_modificado_best_std(functions.np.max(chart.get_temp_modificado_best_std(), axis=0)[0])
                    chart.add_modificado_worst(min(chart.get_temp_modificado_worst(), key=lambda x: [1])[0])
                    chart.add_modificado_worst_std(functions.np.min(chart.get_temp_modificado_worst_std(), axis=0)[0])
                else:
                    chart.add_proposto_means(mean(chart.get_temp_propost()))
                    chart.add_proposto_std(mean(chart.get_temp_proposto_std()))
                    chart.add_proposto_best(max(chart.get_temp_proposto_best(), key=lambda x: x[1])[0])
                    chart.add_proposto_best_std(functions.np.max(chart.get_temp_proposto_best_std(), axis=0)[0])
                    chart.add_proposto_worst(min(chart.get_temp_proposto_worst(), key=lambda x: [1])[0])
                    chart.add_proposto_worst_std(functions.np.min(chart.get_temp_proposto_worst_std(), axis=0)[0])

                db['chart'] = chart

        chart.start_chart("/home/matheus/Documentos/Projeto_de_Graduacao", "/chart_media.png", 1)
        chart.start_chart("/home/matheus/Documentos/Projeto_de_Graduacao", "/chart_melhor.png", 2)
        chart.start_chart("/home/matheus/Documentos/Projeto_de_Graduacao", "/chart_pior.png", 3)
        db['chart'] = chart



    #Voronoi
    # vor = Voronoi(points_random.alvos1)
    #
    # voronoi_plot_2d(vor)
    #
    #
    # path = directory + "/evolucao_" + str(i+1) + ".png"
    # plt.savefig(path)

    # plt.show()
