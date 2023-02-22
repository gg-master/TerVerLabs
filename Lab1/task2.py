import os
import sympy as sp
from math import factorial
from functools import reduce


n, k, m = sp.symbols("n k m")


def formula_print(name, expr):
    formula = sp.pretty(expr).split("\n")
    k = len(formula) // 2
    for i in range(len(formula)):
        if i != k:
            formula[i] = " " * len(name) + formula[i]
        else:
            formula[i] = name + formula[i]
    return "\n".join(formula)


TASK_1_TEXT = """
1. В партии, состоящей из k изделий, имеется l дефектных. 
Из партии выбирается для контроля r изделий.
Найти вероятность того, что из них S изделий будут дефектными.
"""

COMB_FORMULA = formula_print(
    "C(n, k) = ",
    sp.factorial(n) / (sp.factorial(n - k) * sp.factorial(k))
)

TASK_1_PROB_FORMULA = "P(A) = (C(S, l) * C(r - S, k - l)) / C(r, k)"

TASK_2_TEXT = """
2. В отделение связи поступило m телеграмм, которые случайным образом
распределяются по n каналом связи. Каналы перенумерованы. Найти вероятность
того, что на 1-ый канал попадет ровно k1 телеграмм, на 2-ой канал – k2 телеграмм,
…, на n-ый канал – kn телеграмм, причем k1 + k2 + ... + kn = m
"""

PERMUTATION_WITH_REP_FORMULA = "Pm(k1, k2, ..., kn) = m! / (k1! * k2! * ... * kn!)"

PLACEMENT_WITH_REP_FORMULA = formula_print(
    "~A(n, m) = ", n**k
)

TASK_2_PROB_FORMULA = "P(A) = Pm(k1, k2, ..., kn) / ~A(n, m)" 


def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def int_input(name, prompt, min_number=float("inf"), max_number=float("inf")):
    number = input(prompt).strip()
    if number.isdigit():
        number = int(number)
        if number < min_number:
            raise ValueError(f"Значение {name} должно быть не меньше {min_number}")
        if number > max_number:
            raise ValueError(f"Значение {name} должно быть меньше {max_number}")
    else:
        raise ValueError(f"Значение {name} введено неверно")
    return number


def permutation_with_rep(*k):
    kp = reduce(lambda x, y: x * y, map(factorial, k))
    return factorial(sum(k)) / kp


def placement_with_rep(k, n):
    return n ** k


def combinations_without_rep(k, n):
    return factorial(n) / (factorial(n - k) * factorial(k))


def task_solve(number):
    clear_screen()
    print("Текст задачи:")
    TASK_TEXT = TASK_1_TEXT if number == 1 else TASK_2_TEXT
    print(TASK_TEXT)
    print("Используемые формулы: ")
    if number == 1:
        print(COMB_FORMULA, end='\n\n')
        print(TASK_1_PROB_FORMULA, end='\n\n')
    else:
        print(PERMUTATION_WITH_REP_FORMULA, end='\n\n')
        print(PLACEMENT_WITH_REP_FORMULA, end="\n\n")
        print(TASK_2_PROB_FORMULA, end="\n\n")
    print("Введите параметры для решения задачи: ")
    try:
        if number == 1:
            k = int_input('k', "Количество изделий (допустимые значения: [2, 100]): k=", 2, 100)
            l = int_input('l', f"Количество дефектных изделий (допустимые значения: [1, {k}]): l=", 1, k)
            r = int_input('r', f"Количество выбранных для контроля изделий (допустимые значения: [1, {k}]): r=", 1, k)
            # По условию формулы сочетаний r - S <= k - l
            min_S = max(1, l + r - k)
            # Число выбранных дефектных не может превышать число всех выбранных или число всех дефектных
            max_S = min(r, l)
            S = int_input('S', f"Ожидаемое количество дефектных изделий (допустимые значения: [{min_S}, {max_S}]): S=", min_S, max_S)
            print("\n")
            P = (combinations_without_rep(S, l) * combinations_without_rep(r - S, k - l)) / combinations_without_rep(r, k)
            print(f"Вычисленная вероятность того, что из {r} изделий {S} будут дефектными: P(A) =", round(P, 12))
        else:
            n = int_input('n', "Введите количество каналов связи (допустимые значения: [1, 100]): n=", 1, 100)
            k = []
            for i in range(n):
                k.append(int_input(
                    f"k{i + 1}", 
                    f"Количество телеграмм на канале связи {i + 1} (допустимые значения: [0, 100]) k{i + 1}=",
                    0, 100))
            m = sum(k)
            P = permutation_with_rep(*k) / placement_with_rep(m, n)
            print("Вычисленная вероятность: P(A) =", round(P, 12))
    except ValueError as e:
        print(str(e))
        return


def main():
    clear_screen()
    print("Задачи: ")
    print(TASK_1_TEXT)
    print(TASK_2_TEXT)
    try:
        number = int_input("", "Выберите тип решаемой задачи: ", 1, 2)
        number = int(number)
        task_solve(number)
    except ValueError:
        print("Тип задачи введен неверно")
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
