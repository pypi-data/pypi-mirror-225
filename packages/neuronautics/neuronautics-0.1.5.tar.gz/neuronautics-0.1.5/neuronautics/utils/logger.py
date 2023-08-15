from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal


class Logger(QObject):

    process_time = dict()
    progress_signal = pyqtSignal(str, int)
    me = None

    @classmethod
    def get_logger(cls):
        if cls.me is None:
            cls.me = Logger()
        return cls.me

    def log_process(self, title, current_step, total_steps):
        percent = 0 if total_steps == 0 else current_step / total_steps
        times = self.process_time.get(title, [])
        times.append(datetime.now())
        self.process_time[title] = times
        msg = '??'
        if len(times) > 1:
            t0 = times[0]
            delta = 0
            for t in times[1:]:
                delta += (t-t0).total_seconds()
                t0 = t
            avg_delta = delta / (len(times) - 1)
            remaining_time = avg_delta * (total_steps - current_step)
            hours, remainder = divmod(remaining_time, 3600)
            minutes, secs = divmod(remainder, 60)
            msg = f'{hours:02.0f}:{minutes:02.0f}:{secs:05.2f}'

        if current_step >= total_steps:
            msg = f'Total time [{times[-1]-times[0]}]'
            self.process_time.pop(title)

        self.progress_signal.emit(msg, int(100*percent))
