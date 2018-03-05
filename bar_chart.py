"""
========
Barchart
========

A bar plot with errorbars and height labels on individual bars
"""
import numpy as np
import matplotlib.pyplot as plt

N = 9
proposto_means = (18, 18, 20, 27, 26.6, 26.6, 39.6, 39.4, 38.6)
proposto_std = (2, 3, 4, 1, 2, 4, 1, 3, 5)

ind = np.arange(N)  # the x locations for the groups
width = 0.25       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, proposto_means, width, color='r', yerr=proposto_std)

gupta_means = (18.6, 18.8, 21.8, 32.4, 31.8, 32.4, 42.4, 44.8, 43.4)
gupta_std = (3, 5, 2, 3, 3, 4, 3, 2, 5)
rects2 = ax.bar(ind + width, gupta_means, width, color='y', yerr=gupta_std)


modificado_means = (21, 22, 26, 27, 29, 33, 35, 39, 45)
modificado_std = (3, 1, 5, 3, 4, 1, 5, 3, 2)
rects3 = ax.bar(ind+(2*width), modificado_means, width, color='b', yerr=modificado_std)

# add some text for labels, title and axes ticks
ax.set_ylabel('Número de Posições Potenciais Selecionadas')
ax.set_title('Comparação em Termos de Posições Potenciais Selecionadas')
ax.set_xticks(ind + width)
ax.set_xticklabels(('(1, 1)', '(1, 2)', '(1, 3)', '(2, 1)', '(2, 2)', '(2, 3)', '(3, 1)', '(3, 2)', '(3, 3)'))

ax.legend((rects1[0], rects2[0], rects3[0]), ('Proposto(Modificado)', 'Gupta(Implementado)', 'Gupta(Artigo)'))

plt.yticks(np.arange(0, 51, 10))


def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom')


autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

plt.show()
