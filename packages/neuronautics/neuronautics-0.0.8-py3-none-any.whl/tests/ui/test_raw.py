import unittest
from unittest.mock import patch, MagicMock, call
from neuronautics.ui.raw import Raw
from neuronautics.ui.abstract_source import AbstractSource
from neuronautics.recordings.mcs_raw import McsRaw

import pandas as pd
import numpy as np


class TestRaw(unittest.TestCase):
    def test_constructor(self):
        mock_ui = MagicMock()
        raw = Raw(ui=mock_ui)
        self.assertIsInstance(raw, AbstractSource)
        self.assertIs(raw.ui, mock_ui)
        self.assertIs(raw.data_handler, McsRaw)

    def test_load_files(self):
        mock_ui = MagicMock()
        files = ['file1.h5', 'file2.h5']
        with patch('glob.glob') as spy_glob:
            spy_glob.return_value = files
            raw = Raw(mock_ui)
            raw.load_files('/random/folder')

            call_args_list = mock_ui.rawBtn.setEnabled.call_args_list
            self.assertEqual(call_args_list[0].args, (False,))
            self.assertEqual(call_args_list[1].args, (True,))
            self.assertListEqual(raw.filenames, files)

    def test_load_files_empty_folder(self):
        mock_ui = MagicMock()
        files = []
        with patch('glob.glob') as spy_glob:
            spy_glob.return_value = files
            raw = Raw(mock_ui)
            raw.load_files('/random/folder')

            mock_ui.rawBtn.setEnabled.assert_called_once_with(False)
            self.assertListEqual(raw.filenames, [])

    def test_select_view(self):
        with patch('neuronautics.ui.spike.AbstractSource.select_view') as spy_select_view:
            mock_ui = MagicMock()
            raw = Raw(mock_ui)

            raw.select_view()

            spy_select_view.assert_called_once()
            mock_ui.optionStck.setCurrentWidget.assert_called_once_with(mock_ui.rawOptPage)

    def test_plot_single_view(self):
        mock_ui = MagicMock()
        mock_ui.recording_start_s = 0
        mock_ui.single_chart_view.x_label.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.y_label.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.title.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.plot_xy.return_value = mock_ui.single_chart_view

        spy_data_handler = MagicMock()
        spy_data_handler.return_value = spy_data_handler
        spy_data_handler.to_ticks.side_effect = lambda x, _: x
        spy_data_handler.get_channel_data.return_value = ([0, 1, 2], [0.1, 0.2, 0.3])

        spike = Raw(mock_ui)
        spike.data_handler = spy_data_handler

        spike._plot_single_view(path='/random/file.h5', channel_id=0)

        mock_ui.single_chart_view.x_label.assert_called_once_with('Time (seconds)')
        mock_ui.single_chart_view.y_label.assert_called_once_with('Microvolts')
        mock_ui.single_chart_view.title.assert_called_once_with('Channel 0')
        mock_ui.single_chart_view.plot_xy.assert_called_once_with(
            [0, 1, 2], [0.1, 0.2, 0.3]
        )

    def test_plot_grid_view(self):
        mock_ui = MagicMock()
        mock_ui.recording_start_s = 0
        mock_ui.multiple_chart_view.plot_xy.return_value = mock_ui.multiple_chart_view

        spy_data_handler = MagicMock()
        spy_data_handler.return_value = spy_data_handler
        spy_data_handler.to_ticks.side_effect = lambda x, _: x
        spy_data_handler.get_all_data.return_value = {0: ([0, 1, 2], [0.1, 0.2, 0.3])}

        spike = Raw(mock_ui)
        spike.data_handler = spy_data_handler

        spike._plot_grid_view(path='/random/file.h5')

        mock_ui.multiple_chart_view.plot_xy.assert_called_once_with(
            {0: ([0, 1, 2], [0.1, 0.2, 0.3])}
        )

    def test_plot_list_view(self):
        mock_ui = MagicMock()
        mock_ui.recording_start_s = 0
        mock_ui.list_chart_view.plot_xy.return_value = mock_ui.list_chart_view

        spy_data_handler = MagicMock()
        spy_data_handler.return_value = spy_data_handler
        spy_data_handler.to_ticks.side_effect = lambda x, _: x
        spy_data_handler.get_channel_data.return_value = ([0, 1, 2], [0.1, 0.2, 0.3])

        spike = Raw(mock_ui)
        spike.filenames = ['file.h5']
        spike.data_handler = spy_data_handler

        spike._plot_list_view(channel_id=1)

        mock_ui.list_chart_view.plot_xy.assert_called_once_with(
            {'file': ([0, 1, 2], [0.1, 0.2, 0.3])}
        )

    def test_get_filename(self):
        fn = Raw.get_filename('/path/to/file.h5')
        self.assertEqual(fn, 'file')

    def test_extract_spikes(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.currentText.return_value = 'file.h5'
        mock_ui.sigmaValue.value.return_value = 4
        mock_ui.windowValue.value.return_value = 1000

        spy_data_handler = MagicMock()
        spy_data_handler.return_value = spy_data_handler
        spy_data_handler.extract_all_spikes.return_value = MagicMock()

        spike = Raw(mock_ui)
        spike.data_handler = spy_data_handler

        spike.extract_spikes()

        spy_data_handler.extract_all_spikes.assert_called_once_with(4, 1000)
        spy_data_handler.extract_all_spikes.return_value.to_csv.assert_called_once_with('file.spike', index=False)

    def test_extract_spikes_empty_selector(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.currentText.return_value = None
        mock_ui.sigmaValue.value.return_value = 4
        mock_ui.windowValue.value.return_value = 1000

        spy_data_handler = MagicMock()
        spy_data_handler.return_value = spy_data_handler
        spy_data_handler.extract_all_spikes.return_value = MagicMock()

        spike = Raw(mock_ui)
        spike.data_handler = spy_data_handler

        spike.extract_spikes()

        spy_data_handler.extract_all_spikes.assert_not_called()

    def test_extract_all_spikes(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.count.return_value = 2

        with patch('PyQt5.QtWidgets.QApplication.processEvents') as spy_events:
            spike = Raw(mock_ui)
            spike.extract_spikes = MagicMock()

            spike.extract_all_spikes()

            mock_ui.fileSelector.setCurrentIndex.assert_has_calls([call(0), call(1)])
            spike.extract_spikes.assert_called()


if __name__ == '__main__':
    unittest.main()
