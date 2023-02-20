import abc
from math import factorial
import sympy as sp

n, k = sp.symbols("n k")

class Formula(abc.ABC):
    MIN = 0
    MAX = 100
    
    formula = None
    sympy_f = None
    name = None

    def __init__(self, k, n):
        self.k, self.n = k, n

        if not(self.MIN <= self.k <= self.MAX):
            raise ValueError("Число k указано в неправильном диапазоне.")
        elif not(self.MIN <= self.n <= self.MAX):
            raise ValueError("Число n указано в неправильном диапазоне.")

    @abc.abstractmethod
    def calculate(self):
        raise NotImplementedError


class CombinationWithoutRep(Formula):
    name = "Сочетание без повторений"
    formula = "C(n; k) = "
    # n! / ((n - k)! * k!)
    sympy_f = sp.factorial(n) / (sp.factorial(n - k) * sp.factorial(k))

    def __init__(self, k, n):
        super().__init__(k, n)

        if self.n < self.k:
            raise ValueError("Число n должно быть больше числа k!")

    def calculate(self):
        return (factorial(self.n)) // ( factorial(self.n - self.k) \
                                       * factorial(self.k))


class CombinationWithRep(CombinationWithoutRep):
    name = "Сочетание с повторениями"
    formula = "C~(n; k) = C(n + k - 1; k) = "

    # n! / ((n - k)! * k!)
    def __init__(self, k, n):
        super().__init__(k, n + k - 1)
       

class PlacementWithRep(Formula):
    name = "Размещение с повторениями"
    formula = "A~(n; k) = "
    sympy_f = n ** k
    # n^k 
    def calculate(self):
        return self.n ** self.k
    

class Permutation(Formula):
    name = "Перестановка"
    formula = "P(n) = "
    # n!
    sympy_f = sp.factorial(n)

    def __init__(self, n):
        super().__init__(0, n)
    
    def calculate(self):
        return factorial(self.n)


def formula_print(name, expr):
    formula = sp.pretty(expr).split("\n")
    if len(formula) % 2 != 0:
        k = len(formula) // 2
    else:
        k = len(formula) - 1
    for i in range(len(formula)):
        if i != k:
            formula[i] = " " * len(name) + formula[i]
        else:
            formula[i] = name + formula[i]
    return "\n".join(formula)


if __name__ == "__main__":
    # C, A, P, C~, A~, P~
    type_f = input("Введите тип формулы. "
                   "Доступные: C (Сочетание без повторений), "
                   "P (Перестановка), "
                   "A~ (Размещение с повторениями), "
                   "C~ (сочетание с повторениями)\n")
        
    text = "Введите числа n и k через пробел. \
            \nОграничения 0 <= n <= 100; 0 <= k <= 100;\n"
    try:
        if type_f == "C":
            n, k = map(int, input(text).split())
            formula = CombinationWithoutRep(k, n)
        elif type_f == "A~":
            n, k = map(int, input(text).split())
            formula = PlacementWithRep(k, n)
        elif type_f == "P":
            n = int(input("Введите число n.\nОграничения 0 <= n <= 100\n"))
            formula = Permutation(n)
        elif type_f == "C~":
            n, k = map(int, input(text).split())
            formula = CombinationWithRep(k, n)
        else:
            exit("Тип формулы указан неверно!")
    except ValueError as e:
        exit(e)

    print(f"Используемая формула для \"{formula.name}\":\n "
          f"{formula_print(formula.formula, formula.sympy_f)}")
    print(f"Результат: {formula.calculate()}")
