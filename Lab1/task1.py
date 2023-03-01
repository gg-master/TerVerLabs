from formulas import (
    CombinationsWithoutRep,
    PlacementWithRep,
    PermutationWithoutRep,
    CombinationsWithRep,
    formula_print,
)

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
            formula = CombinationsWithoutRep(*map(int, input(text).split()))
        elif type_f == "A~":
            formula = PlacementWithRep(*map(int, input(text).split()))
        elif type_f == "P":
            formula = PermutationWithoutRep(
                int(input("Введите число n.\nОграничения 0 <= n <= 100\n"))
            )
        elif type_f == "C~":
            formula = CombinationsWithRep(*map(int, input(text).split()))
        else:
            exit("Тип формулы указан неверно!")
    except ValueError as e:
        exit(e)

    print(
        f"Используемая формула для \"{formula.name}\":\n "
        f"{formula_print(formula.notation, formula.sympy_f)}"
    )
    print(f"Результат: {formula.result}")
