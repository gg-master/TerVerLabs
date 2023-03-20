from widgets import TaskView

from functools import partial
from tasks.lab2_task1_2 import Lab2_Task1_2
from tasks.lab2_tast3 import Lab2Task3
from tasks.lab_task4 import Lab2Task4


labs = {
    2: [
        partial(Lab2_Task1_2, 1),
        partial(Lab2_Task1_2, 2),
        partial(Lab2Task3, 3),
        partial(Lab2Task4, 4)
    ],
}

lab_names = {
    2: "Теоремы сложения и умножения вероятностей. Формула полной вероятности и Байеса"
}