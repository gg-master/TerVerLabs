from typing import List
from widgets import TaskView
from utils.paths import resolve_path
from PyQt5 import uic

from formulas.combinatorics import combinations_without_rep as C

class Lab2Task3(TaskView):
    def __init__(self, task_number: int, parent):
        super().__init__(parent)
        self._task_number: int = task_number
        uic.loadUi(resolve_path('ui/lab2_task3.ui'), self)
        self._init_ui()
        self.on_spinbox_input()

    def _init_ui(self):
        for sb in [
            self.n_val,
            self.m1_val,
            self.m2_val,
        ]:
            sb.valueChanged.connect(self.on_spinbox_input)
        self.tabWidget.currentChanged.connect(self.on_spinbox_input)

    def task_name(self):
        return f"{self._task_number}. Отыскание вероятноcтей заданных сложных событий"

    def on_spinbox_input(self, *args):
        n = self.n_val.value()
        self.m1_val.setMaximum(n)
        self.m2_val.setMaximum(n)
        self.m1_val.setMinimum(3)
        self.m2_val.setMinimum(3)
        if self.tabWidget.currentIndex() == 0:
            self.compute_A()
        elif self.tabWidget.currentIndex() == 1:
            self.compute_B()
        elif self.tabWidget.currentIndex() == 2:
            self.compute_C()
        elif self.tabWidget.currentIndex() == 3:
            self.compute_D()

    def compute_A(self) -> List[float]:
        n = self.n_val.value()
        m1 = self.m1_val.value()
        m2 = self.m2_val.value()

        c3m1 = C(3, m1)
        c3m2 = C(3, m2)
        c3n = C(3, n)

        pa1 = c3m1 / c3n
        pa2 = c3m2 / c3n
        res = pa1 * pa2

        self.Pa1_result.setText(str(round(pa1, 12)))
        self.Pa2_result.setText(str(round(pa2, 12)))

        self.C3m1_a_result.setText(str(round(c3m1, 12)))
        self.C3m2_a_result.setText(str(round(c3m2, 12)))
        self.C3n_a_result.setText(str(round(c3n, 12)))
        self.Pa_result.setText(str(round(res, 12)))
        return [res, pa1, pa2, c3m1, c3m2, c3n]

    def compute_B(self) -> List[float]:
        n = self.n_val.value()
        m1 = self.m1_val.value()
        m2 = self.m2_val.value()

        c3m1 = C(3, m1)
        c3m2 = C(3, m2)
        c3n = C(3, n)

        pb1 = c3m1 / c3n
        pb2 = 1 - (c3m2 / c3n)
        res = pb1 * pb2

        self.Pb1_result.setText(str(round(pb1, 12)))
        self.Pb2_result.setText(str(round(pb2, 12)))

        self.C3m1_b_result.setText(str(round(c3m1, 12)))
        self.C3m2_b_result.setText(str(round(c3m2, 12)))
        self.C3n_b_result.setText(str(round(c3n, 12)))
        self.Pb_result.setText(str(round(res, 12)))
        return [res, pb1, pb2, c3m1, c3m2, c3n]

    def compute_C(self) -> List[float]:
        n = self.n_val.value()
        m1 = self.m1_val.value()
        m2 = self.m2_val.value()

        c3m1 = C(3, m1)
        c3m2 = C(3, m2)
        c3n = C(3, n)

        res = ((c3m1 / c3n) * (1 - (c3m2 / c3n))) + (
            (c3m2 / c3n) * (1 - (c3m1 / c3n))
        )

        self.C3m1_c_result.setText(str(round(c3m1, 12)))
        self.C3m2_c_result.setText(str(round(c3m2, 12)))
        self.C3n_c_result.setText(str(round(c3n, 12)))
        self.Pc_result.setText(str(round(res, 12)))
        return [res, c3m1, c3m2, c3n]

    def compute_D(self) -> List[float]:
        (res_a, pa1, pa2, c3m1, c3m2, c3n) = self.compute_A()
        res_c = self.compute_C()[0]
        res = res_a + res_c

        self.Pa1_result_d.setText(str(round(pa1, 12)))
        self.Pa2_result_d.setText(str(round(pa2, 12)))
        self.Pa_result_d.setText(str(round(res_a, 12)))
        self.Pc_result_d.setText(str(round(res_c, 12)))
        self.C3m1_d_result.setText(str(round(c3m1, 12)))
        self.C3m2_d_result.setText(str(round(c3m2, 12)))
        self.C3n_d_result_2.setText(str(round(c3n, 12)))
        self.Pd_result.setText(str(round(res, 12)))
        return [res]
