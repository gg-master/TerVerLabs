from widgets import TaskView
from utils.paths import resolve_path
from utils.files import load_text_file, parse_statistic_file
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from utils.plots import *
from traceback import print_exc

from formulas.statistics import process_continuous_data, process_continuous_plot_data


class Lab5Task2(TaskView):
    def __init__(self, task_number: int, parent):
        super().__init__(parent)
        self._task_number: int = task_number
        self.currentFile = None
        self.data = None

        uic.loadUi(resolve_path('ui/lab5_task2.ui'), self)
        self.openFile.clicked.connect(self.file_load_signal)
        self.prepare_plots()

    def prepare_plots(self):
        pass

    def load_data(self):
        continuous_data = process_continuous_data(self.data)
        plot_data = process_continuous_plot_data(continuous_data)
        # TODO: ... 
         # Основные харрактеристики
        self.xv_label.setText(str(round(continuous_data.x_v, 5)))
        self.dv_label.setText(str(round(continuous_data.D_v, 5)))
        self.sigma_v_label.setText(str(round(continuous_data.sigma, 5)))
        self.s_label.setText(str(round(continuous_data.S, 5)))

    def file_load_signal(self):
        load_text_file(self)
        if self.currentFile:
            try:
                self.data = parse_statistic_file(self.currentFile)
                self.load_data()
            except Exception as e:
                print_exc()
                QMessageBox.critical(self, "Возникла ошибка", str(e))

    def task_name(self):
        return f"{self._task_number}. Непрерывная случайная величина"