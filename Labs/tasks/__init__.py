from widgets import TaskView

from functools import partial
from tasks.lab2_task1_2 import Lab2_Task1_2

labs = {
    2: [
        partial(Lab2_Task1_2, 1),
        partial(Lab2_Task1_2, 2),
    ],
}

lab_names = {
    2: "Теоремы сложения и умножения вероятностей. Формула полной вероятности и Байеса"
}