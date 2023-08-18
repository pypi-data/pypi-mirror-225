from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal


class Logger(QObject):
    """
    Provides logging capabilities for tracking and reporting process progress.

    This class allows you to log the progress of processes, estimating remaining
    time, and emitting signals for progress updates.

    Attributes:
        process_time (dict): A dictionary storing process titles as keys and
                            corresponding start and end time instances as values.
        progress_signal (pyqtSignal): A signal emitted on progress updates, providing
                                     a formatted message and progress percentage.
        me (Logger): A class-level instance of the Logger class, acting as a singleton.

    Methods:
        get_logger(cls): Returns the singleton instance of the Logger class.
        log_process(self, title, current_step, total_steps): Logs process progress,
                                                             estimating remaining time,
                                                             and emits progress signals.
    """

    process_time = dict()
    progress_signal = pyqtSignal(str, int)
    me = None

    @classmethod
    def get_logger(cls):
        """
        Returns a singleton instance of the Logger class.

        This class method returns an instance of the Logger class if it doesn't
        exist already. The Logger class utilizes a singleton pattern, ensuring
        that only one instance of the class is created and shared across calls.

        Returns:
            Logger: A singleton instance of the Logger class.
        """
        if cls.me is None:
            cls.me = Logger()
        return cls.me

    def log_process(self, title, current_step, total_steps):
        """
        Logs the progress of a process, estimates remaining time, and emits
        progress signals.

        Args:
            title (str): The title of the process.
            current_step (int): The current step of the process.
            total_steps (int): The total number of steps in the process.
        """
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
            total_time = (times[-1]-times[0]).total_seconds()

            hours, remainder = divmod(total_time, 3600)
            minutes, secs = divmod(remainder, 60)
            msg = f'{hours:02.0f}:{minutes:02.0f}:{secs:05.2f}'
            msg = f'Total time [{msg}]'
            self.process_time.pop(title)

        self.progress_signal.emit(msg, int(100*percent))
