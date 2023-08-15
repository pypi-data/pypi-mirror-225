from PyQt5.QtGui import QFont
from PyQt5.QtCore import QMargins
from PyQt5.QtWidgets import QSizePolicy
from neuronautics.plotters.line_2d import Line2D


class MiniLine2D(Line2D):
    def __init__(self, parent, yaxis=False, xaxis=False):
        super().__init__(parent)

        self.yaxis.setTickCount(3)  # Adjust the number of ticks
        self.yaxis.setLabelFormat("%.2f")  # Format the labels (adjust as needed)
        # Set font size for the axis labels
        font = QFont()
        font.setPointSize(6)  # Adjust font size
        self.yaxis.setLabelsFont(font)
        self.yaxis.setVisible(yaxis)
        self.xaxis.setVisible(xaxis)

        self.chart.legend().hide()  # Hide the plot legend
        self.chart.layout().setContentsMargins(0, 0, 0, 0)  # Remove margins for the chart
        self.chart.layout().setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))  # Remove margins for the chart

        self.chart.setBackgroundRoundness(0)  # Set background roundness to zero

        # Set up the chart appearance
        self.chart.setBackgroundVisible(False)  # Hide the chart's background
        self.chart.setPlotAreaBackgroundVisible(False)  # Hide the plot area's background

        # Set the plot area margins to zero to maximize the plot area
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.single_chart_view.allow_selection(False)

    def plot_xy(self, xvalues, yvalues):
        super().plot_xy(xvalues, yvalues)
        self.single_chart_view.setContentsMargins(0, 0, 0, 0)  # Remove margins for the QChartView
