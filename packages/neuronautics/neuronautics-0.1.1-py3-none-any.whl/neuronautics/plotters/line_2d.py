import numpy as np
from PyQt5.QtChart import QChart, QChartView, QValueAxis
from PyQt5.QtCore import Qt, QPointF, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QVBoxLayout


from neuronautics.plotters.widgets.signal_line import SignalLine
from neuronautics.plotters.widgets.signal_unit_selector import SignalUnitSelector
from neuronautics.plotters.widgets.signal_view_selector import SignalViewSelector

from neuronautics.utils.logger import Logger
logger = Logger.get_logger()


class DragSelectChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)

        self.parent = parent

        # Variables to track selection
        self.dragging = False
        self.startPos = None
        self.endPos = None
        self.allow_dragging = True


    def allow_selection(self, allow):
        self.allow_dragging = allow

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.startPos = event.pos()
            self.endPos = event.pos()
        elif event.button() == Qt.RightButton:
            self.parent.view_series()

    def mouseReleaseEvent(self, event):
        if self.allow_dragging and self.dragging:
            self.endPos = event.pos()
            self.dragging = False

            x_start = self.chart().mapToValue(self.mapToScene(self.startPos)).x()
            y_start = self.chart().mapToValue(self.mapToScene(self.startPos)).y()

            x_end = self.chart().mapToValue(self.mapToScene(self.endPos)).x()
            y_end = self.chart().mapToValue(self.mapToScene(self.endPos)).y()

            x_start, x_end = min(x_start, x_end), max(x_start, x_end)
            y_start, y_end = min(y_start, y_end), max(y_start, y_end)

            self.parent.select_series(x_start, x_end, y_start, y_end)


class Line2D(QWidget):
    signal_unit_changed = pyqtSignal(list)

    def __init__(self, parent):
        super().__init__(parent)

        self.chart = QChart()
        self.series = []

        self.xaxis = QValueAxis()
        self.xaxis.setTickCount(11)
        self.yaxis = QValueAxis()
        self.yaxis.setTickCount(11)


        self.chart.addAxis(self.xaxis, Qt.AlignBottom)
        self.chart.addAxis(self.yaxis, Qt.AlignLeft)
        self.chart.legend().setVisible(False)  # Hide the plot legend

        self.single_chart_view = DragSelectChartView(self.chart, parent=self)
        self.single_chart_view.setRenderHint(QPainter.Antialiasing)  # Optional: enable antialiasing for smoother lines

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero
        layout.setSpacing(0)
        layout.addWidget(self.single_chart_view)

        parent.setLayout(layout)

    def x_label(self, xlab):
        self.xaxis.setLabelFormat("%.2f")  # Set the label format for the X axis
        self.xaxis.setTitleText(xlab)  # Set the label for the X axis
        return self

    def y_label(self, ylab):
        self.yaxis.setLabelFormat("%.2f")
        self.yaxis.setTitleText(ylab)
        return self

    def title(self, title):
        self.chart.setTitle(title)
        return self

    def plot_xy(self, x_values, y_values, *args, **kwargs):
        self.plot([zip(x_values, y_values)], *args, **kwargs)

    def plot(self,  values=None, group=None, allow_selection=False, xlim=None, ylim=None, progress_bar=False):
        self.single_chart_view.allow_selection(allow_selection)
        self.clear()

        y_range = (np.Inf, -np.Inf)
        x_range = (np.Inf, -np.Inf)
        for ix, series in enumerate(values):
            if progress_bar:
                logger.log_process('plot', ix, len(values))

            line = SignalLine()
            if group is not None:
                line.set_id(group[ix])
            line.append([QPointF(x, y) for x, y in series])

            x_range, y_range = self._update_ranges(line, x_range, y_range)

            self.chart.addSeries(line)
            self.chart.setAxisY(self.yaxis, line)
            self.chart.setAxisX(self.xaxis, line)

            self.series.append(line)

        if progress_bar:
            logger.log_process('plot', len(values), len(values))

        x_range = x_range if xlim is None else xlim
        y_range = y_range if ylim is None else ylim
        self.xaxis.setRange(*x_range)
        self.yaxis.setRange(*y_range)

    @classmethod
    def _update_ranges(cls, line, x_range, y_range):
        y_r = line.y_range
        y_range = (min(y_r[0], y_range[0]), max(y_r[1], y_range[1]))
        x_r = line.x_range
        x_range = (min(x_r[0], x_range[0]), max(x_r[1], x_range[1]))
        return x_range, y_range

    def clear(self):
        for series in self.series:
            self.chart.removeSeries(series)
            series.clear()
        self.series.clear()
        self.series = []

    def select_series(self, x_start, x_end, y_start, y_end):
        selected_series = []
        signal_ids = set()

        for series in self.series:
            signal_ids.add(series.signal_id)
            if series.has_points_inside_bounding_box(x_start, x_end, y_start, y_end):
                selected_series.append(series)
                series.select()

        if selected_series:
            msg_box = SignalUnitSelector(signal_ids)
            result = msg_box.exec()
            time_unit = []
            if result == SignalUnitSelector.CANCEL:
                for series in selected_series:
                    series.unselect()
            elif result == SignalUnitSelector.NEW:
                new_id = sorted(list(set(range(1, 100)).difference(set(signal_ids))))[0]
                for series in selected_series:
                    series.set_id(new_id)
                    time_unit.append((series.time_ms, series.signal_id))
            else:
                for series in selected_series:
                    series.set_id(result)
                    time_unit.append((series.time_ms, series.signal_id))

            self.signal_unit_changed.emit(time_unit)


        self.update()

    def view_series(self):

        signal_ids = set()

        for series in self.series:
            signal_ids.add(series.signal_id)
        msg_box = SignalViewSelector(signal_ids)
        result = msg_box.exec()
        if result == 1:
            signal_ids_selected = msg_box.get_selected()

            y_min, y_max = np.Inf, -np.Inf
            for series in self.series:
                visible = signal_ids_selected.get(series.signal_id, True)
                series.set_visible(visible)
                if visible:
                    y_range = series.y_range
                    y_min = min(y_min, y_range[0])
                    y_max = max(y_max, y_range[1])

            self.yaxis.setRange(y_min, y_max)
            self.update()
