from formulas import (
    combinations_without_rep,
    placement_with_rep,
    permutation_without_rep,
    combinations_with_rep,
    formula_print
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