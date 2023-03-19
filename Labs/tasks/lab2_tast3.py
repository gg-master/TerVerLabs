import os
import sys
from widgets import TaskView
from utils.paths import resolve_path
from PyQt5 import uic


sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    )
)
from Lab1.formulas import CombinationsWithoutRep


class Lab2Task3(TaskView):
    def __init__(self, task_number: int, parent):
        super().__init__(parent)
        self._task_number: int = task_number
        uic.loadUi(resolve_path('ui/lab2_task3.ui'), self)
        self._init_ui()
        self.on_spinbox_input()
    
    def _init_ui(self):
        for sb in [
            self.n_val_a, self.n_val_b, self.n_val_c, self.n_val_d,
            self.m1_val_a, self.m1_val_b, self.m1_val_c, self.m1_val_d,
            self.m2_val_a, self.m2_val_b, self.m2_val_c, self.m2_val_d,  
        ]:
            sb.valueChanged.connect(self.on_spinbox_input)
        self.tabWidget.currentChanged.connect(self.on_spinbox_input)

    def task_name(self):
        return f"{self._task_number}. Отыскание вероятнотей заданных сложных событий."

    def on_spinbox_input(self, *args):
        if self.tabWidget.currentIndex() == 0:
            self.compute_A()
        elif self.tabWidget.currentIndex() == 1:
            self.compute_B()
        elif self.tabWidget.currentIndex() == 2:
            self.compute_C()
        elif self.tabWidget.currentIndex() == 3:
            self.compute_D()

    def compute_A(self):
        n = self.n_val_a.value()
        self.m1_val_a.setMaximum(n)
        self.m2_val_a.setMaximum(n)

        m1 = self.m1_val_a.value()
        m2 = self.m2_val_a.value()

        c3m1 = CombinationsWithoutRep(3, m1).result
        c3m2 = CombinationsWithoutRep(3, m2).result
        c3n = CombinationsWithoutRep(3, n).result

        res = (c3m1 * c3m2) / (c3n ** 2)

        self.C3m1_a_result.setText(str(round(c3m1, 12)))
        self.C3m2_a_result.setText(str(round(c3m2, 12)))
        self.C3n_a_result.setText(str(round(c3n, 12)))
        self.Pa_result.setText(str(round(res, 12)))

    def compute_B(self):
        n = self.n_val_b.value()
        self.m1_val_b.setMaximum(n)
        self.m2_val_b.setMaximum(n)

        m1 = self.m1_val_b.value()
        m2 = self.m2_val_b.value()

        c3m1 = CombinationsWithoutRep(3, m1).result
        c3m2 = CombinationsWithoutRep(3, m2).result
        c3n = CombinationsWithoutRep(3, n).result

        res = (c3m1 / c3n) * (1 - (c3m2 / c3n))

        self.C3m1_b_result.setText(str(round(c3m1, 12)))
        self.C3m2_b_result.setText(str(round(c3m2, 12)))
        self.C3n_b_result.setText(str(round(c3n, 12)))
        self.Pb_result.setText(str(round(res, 12)))

    def compute_C(self):
        n = self.n_val_c.value()
        self.m1_val_c.setMaximum(n)
        self.m2_val_c.setMaximum(n)

        m1 = self.m1_val_c.value()
        m2 = self.m2_val_c.value()

        c3m1 = CombinationsWithoutRep(3, m1).result
        c3m2 = CombinationsWithoutRep(3, m2).result
        c3n = CombinationsWithoutRep(3, n).result

        res = ((c3m1 / c3n) * (1 - (c3m2 / c3n))) + ((c3m2 / c3n) * (1 - (c3m1 / c3n)))

        self.C3m1_c_result.setText(str(round(c3m1, 12)))
        self.C3m2_c_result.setText(str(round(c3m2, 12)))
        self.C3n_c_result.setText(str(round(c3n, 12)))
        self.Pc_result.setText(str(round(res, 12)))

    def compute_D(self):
        n = self.n_val_d.value()
        max_val = max(0, n - 3)
        self.m1_val_d.setMaximum(max_val)
        self.m2_val_d.setMaximum(max_val)

        m1 = self.m1_val_d.value()
        m2 = self.m2_val_d.value()

        c3m1 = CombinationsWithoutRep(3, n - m1).result
        c3m2 = CombinationsWithoutRep(3, n - m2).result
        c3n = CombinationsWithoutRep(3, n).result

        res = 1 - ((c3m1 * c3m2) / c3n**2)

        self.C3nm1_d_result.setText(str(round(c3m1, 12)))
        self.C3nm2_d_result.setText(str(round(c3m2, 12)))
        self.C3n_d_result.setText(str(round(c3n, 12)))
        self.Pd_result.setText(str(round(res, 12)))
