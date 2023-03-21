from widgets import TaskView
from utils.paths import resolve_path
from PyQt5 import uic
from PyQt5.QtGui import QPixmap


class Lab2_Task1_2(TaskView):
    FORMULA_TASK_1 = "P(B) = P(A<sub>1</sub>) · (1 - P(¬A<sub>2</sub>) · P(¬A<sub>3</sub>) · P(¬A<sub>4</sub>)) · P(A<sub>5</sub>) ="
    FORMULA_TASK_2 = "P(B) = (1 - P(¬A<sub>1</sub>) · P(¬A<sub>2</sub>)) · P(A<sub>3</sub>) · (P(A<sub>4</sub>) · P(A<sub>5</sub>) + P(A<sub>6</sub>) - P(A<sub>4</sub>) · P(A<sub>5</sub>) · P(A<sub>6</sub>)) ="

    def __init__(self, task_number: int, parent):
        super().__init__(parent)
        self._task_number = task_number
        uic.loadUi(resolve_path("ui/lab2_task1_2.ui"), self)

        self.Pa1_spinbox.valueChanged.connect(self.on_spinbox_input)
        self.Pa2_spinbox.valueChanged.connect(self.on_spinbox_input)
        self.Pa3_spinbox.valueChanged.connect(self.on_spinbox_input)
        self.Pa4_spinbox.valueChanged.connect(self.on_spinbox_input)
        self.Pa5_spinbox.valueChanged.connect(self.on_spinbox_input)
        self.Pa6_spinbox.valueChanged.connect(self.on_spinbox_input)

        if task_number > 2 or task_number < 1:
            raise ValueError("Invalid task number")

        font = self.formulaText.font()
        if task_number == 1:
            self.formulaText.setText(self.FORMULA_TASK_1)
            self.taskImage.setPixmap(QPixmap(resolve_path("images/lab2_task1.png")))
            self._set_layout_visibility(self.Pa6, False)
            font.setPointSize(16)
            self.formulaText.setFont(font)
            self.result.setFont(font)
            self.Pa6_spinbox.blockSignals(True)
        elif task_number == 2:
            font.setPointSize(14)
            self.formulaText.setText(self.FORMULA_TASK_2)
            self.formulaText.setFont(font)
            self.result.setFont(font)
            self.taskImage.setPixmap(QPixmap(resolve_path("images/lab2_task2.png")))
            self._set_layout_visibility(self.Pa6, True)

    @staticmethod
    def _set_layout_visibility(item, state: bool):
        if (item.widget()):
            item.widget().setVisible(state)
        elif (item.layout()):
            layout = item.layout()
            for i in range(layout.count()):
                Lab2_Task1_2._set_layout_visibility(layout.itemAt(i), state)  

    @staticmethod
    def task1_formula(Pa1, Pa2, Pa3, Pa4, Pa5):
        _Pa2 = 1 - Pa2
        _Pa3 = 1 - Pa3
        _Pa4 = 1 - Pa4
        return Pa1 * (1 - _Pa2 * _Pa3 * _Pa4) * Pa5

    @staticmethod
    def task2_formula(Pa1, Pa2, Pa3, Pa4, Pa5, Pa6):
        _Pa1 = 1 - Pa1
        _Pa2 = 1 - Pa2
        return (1 - _Pa1 * _Pa2) * Pa3 * (Pa4 * Pa5 + Pa6 - Pa4 * Pa5 * Pa6) 

    def compute_probability(self):
        Pa1 = self.Pa1_spinbox.value()
        Pa2 = self.Pa2_spinbox.value()
        Pa3 = self.Pa3_spinbox.value()
        Pa4 = self.Pa4_spinbox.value()
        Pa5 = self.Pa5_spinbox.value()
        Pa6 = self.Pa6_spinbox.value()
        if self._task_number == 1:
            return self.task1_formula(Pa1, Pa2, Pa3, Pa4, Pa5)
        else:
            return self.task2_formula(Pa1, Pa2, Pa3, Pa4, Pa5, Pa6)
    
    def task_name(self):
        return f"{self._task_number}. Вероятность безотказной работы заданной схемы"

    def on_spinbox_input(self):
        self.result.setText(str(round(self.compute_probability(), 12)))
    
