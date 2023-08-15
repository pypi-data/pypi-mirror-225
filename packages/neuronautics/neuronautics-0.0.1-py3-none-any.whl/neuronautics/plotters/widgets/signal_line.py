from PyQt5.QtChart import QLineSeries
from PyQt5.QtGui import QColor
import numpy as np


signal_color = {
    -3: (0, 0, 0, 0),      # invisible
    -2: (30, 144, 255),    # Blue       -- line selected
    -1: (200, 200, 200),   # Light Gray -- noise
    0: (50, 50, 50),       # Black
    1: (230, 85, 85),      # Soft Red
    2: (85, 230, 85),      # Soft Green
    3: (85, 85, 230),      # Soft Blue
    4: (230, 185, 85),     # Soft Orange
    5: (180, 85, 230),     # Soft Purple
    6: (230, 230, 85),     # Soft Yellow
    7: (85, 230, 230),     # Soft Cyan
    8: (230, 85, 230),     # Soft Magenta
    9: (150, 150, 150),    # Soft Gray
    10: (230, 160, 180),   # Soft Pink
}


class SignalLine(QLineSeries):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal_id = 0
        self.time_ms = 0
        self.visible = True
        self.y_range = None
        self.x_range = None

    @classmethod
    def color(cls, sid: int):
        return signal_color.get(sid, (0, 0, 0))

    def _change_color(self, cid: int):
        pen = self.pen()
        pen.setColor(QColor(*self.color(cid)))
        self.setPen(pen)

    def select(self):
        self._change_color(-2)

    def unselect(self):
        self._change_color(self.signal_id)

    def set_id(self, signal_id: int):
        self.signal_id = signal_id
        self._change_color(self.signal_id)

    def set_visible(self, visibility: bool):
        self.visible = visibility
        if self.visible:
            self._change_color(self.signal_id)
        else:
            self._change_color(-3)

    def set_time(self, time_ms):
        self.time_ms = time_ms

    def has_points_inside_bounding_box(self, x_start, x_end, y_start, y_end):
        if not self.visible:
            return False

        x_start, x_end = min(x_start, x_end), max(x_start, x_end)
        y_start, y_end = min(y_start, y_end), max(y_start, y_end)

        # Check if any points in the series fall within the bounding box
        for point in self.pointsVector():
            x = point.x()
            y = point.y()
            if x_start <= x <= x_end and y_start <= y <= y_end:
                return True
        return False

    def append(self, *args, **kwargs):
        super().append(*args, **kwargs)
        ys = np.array([point.y() for point in self.pointsVector()])
        xs = np.array([point.x() for point in self.pointsVector()])
        self.y_range = (ys.min(), ys.max())
        self.x_range = (xs.min(), xs.max())
