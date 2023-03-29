from widgets import TaskView

from functools import partial
from tasks.lab2_task1_2 import Lab2_Task1_2
from tasks.lab2_tast3 import Lab2Task3
from tasks.lab_task4 import Lab2Task4
from tasks.lab3_task2 import Lab3Task2


labs = {
    2: [
        partial(Lab2_Task1_2, 1),
        partial(Lab2_Task1_2, 2),
        partial(Lab2Task3, 3),
        partial(Lab2Task4, 4)
    ],
    3: [
        Lab3Task2
    ]
}

lab_names = {
    2: "Теоремы сложения и умножения вероятностей. Формула полной вероятности и Байеса",
    3: "Формула Бернулли. Полиномиальная формула. Предельные теоремы в схеме Бернулли"
}