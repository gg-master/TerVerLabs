from widgets import TaskView
from utils.paths import resolve_path
from PyQt5 import uic
from PyQt5.QtWidgets import QDoubleSpinBox, QHBoxLayout, QSpinBox
from PyQt5.QtGui import QFont
from formulas.probabilities import bernoulli_formula, polynomial_distribution


class Lab3Task1(TaskView):
    def __init__(self, task_number: int, parent):
        super().__init__(parent)
        self._task_number: int = task_number
        uic.loadUi(resolve_path('ui/lab3_task1.ui'), self)

        self._p_k = 1
        self._init_ui()

    def _init_ui(self):
        # Bernulli page
        self.b_less.clicked.connect(self._bernulli_change_formula)
        self.b_equal.clicked.connect(self._bernulli_change_formula)
        self.b_equal_or_greater.clicked.connect(self._bernulli_change_formula)
        self.b_betwen.clicked.connect(self._bernulli_change_formula)
        self.b_n.valueChanged.connect(self._compute_bernulli)
        self.b_p.valueChanged.connect(self._compute_bernulli)
        self.bernulli_input_m_1.valueChanged.connect(self._compute_bernulli)
        self.bernulli_input_m_2.valueChanged.connect(self._compute_bernulli)
        self.b_equal.clicked.emit()

        # Polinom page
        self.p_k.valueChanged.connect(self._update_count_of_m)
        self.pm1.valueChanged.connect(self._on_pm_input_changed)
        self.pp1.valueChanged.connect(self._compute_polinom)
        self.p_n.valueChanged.connect(
            lambda: self.pm1.valueChanged.emit(self.pm1.value())
        )
        self.pm1.valueChanged.emit(self.pm1.value())

    def task_name(self):
        return f"{self._task_number}. Применение формулы Бернулли и полиномиальной формулы"

    # ------------------------ BERNULLLI FROMULAS ---------------------------------
    def _bernulli_change_formula(self):
        sender_attr = getattr(self, f"{self.sender().objectName()}")

        self.bernulli_input_m_1.hide()

        if sender_attr is self.b_less:
            self.bernulli_formula_k.setText('k < ')
        elif sender_attr is self.b_equal:
            self.bernulli_formula_k.setText('k = ')
        elif sender_attr is self.b_equal_or_greater:
            self.bernulli_formula_k.setText('k >= ')
        elif sender_attr is self.b_betwen:
            self.bernulli_input_m_1.show()
            self.bernulli_formula_k.setText(' <= k <= ')
        self._compute_bernulli()

    def _compute_bernulli(self):
        self.bernulli_input_m_1.setMaximum(self.b_n.value())
        self.bernulli_input_m_2.setMaximum(self.b_n.value())

        start = self.bernulli_input_m_2.value()
        end = None
        if self.b_betwen.isChecked():
            start = self.bernulli_input_m_1.value()
            end = self.bernulli_input_m_2.value()
        elif self.b_less.isChecked():
            start = 0
            end = self.bernulli_input_m_2.value()
        elif self.b_equal_or_greater.isChecked():
            start = self.bernulli_input_m_2.value()
            end = self.b_n.value()
        self.bernulli_formula_result.setText(
            str(
                round(
                    bernoulli_formula(
                        self.b_n.value(), self.b_p.value(), start, end
                    ),
                    12,
                )
            )
        )

    # ------------------------ POLINOM FORMULAS -----------------------------------
    def _update_count_of_m(self):
        count = self.p_k.value()

        # Adding new widgets
        for num in range(self._p_k + 1, count + 1, 1):
            self._add_new_m_p_spinbox(num)

        # Remove extra widgets
        for num in range(self._p_k, count, -1):
            self._remove_m_p_spinbox(num)

        self._p_k = count
        self._compute_polinom()
        self.pm1.valueChanged.emit(self.pm1.value())

    def _add_new_m_p_spinbox(self, num: int):
        f = QFont()
        f.setPixelSize(17)

        m_spb = QSpinBox()
        m_spb.setValue(0)
        m_spb.setPrefix(f'm{num} = ')
        m_spb.setObjectName(f'pm{num}')
        m_spb.setFont(f)
        m_spb.setMinimum(0)
        m_spb.setSingleStep(1)
        m_spb.valueChanged.connect(self._on_pm_input_changed)

        p_spb = QDoubleSpinBox()
        p_spb.setValue(0.0)
        p_spb.setPrefix(f'p{num} = ')
        p_spb.setObjectName(f'pp{num}')
        p_spb.setFont(f)
        p_spb.setMaximum(1)
        p_spb.setDecimals(3)
        p_spb.setSingleStep(0.01)
        p_spb.valueChanged.connect(self._compute_polinom)

        layout = QHBoxLayout()
        layout.addWidget(m_spb)
        layout.addWidget(p_spb)

        self.scrollAreaWidgetContents.layout().insertLayout(num - 1, layout)

        setattr(self, f'layout_{num}', layout)
        setattr(self, f'pm{num}', m_spb)
        setattr(self, f'pp{num}', p_spb)

    def _remove_m_p_spinbox(self, num: int):
        spb = getattr(self, f'pm{num}')
        spb.setVisible(False)
        spb.disconnect()
        spb = getattr(self, f'pp{num}')
        spb.setVisible(False)
        spb.disconnect()
        delattr(self, f'layout_{num}')
        delattr(self, f'pm{num}')
        delattr(self, f'pp{num}')

    def _on_pm_input_changed(self):
        sender_attr = getattr(self, f"{self.sender().objectName()}")

        s = 0
        for attr in sorted(
            [getattr(self, f"pm{num}") for num in range(1, self._p_k + 1)],
            key=lambda x: x.value(),
        ):
            attr.setStyleSheet("")
            val = attr.value()
            attr.setMaximum(max(0, self.p_n.value() - s))
            s += val

        if s + 0.0001 < self.p_n.value():
            f = QFont()
            f.setPixelSize(17)
            sender_attr.setFont(f)
            sender_attr.setStyleSheet("background-color: rgb(255, 170, 0)")

        self._compute_polinom()

    def _compute_polinom(self):
        m_list = [
            getattr(self, f"pm{num}").value()
            for num in range(1, self._p_k + 1)
        ]
        p_list = [
            getattr(self, f"pp{num}").value()
            for num in range(1, self._p_k + 1)
        ]
        self.polinom_formula_result.setText(
            str(
                round(
                    polynomial_distribution(m_list, p_list),
                    12,
                )
            )
        )
