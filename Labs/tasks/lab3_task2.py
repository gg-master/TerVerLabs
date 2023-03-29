from widgets import TaskView
from utils.paths import resolve_path
from PyQt5 import uic

from math import sqrt

from formulas.probabilities import bernoulli_formula, moivre_laplace_integral_formula


class Lab3Task2(TaskView):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi(resolve_path('ui/lab3_task2.ui'), self)
        self.n_spinbox.valueChanged.connect(self.m_value_set)
        self.m1_spinbox.valueChanged.connect(self.m_value_set)
        self.m2_spinbox.valueChanged.connect(self.m_value_set)

        self.p_spinbox.valueChanged.connect(self.p_value_set)
        self.q_spinbox.valueChanged.connect(self.q_value_set)

        self.X1_prefix = "x<sub>1</sub> = "
        self.X2_prefix = "x<sub>2</sub> = "
        self.P_prefix = "P(m<sub>1</sub> ≤ X ≤ m<sub>2</sub>) = "
    
    def m_value_set(self):
        if self.m1_spinbox.value() > self.n_spinbox.value():
            self.m1_spinbox.blockSignals(True)
            self.m1_spinbox.setValue(self.n_spinbox.value())
            self.m1_spinbox.blockSignals(False)
        self.m2_spinbox.setRange(self.m1_spinbox.value(), self.n_spinbox.value())
        self.m1_spinbox.setRange(0, self.m2_spinbox.value())
        self.calculate_all()

    def p_value_set(self):
        self.q_spinbox.blockSignals(True)
        self.q_spinbox.setValue(round(1 - round(self.p_spinbox.value(), 3), 3))
        self.q_spinbox.blockSignals(False)
        self.calculate_all()

    def q_value_set(self):
        self.p_spinbox.blockSignals(True)
        self.p_spinbox.setValue(round(1 - round(self.q_spinbox.value(), 3), 3))
        self.p_spinbox.blockSignals(False)
        self.calculate_all()

    def calculate_all(self):
        n, p = self.n_spinbox.value(), self.p_spinbox.value()
        m1, m2 = self.m1_spinbox.value(), self.m2_spinbox.value()
        q = 1 - p
        print(n, p, m1, m2, q)
        Pbern = bernoulli_formula(n, p, m1, m2)
        P = moivre_laplace_integral_formula(m1, m2, p, n)
        x1 = (m1 - n*p) / sqrt(n * p * q)
        x2 = (m2 - n*p) / sqrt(n * p * q)
        
        self.x1.setText(self.X1_prefix + str(round(x1, 12)))
        self.x2.setText(self.X2_prefix + str(round(x2, 12)))
        self.integral_formula_result.setText(self.P_prefix + str(round(P, 12)))
        self.bernoulli_result.setText(self.P_prefix + str(round(Pbern, 12)))

    
    def task_name(self):
        return "2. Интегральная теорема Муавра-Лапласа"