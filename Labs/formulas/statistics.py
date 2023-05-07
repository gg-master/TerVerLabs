from collections import Counter
from math import sqrt
from dataclasses import dataclass
from typing import Dict


@dataclass
class DiscreteData:
    X: Dict[float, int]
    x_n: Dict[float, int]
    x_w: Dict[float, float]
    N: int
    x_v: float
    sigma: float
    D_v: float
    S: float


def process_discrete_data(data):
    counter = Counter(data)
    # Частота
    x_n = {}
    for key in sorted(counter.keys()):
        x_n[key] = counter[key]
    sum_n = sum(x_n.values())
    # Относительная частота
    x_w = {}
    for key in sorted(counter.keys()):
        x_w[key] = counter[key] / sum_n
    # Среднее выборочное
    Xv = 0
    for xi in x_n:
        Xv += x_n[xi] * xi
    Xv /= sum_n
    # Выборочная дисперсия
    Dv = 0
    for xi in x_n:
        Dv += (xi - Xv)**2 * x_n[xi]
    Dv /= sum_n
    # Среднее квадратическое отклонение
    sigma = sqrt(Dv)
    # Исправленное среднее квадратическое отклонение
    S = 0
    for xi in x_n:
        S += (xi - Xv)**2 * x_n[xi]
    S /= sum_n - 1
    S = sqrt(S)
    return DiscreteData(list(x_n.keys()), x_n, x_w, sum_n, Xv, sigma, Dv, S)


def process_discrete_plot_data(discrete_data: DiscreteData):
    # Эмпирическая функция
    f = {'lines': [], 'dotsx': [], 'dotsy': []}
    plot_data = {}
    k = len(discrete_data.X)
    
    func = '0,\tпри x < ' + str(discrete_data.X[0]) + '\n'

    intlen = 3 * (discrete_data.X[1] - discrete_data.X[0])
    line = [[discrete_data.X[0] - intlen, discrete_data.X[0]], [0, 0]]
    f['lines'].append(line)

    counter = list(discrete_data.x_w.values())[0]
    for i in range(1, k):
        newstr = ''
        newstr += str(round(counter, 2)) + ',\tпри ' + str(discrete_data.X[i - 1]) + ' <= x < ' + str(discrete_data.X[i])

        line = [[discrete_data.X[i - 1], discrete_data.X[i]], [counter, counter]]
        f['lines'].append(line)

        f['dotsx'].append(discrete_data.X[i-1])
        f['dotsy'].append(counter)

        counter += list(discrete_data.x_w.values())[i]
        func += newstr + '\n'

    func += '1,\tпри x >= ' + str(discrete_data.X[k - 1])
    line = [[discrete_data.X[k - 1],discrete_data.X[k - 1] + intlen], [counter, counter]]
    f['lines'].append(line)

    f['dotsx'].append(discrete_data.X[k - 1])
    f['dotsy'].append(counter)

    plot_data['F*'] = func
    plot_data['func'] = f

    return plot_data