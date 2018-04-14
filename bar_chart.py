"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt
import functions


class Chart(object):

    """Temporarias so pra nao sujar o arquivo gupta.py"""
    temp_proposto = ()
    temp_proposto_std = ()

    temp_proposto_best = ()
    temp_proposto_best_std = ()

    temp_proposto_worst = ()
    temp_proposto_worst_std = ()

    temp_modificado = ()
    temp_modificado_std = ()

    temp_modificado_best = ()
    temp_modificado_best_std = ()

    temp_modificado_worst = ()
    temp_modificado_worst_std = ()
    """"-----------------------------------------------"""

    N = 9
    ind = np.arange(N)  # a posicao de x para os grupos
    width = 0.25  # a largura das barras
    fig, ax = plt.subplots()

    '''-------------------------------------------------------------------'''
    # proposto_means = (18, 18, 20, 27, 26.6, 26.6, 39.6, 39.4, 38.6)
    # proposto_std = (2, 3, 4, 1, 2, 4, 1, 3, 5)
    proposto_means = ()
    proposto_std = ()

    '''-------------------------------------------------------------------'''
    proposto_best = ()
    proposto_best_std = ()

    '''-------------------------------------------------------------------'''
    proposto_worst = ()
    proposto_worst_std = ()

    gupta_means = (21, 22, 26, 27, 29, 33, 35, 39, 45)
    gupta_std = (3, 5, 2, 3, 3, 4, 3, 2, 5)

    # modificado_means = (18.6, 18.8, 21.8, 32.4, 31.8, 32.4, 42.4, 44.8, 43.4)
    # modificado_std = (3, 1, 5, 3, 4, 1, 5, 3, 2)
    modificado_means = ()
    modificado_std = ()

    '''-------------------------------------------------------------------'''
    modificado_best = ()
    modificado_best_std = ()

    '''-------------------------------------------------------------------'''
    modificado_worst = ()
    modificado_worst_std = ()


    # def __init__(self):


    def start_chart(self, path, title, type):


        rects1 = self.get_ax().bar(self.get_ind(), self.get_type(type)[0], self.get_width(), color='r',
                                   yerr=self.get_type(type)[1])
        rects2 = self.get_ax().bar(self.get_ind() + self.get_width(), self.get_type(type)[2], self.get_width(),
                                   color='y', yerr=self.get_type(type)[3])
        rects3 = self.get_ax().bar(self.get_ind() + (2*self.get_width()), self.get_gupta_means(), self.get_width(), color='b', yerr=self.get_gupta_std())

        # informacoes das labels
        self.get_ax().set_ylabel('Número de Posições Potenciais Selecionadas')
        self.get_ax().set_title('Comparação em Termos de Posições Potenciais Selecionadas')
        self.get_ax().set_xticks(self.get_ind() + self.get_width())
        self.get_ax().set_xticklabels(('(1, 1)', '(1, 2)', '(1, 3)', '(2, 1)', '(2, 2)', '(2, 3)', '(3, 1)', '(3, 2)', '(3, 3)'))

        self.get_ax().legend((rects1[0], rects2[0], rects3[0]), ('Proposto(Modificado)', 'Gupta(Implementado)', 'Gupta(Artigo)'))

        plt.yticks(np.arange(0, 51, 10))

        self.autolabel(rects1)
        self.autolabel(rects2)
        self.autolabel(rects3)

        plt.savefig(path + title)


    def autolabel(self, rects):
        """
        Attach a text label above each bar displaying its height
        """
        for rect in rects:
            height = rect.get_height()
            self.get_ax().text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    def get_type(self, argument):
        switcher = {
            1: [self.get_proposto_means(), self.get_proposto_std(), self.get_modificado_means(), self.get_modificado_std()],
            2: [self.get_proposto_best(), self.get_proposto_best_std(), self.get_modificado_best(), self.get_modificado_best_std()],
            3: [self.get_proposto_worst(), self.get_proposto_worst_std(), self.get_modificado_worst(), self.get_modificado_worst_std()],
        }
        return switcher.get(argument)


    # plt.show()


    def get_ax(self):
        return self.ax

    def get_ind(self):
        return self.ind

    def get_width(self):
        return self.width

    def get_fig(self):
        return self.fig

    def get_N(self):
        return self.N

    def get_proposto_means(self):
        return self.proposto_means

    def get_proposto_std(self):
        return self.proposto_std

    def get_gupta_means(self):
        return self.gupta_means

    def get_gupta_std(self):
        return self.gupta_std

    def get_modificado_means(self):
        return self.modificado_means

    def get_modificado_std(self):
        return self.modificado_std

    def get_proposto_best(self):
        return self.proposto_best

    def get_proposto_best_std(self):
        return self.proposto_best_std

    def get_modificado_best(self):
        return self.modificado_best

    def get_modificado_best_std(self):
        return self.modificado_best_std

    def get_proposto_worst(self):
        return self.proposto_worst

    def get_proposto_worst_std(self):
        return self.proposto_worst

    def get_modificado_worst(self):
        return self.modificado_worst

    def get_modificado_worst_std(self):
        return self.modificado_worst_std

    def get_temp_propost(self):
        return self.temp_proposto

    def get_temp_modificado(self):
        return self.temp_modificado

    def get_temp_modificado_std(self):
        return self.temp_modificado_std

    def get_temp_proposto_std(self):
        return self.temp_proposto_std

    def get_temp_proposto_best(self):
        return self.temp_proposto_best

    def get_temp_proposto_best_std(self):
        return self.temp_proposto_best_std

    def get_temp_modificado_best(self):
        return self.temp_modificado_best

    def get_temp_modificado_best_std(self):
        return self.temp_modificado_best_std

    def get_temp_proposto_worst(self):
        return self.temp_proposto_worst

    def get_temp_proposto_worst_std(self):
        return self.temp_proposto_worst_std

    def get_temp_modificado_worst(self):
        return self.temp_modificado_worst

    def get_temp_modificado_worst_std(self):
        return self.temp_modificado_worst_std

    def set_N(self, value):
        self.N = value

    def set_width(self, value):
        self.width = value

    def add_proposto_means(self, value):
        self.proposto_means = self.proposto_means + (value, )

    def add_proposto_std(self, value):
        self.proposto_std = self.proposto_std + (value, )

    def add_proposto_best(self, value):
        self.proposto_best = self.proposto_best + (value, )

    def add_proposto_best_std(self, value):
        self.proposto_best_std = self.proposto_best_std + (value, )

    def add_proposto_worst(self, value):
        self.proposto_worst = self.proposto_worst + (value, )

    def add_proposto_worst_std(self, value):
        self.proposto_worst_std = self.proposto_worst_std + (value, )

    def add_modificado_means(self, value):
        self.modificado_means = self.modificado_means + (value, )

    def add_modificado_std(self, value):
        self.modificado_std = self.modificado_std + (value, )

    def add_modificado_best(self, value):
        self.modificado_best = self.modificado_best + (value, )

    def add_modificado_best_std(self, value):
        self.modificado_best_std = self.modificado_best_std + (value, )

    def add_modificado_worst(self, value):
        self.modificado_best = self.modificado_best + (value, )

    def add_modificado_worst_std(self, value):
        self.modificado_worst_std = self.modificado_worst_std + (value, )

    def add_temp_proposto(self, value1, value2):
        self.temp_proposto = self.temp_proposto + (value1, )
        self.temp_proposto_std = self.temp_proposto_std + (value2, )

    def add_temp_proposto_best(self, value1, value2):
        self.temp_proposto_best = self.temp_proposto_best + (value1, )
        self.temp_proposto_best_std = self.temp_proposto_best_std + (value2, )

    def add_temp_proposto_worst(self, value1, value2):
        self.temp_proposto_worst = self.temp_proposto_worst + (value1, )
        self.temp_proposto_worst_std = self.temp_proposto_worst_std + (value2, )

    def add_temp_modificado(self, value1, value2):
        self.temp_modificado = self.temp_modificado + (value1, )
        self.temp_modificado_std = self.temp_modificado_std + (value2, )

    def add_temp_modificado_best(self, value1, value2):
        self.temp_modificado_best = self.temp_modificado_best + (value1, )
        self.temp_modificado_best_std = self.temp_modificado_best_std + (value2, )

    def add_temp_modificado_worst(self, value1, value2):
        self.temp_modificado_worst = self.temp_modificado_worst + (value1, )
        self.temp_modificado_worst_std = self.temp_modificado_worst_std + (value2, )

    def reset_temporaries(self):
        self.temp_proposto = ()
        self.temp_modificado = ()
        self.temp_proposto_best = ()
        self.temp_proposto_worst = ()
        self.temp_modificado_best = ()
        self.temp_modificado_worst = ()
        self.temp_proposto_std = ()
        self.temp_proposto_best_std = ()
        self.temp_modificado_worst_std = ()
        self.temp_modificado_best_std = ()
        self.temp_proposto_std = ()
        self.temp_proposto_worst_std = ()

# if __name__ == "__main__":
#
#     lista = ['arroz', 'feijao', 'batata', 'frango']
#     skip = 2
#     for i, value in enumerate(lista):
#         if i < skip:
#             continue
#         print(value)
#     teste = [[15, 0.9174193548387097], [15, 0.8911627906976745], [16, 0.984872387237858]]
#     print(functions.np.max(teste, axis=0)[0])
    # print(functions.np.std(teste, axis=0))
    # chart = Chart()
    # chart.add_proposto_means(33.5)
    # chart.add_proposto_means(20)
    # chart.add_proposto_means(10)
    # print(chart.get_proposto_means())
