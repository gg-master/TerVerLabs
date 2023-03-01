from math import factorial as m_factorial
from typing import Union, Optional
from dataclasses import dataclass
from sympy import symbols, pretty
from sympy import factorial as sp_factorial
from sympy.core.expr import Expr
from functools import reduce


MIN_VAL = 0
MAX_VAL = 100

SP_N, SP_K, SP_M = symbols("n k m")


@dataclass
class Formula:
    name: str
    notation: str
    sympy_f: Expr
    result: Union[int, float]


def global_args_validator(func):
    """
    checking that all arguments are int and in the range [0, 100]
    """

    def wrapper(*args):
        if not all(
            [MIN_VAL <= val <= MAX_VAL for val in args if isinstance(val, int)]
        ):
            raise ValueError(
                "Один из аргументов указан в неправильном диапазоне!"
            )
        return func(*args)

    return wrapper


@global_args_validator
def combinations_without_rep(k: int, n: int) -> Formula:
    # сhecking the condition for a specific formula
    if n < k:
        raise ValueError("Число n должно быть больше числа k!")

    result = (m_factorial(n)) / (m_factorial(n - k) * m_factorial(k))
    return Formula(
        "Сочетание без повторений",
        "C(n; k) = ",
        sp_factorial(SP_N) / (sp_factorial(SP_N - SP_K) * sp_factorial(SP_K)),
        result,
    )


@global_args_validator
def combinations_with_rep(k: int, n: int) -> Formula:
    f_result: Formula = combinations_without_rep(k, n + k - 1)
    return Formula(
        "Сочетание с повторениями",
        "C~(n; k) = C(n + k - 1; k) = ",
        f_result.sympy_f,
        f_result.result,
    )


@global_args_validator
def placement_with_rep(k: int, n: int) -> Formula:
    return Formula(
        "Размещение с повторениями",
        "A~(n; k) = ",
        SP_N**SP_K,
        result=n**k,
    )


@global_args_validator
def permutation_without_rep(n: int) -> Formula:
    return Formula(
        "Перестановка",
        "P(n) = ",
        sp_factorial(SP_N),
        result=m_factorial(n),
    )


@global_args_validator
def permutation_with_rep(*k) -> Formula:
    result = m_factorial(sum(k)) / reduce(lambda x, y: x * y, map(m_factorial, k))
    return Formula(
        "Перестановка c повторениями",
        "Pm(k1, k2, ..., kn) = ",
        Expr(),
        result,
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


if __name__ == "__main__":
    type_f = input(
        "Введите тип формулы. "
        "Доступные: C (Сочетание без повторений), "
        "P (Перестановка), "
        "A~ (Размещение с повторениями), "
        "C~ (сочетание с повторениями)\n"
    )

    text = "Введите числа k и n через пробел. \
            \nОграничения 0 <= k <= 100; 0 <= n <= 100;\n"
    try:
        if type_f == "C":
            formula = combinations_without_rep(*map(int, input(text).split()))
        elif type_f == "A~":
            formula = placement_with_rep(*map(int, input(text).split()))
        elif type_f == "P":
            formula = permutation_without_rep(
                int(input("Введите число n.\nОграничения 0 <= n <= 100\n"))
            )
        elif type_f == "C~":
            formula = combinations_with_rep(*map(int, input(text).split()))
        else:
            exit("Тип формулы указан неверно!")
    except ValueError as e:
        exit(e)

    print(
        f"Используемая формула для \"{formula.name}\":\n "
        f"{formula_print(formula.notation, formula.sympy_f)}"
    )
    print(f"Результат: {formula.result}")
