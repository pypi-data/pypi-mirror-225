import unittest
from unittest.mock import patch, MagicMock
from neuronautics.utils.logger import Logger
from datetime import datetime, timedelta


class TestLogger(unittest.TestCase):
    def test_get_logger_singleton(self):
        instance1 = Logger.get_logger()
        instance2 = Logger.get_logger()
        self.assertEqual(instance1, instance2)  # add assertion here

    def test_log_process_first_log(self):
        logger = Logger.get_logger()
        logger.process_time.clear() # ensuring first log
        logger.progress_signal = MagicMock()

        logger.log_process('title', 3, 100)
        logger.progress_signal.emit.assert_called_once_with('??', 3)

    def test_log_process(self):
        logger = Logger.get_logger()
        logger.process_time.clear() # ensuring first log
        logger.progress_signal = MagicMock()

        logger.log_process('title', 1, 100)
        logger.log_process('title', 10, 100)

        calls = logger.progress_signal.emit.call_args_list

        self.assertEqual(calls[0].args, ('??', 1))
        self.assertEqual(calls[1].args[1], 10)
        self.assertRegex(calls[1].args[0], r'00:0\d:\d\d.\d\d')

    def test_log_process_end_msg(self):
        logger = Logger.get_logger()
        logger.process_time.clear() # ensuring first log
        logger.progress_signal = MagicMock()

        logger.log_process('title', 1, 100)
        logger.log_process('title', 100, 100)

        calls = logger.progress_signal.emit.call_args_list

        self.assertEqual(calls[0].args, ('??', 1))
        self.assertEqual(calls[1].args[1], 100)
        self.assertRegex(calls[1].args[0], r'Total time \[00:0\d:\d\d.\d\d\]')


if __name__ == '__main__':
    unittest.main()
