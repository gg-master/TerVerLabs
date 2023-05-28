from widgets import TaskView

from functools import partial
from tasks.lab2_task1_2 import Lab2_Task1_2
from tasks.lab2_tast3 import Lab2Task3
from tasks.lab2_task4 import Lab2Task4
from tasks.lab3_task2 import Lab3Task2
from tasks.lab3_task1 import Lab3Task1
from tasks.lab5_task1 import Lab5Task1
from tasks.lab5_task2 import Lab5Task2
from tasks.lab6_task1 import Lab6Task1
from tasks.lab6_task2 import Lab6Task2


labs = {
    2: [
        partial(Lab2_Task1_2, 1),
        partial(Lab2_Task1_2, 2),
        partial(Lab2Task3, 3),
        partial(Lab2Task4, 4)
    ],
    3: [
        partial(Lab3Task1, 1),
        partial(Lab3Task2, 2),
    ],
    5: [
        partial(Lab5Task1, 1),
        partial(Lab5Task2, 2)
    ],
    6: [
        partial(Lab6Task1, 1),
        partial(Lab6Task2, 2)
    ]
}

lab_names = {
    2: "Теоремы сложения и умножения вероятностей. Формула полной вероятности и Байеса",
    3: "Формула Бернулли. Полиномиальная формула. Предельные теоремы в схеме Бернулли",
    5: "Первичная обработка статистических данных",
    6: "Проверка гипотезы о виде закона распределения по критерию согласия Пирсона"
}