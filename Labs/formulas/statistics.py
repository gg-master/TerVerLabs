from collections import Counter
from math import sqrt
from dataclasses import dataclass
from typing import Dict, List


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


@dataclass
class ContinuousData:
    intervals: List[List[float]]
    N: list[int]
    W: list[float]
    middles: list[float]
    x_v: float
    sigma: float
    D_v: float
    S: float


def process_discrete_data(data) -> DiscreteData:
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


def process_continuous_data(data):
    h = max(data) - min(data) // len(data)
    xmax = max(data)
    sorted_uniq_data = list(sorted(set(data)))
    intervals = []
    middles = []
    N = []
    W = []
    #Интервалы и их середины
    for number in sorted_uniq_data:
        intervals.append([number, min(number + h, xmax)])
        middles.append(round((min(number + h, xmax) - number) / 2, 2))
    # Частота для интервалов
    for interval in intervals:
        N.append(data.count(interval[0]))
    Nsum = sum(N)
    assert len(data) == Nsum
    # Относительная частота для интервалов
    for ni in N:
        W.append(ni / Nsum)
    # Среднее выборочное
    Xv = 0
    for i, xi in enumerate(middles):
        Xv += xi * N[i]
    Xv /= Nsum
    # Выборочная дисперсия
    Dv = 0
    for i, xi in enumerate(middles):
        Dv += (xi - Xv)**2 * N[i]
    Dv /= Nsum
    # Среднее квадратическое отклонение
    sigma = sqrt(Dv)
    # Исправленное среднее квадратическое отклонение
    S = 0
    for i, xi in enumerate(middles):
        S += (xi - Xv)**2 * N[i]
    S /= Nsum - 1
    S = sqrt(S)
    return ContinuousData(intervals, N, W, middles, Xv, sigma, Dv, S)
    

def process_continuous_plot_data(data: ContinuousData):
    plot_data = {}
    k = len(data.intervals)
    f = {'lines': [], 'dotsx': [], 'dotsy': []}
    func = '0,\tпри x <= ' + str(round(data.intervals[0][1], 3)) + '\n'

    intlen = 3 * (data.intervals[0][1] - data.intervals[0][0])
    line = [[data.intervals[1] - intlen, data.intervals[0][1]], [0, 0]]
    f['lines'].append(line)

    counter = data.W[0]
    for i in range(1, k):
        newstr = ''
        newstr += str(round(counter, 2)) + ',\tпри ' + str(round(data.intervals[i - 1][1], 3)) + ' < x <= '\
                                                         + str(round(data.intervals[i][1], 3))
        line = [[data.intervals[i][1], data.intervals[i][0]], [counter, counter]]
        f['lines'].append(line)

        f['dotsx'].append(data.intervals[i - 1][1])
        f['dotsy'].append(counter)

        counter += data.W[i]
        func += newstr + '\n'
    func += '1,\tпри x > ' + str(round(data.intervals[k - 1][1], 3))

    line = [[data.intervals[k - 1][1], data.intervals[k - 1][1] + intlen], [counter, counter]]
    f['lines'].append(line)

    f['dotsx'].append(data.intervals[k - 1][1])
    f['dotsy'].append(counter)

    plot_data['F*'] = func
    plot_data['func'] = f

    return plot_data


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