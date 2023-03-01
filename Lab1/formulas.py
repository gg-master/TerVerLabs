from abc import ABC
from math import factorial as m_factorial
from typing import Union, List
from functools import reduce
from sympy import symbols, pretty
from sympy import factorial as sp_factorial
from sympy.core.expr import Expr


MIN_VAL = 0
MAX_VAL = 100

SP_N, SP_K, SP_M = symbols("n k m")


class Formula(ABC):
    name: str
    notation: str
    sympy_f: Expr
    result: Union[int, float]

    def __init__(self, *args):
        if not all(
            [MIN_VAL <= val <= MAX_VAL for val in args if isinstance(val, int)]
        ):
            raise ValueError(
                "Один из аргументов указан в неправильном диапазоне!"
            )


class CombinationsWithoutRep(Formula):
    name = "Сочетание без повторений"
    notation = "C(n; k) = "
    sympy_f = sp_factorial(SP_N) / (
        sp_factorial(SP_N - SP_K) * sp_factorial(SP_K)
    )

    def __init__(self, k: int, n: int):
        super().__init__(k, n)
        # сhecking the condition for a specific formula
        if n < k:
            raise ValueError("Число n должно быть больше числа k!")

        self.result = m_factorial(n) // (m_factorial(n - k) * m_factorial(k))


class CombinationsWithRep(CombinationsWithoutRep):
    name = "Сочетание с повторениями"
    notation = "C~(n; k) = C(n + k - 1; k) = "

    def __init__(self, k: int, n: int):
        super().__init__(k, n + k - 1)


class PlacementWithRep(Formula):
    name = "Размещение с повторениями"
    notation = "A~(n; k) = "
    sympy_f = SP_N**SP_K

    def __init__(self, k: int, n: int):
        super().__init__(k, n)
        self.result = n**k


class PermutationWithoutRep(Formula):
    name = "Перестановка"
    notation = "P(n) = "
    sympy_f = sp_factorial(SP_N)

    def __init__(self, n: int):
        super().__init__(n)
        self.result = m_factorial(n)


class PermutationWithRep(Formula):
    name = "Перестановка c повторениями"
    notation = "Pm(k1, k2, ..., kn) = "
    sympy_f = Expr()

    def __init__(self, *k: List[int]):
        super().__init__(k)
        self.result = m_factorial(sum(k)) // reduce(
            lambda x, y: x * y, map(m_factorial, k)
        )


def formula_print(name, expr) -> str:
    formula = pretty(expr).split("\n")
    k = len(formula) // 2
    for i in range(len(formula)):
        if i != k:
            formula[i] = " " * len(name) + formula[i]
        else:
            formula[i] = name + formula[i]
    return "\n".join(formula)
