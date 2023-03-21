from math import sqrt, erf, pi
from formulas.combinatorics import combinations_without_rep as C, permutation_with_rep as _P
from typing import List


def bernoulli_formula(n: int, p: float, start: int, end: int=None) -> float:
    if end is not None:
        result = 0
        for i in range(start, end+1):
            result += bernoulli_formula(n, p, i)
        return result
    else:
        return C(start, n) * p**start * (1-p)**(n - start)


def polynomial_distribution(m: List[float], p: List[float]) -> float:
    assert len(m) == len(p), "Length of m and p must be equal"
    result = _P(*m) 
    for i in range(len(m)):
        result *= p[i]**m[i]
    return result


def moivre_laplace_integral_formula(m1: int, m2: int, p: float, n: int) -> float:
    q = 1 - p
    x1 = (m1 - n*p) / sqrt(n * p * q)
    x2 = (m2 - n*p) / sqrt(n * p * q)
    return laplace_function(x2) - laplace_function(x1)


def laplace_function(x) -> float:
    return (1 / sqrt(2 * pi)) * (sqrt(pi) * erf(x / sqrt(2)) / sqrt(2))