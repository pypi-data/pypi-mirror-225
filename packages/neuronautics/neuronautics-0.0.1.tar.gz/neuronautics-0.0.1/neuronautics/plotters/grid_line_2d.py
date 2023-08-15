from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy
from neuronautics.plotters.mini_line_2d import MiniLine2D
from neuronautics.plotters.line_2d import Line2D
from PyQt5.QtCore import Qt
from neuronautics.utils.logger import Logger

logger = Logger.get_logger()


class GridLine2D:

    def __init__(self, parent):
        layout = QVBoxLayout()
        layout.setSpacing(0)  # Set spacing to zero
        layout.setContentsMargins(0, 0, 0, 0)  # Set margins to zero

        self.channel_plots = {}
        parent.setLayout(layout)
        self.parent = parent

    def setup_grid(self, nrows=8, ncols=15, plot_names=None, show_axis=False):
        if plot_names is None:
            plot_names = [int(i) for i in range(nrows*ncols)]
        while len(plot_names) < nrows*ncols:
            plot_names.append(len(plot_names))
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Disable updates
        self.parent.setUpdatesEnabled(False)

        # Clear existing widgets from layout
        layout = self.parent.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()


        ch_id = 0
        for row in range(nrows):
            row_widget = QWidget()
            row_widget.setSizePolicy(size_policy)

            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            for col in range(ncols):
                if ch_id < len(plot_names):
                    w = QWidget()
                    w.setSizePolicy(size_policy)

                    row_layout.addWidget(w)
                    self.channel_plots[plot_names[ch_id]] = MiniLine2D(w, yaxis=show_axis)

                ch_id += 1
            layout.addWidget(row_widget)
        # Re-enable updates and refresh the layout
        self.parent.setUpdatesEnabled(True)
        self.parent.update()
        return self

    def plot_xy(self, data):
        length = len(data)

        for ix, (ch_id, (time, serie)) in enumerate(data.items()):
            logger.log_process('plotting_grid_lines', ix, length)
            self.channel_plots[ch_id].title(f'{ch_id}').plot_xy(time, serie)
        logger.log_process('plotting_grid_lines', length, length)

    def plot(self, data, *args, **kwargs):
        length = len(data)
        for plt in self.channel_plots.values():
            plt.clear()

        for ix, (ch_id, (values, group)) in enumerate(data.items()):
            logger.log_process('plotting_grid_lines', ix, length)
            self.channel_plots[ch_id].title(f'{ch_id}').plot(values=values, group=group, *args, **kwargs)
        logger.log_process('plotting_grid_lines', length, length)
