from widgets import TaskView
from utils.paths import resolve_path
from utils.files import load_text_file, parse_statistic_file
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMessageBox,
    QVBoxLayout,
    QTableWidgetItem,
    QTableWidget,
    QAbstractItemView,
)

from utils.plots import *
from traceback import print_exc
from scipy.stats import chi2

from formulas.statistics import (
    process_continuous_data,
    process_normal_density,
    ContinuousData,
    process_continuous_intervals,
    normal_theorethical_probability,
    normal_chi2
)


class Lab6Task1(TaskView):
    def __init__(self, task_number: int, parent):
        super().__init__(parent)
        self._task_number: int = task_number
        self.currentFile = None
        self.data = None

        uic.loadUi(resolve_path('ui/lab6_task1.ui'), self)
        self.openFile.clicked.connect(self.file_load_signal)
        self.calculateButton.clicked.connect(self.load_data)
        self.manualInput.stateChanged.connect(self.manual_input_activate)

        self.intervals_combobox.currentIndexChanged.connect(self.interval_selected)
        self.alpha.valueChanged.connect(self.alpha_changed)

        self.table.setRowCount(4)
        self.table.setVerticalHeaderLabels(['xi; xi+1', 'ni', 'ωi', 'ci'])
        self.prepare_plots()

    def prepare_plots(self):
        lt = QVBoxLayout()
        self.histpolygon = PolygonHistogram(
            self, name='Гистограмма относительных частот'
        )
        lt.addWidget(self.histpolygon, alignment=Qt.Alignment())
        self.continuous_rel_histpolygon.setLayout(lt)

        lt = QVBoxLayout()
        self.density_graph = ContinuousFunction(
            self, name='Плотность распределения'
        )
        lt.addWidget(self.density_graph, alignment=Qt.Alignment())
        self.density_plot.setLayout(lt)

    def read_manual_data(self):
        count = self.intervalCount.value()
        data = ContinuousData([], [], [], [], 0, 0, 0, 0, 0)

        for i in range(count):
            interval = self.table.item(0, i)
            if interval is None:
                raise ValueError('Обнаружена пустая клетка интервала.')
            interval = interval.text()

            if ';' not in interval:
                raise ValueError('Неправильно указан интервал.')
            
            left, righ = interval.replace(' ', '').replace(',', '.').split(';')
            data.intervals.append([float(left), float(righ)])

            freq = self.table.item(1, i)
            if freq is None:
                raise ValueError('Обнаружена пустая клетка частоты.')

            data.N.append(int(freq.text()))

        return process_continuous_intervals(data)

    def load_data(self):
        interval_count = self.intervalCount.value()

        if not self.manualInput.isChecked():
            continuous_data = process_continuous_data(
                self.data, interval_count
            )
        else:
            try:
                continuous_data = self.read_manual_data()
            except ValueError as err:
                QMessageBox.warning(self, 'Ошибка!', str(err))
                return None

        self.continuous_data = continuous_data

        table = self.table
        table.setColumnCount(interval_count)

        for i in range(interval_count):
            N = continuous_data.N[i]
            W = continuous_data.W[i]
            mid = continuous_data.middles[i]
            table.setItem(
                0,
                i,
                QTableWidgetItem(
                    f'{round(continuous_data.intervals[i][0], 3)}; '
                    f'{round(continuous_data.intervals[i][1], 3)}\t'
                ),
            )
            table.setItem(1, i, QTableWidgetItem(f'{N}\t'))
            table.setItem(2, i, QTableWidgetItem(f'{round(W, 3)}\t'))
            table.setItem(3, i, QTableWidgetItem(f'{round(mid, 3)}\t'))

        # Основные харрактеристики
        self.xv_label.setText(str(round(continuous_data.x_v, 5)))
        self.dv_label.setText(str(round(continuous_data.D_v, 5)))
        self.sigma_v_label.setText(str(round(continuous_data.sigma, 5)))
        self.s_label.setText(str(round(continuous_data.S, 5)))

        a = continuous_data.x_v
        sigma = continuous_data.sigma

        self.a = a
        self.sigma = sigma


        # Эмпирическая функция
        if sigma:
            plot_data = process_normal_density(a, sigma)
            self.density_graph.display(
                plot_data, 'x', 'f*(x)', color='k'
            )

        self.a_label.setText(str(round(a, 5)))
        self.sigma_label.setText(str(round(sigma, 5)))
        self.alpha_changed(self.alpha.value())

        # Гистограмма частот и относительных частот
        bounds = list(map(lambda x: x[0], continuous_data.intervals))
        bounds.append(continuous_data.intervals[-1][1])

        self.histpolygon.set_x_gap(None)
        Xmin = continuous_data.intervals[0][0]
        if continuous_data.middles[0] > 100:
            self.histpolygon.set_x_gap(round(Xmin - (Xmin / 4), 2))

        self.histpolygon.display(
            bounds,
            continuous_data.h,
            continuous_data.middles,
            continuous_data.N,
            'xi*',
            'ni/nh',
        )

        self.intervals_combobox.clear()
        self.intervals_combobox.addItems(list(map(lambda x: f"[{x[0]}, {x[1]})", continuous_data.intervals)))
    
    def alpha_changed(self, value):
        k = self.intervalCount.value() - 3
        # k = m - 3 только для нормального распределения, у других распределений другая формула
        if k > 0 and self.sigma:
            alpha = value
            chi2_crit = round(chi2.ppf(1 - alpha, k), 5)
            chi2_exp = round(normal_chi2(self.intervalCount.value(), self.a, self.sigma, self.continuous_data), 5)
        
            self.k_label.setText(str(k))
            self.chi2_label.setText(str(chi2_crit))
            self.chi2_exp_label.setText(str(chi2_exp))

            if chi2_exp > chi2_crit:
                self.checkResult_label.setStyleSheet("color: red; font-size: 24px")
                self.checkResult_label.setText("ГИПОТЕЗА ОТВЕРГНУТА")
            else:
                self.checkResult_label.setStyleSheet("color: green; font-size: 24px")
                self.checkResult_label.setText("ГИПОТЕЗА ПОДТВЕРЖДЕНА")

    def interval_selected(self, index):
        interval = self.continuous_data.intervals[index]
        if self.sigma:
            self.prob_label.setText(str(
                round(normal_theorethical_probability(interval, self.a, self.sigma), 5)))
    
    def file_load_signal(self):
        self.file_input_activate()
        load_text_file(self)
        if self.currentFile:
            try:
                self.data = parse_statistic_file(self.currentFile)
                self.intervalCount.setMaximum(len(set(self.data)))
                self.load_data()
            except Exception as err:
                print_exc()
                QMessageBox.critical(self, "Возникла ошибка", str(err))

    def file_input_activate(self):
        self.manualInput.disconnect()
        self.manualInput.stateChanged.connect(self.manual_input_activate)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.helpText.setText(
            'В файле должны находиться числа, которые '
            'разделены пробелом или переносом строки'
        )

    def manual_input_activate(self):
        self.manualInput.disconnect()
        self.manualInput.stateChanged.connect(self.file_input_activate)

        self.intervalCount.valueChanged.connect(self.interval_count_changed)
        self.table.setColumnCount(0)
        self.table.setColumnCount(self.intervalCount.value())
        self.table.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.helpText.setText(
            'Укажите количество интервалов, а после введите '
            'значения xi и ni и нажмите "Рассчитать". '
            'Границы интервалов должны разделяться ";"'
        )

    def interval_count_changed(self):
        self.table.setColumnCount(self.intervalCount.value())

    def task_name(self):
        return f"{self._task_number}. Проверка гипотезы о нормальном распределении"
