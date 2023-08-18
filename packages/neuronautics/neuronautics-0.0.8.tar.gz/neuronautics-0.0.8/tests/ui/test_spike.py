import unittest
from unittest.mock import patch, MagicMock
from neuronautics.ui.spike import (Spike, SINGLE_VIEW_LENGTH_S,
                                   GRID_VIEW_STACKED_S, GRID_VIEW_TIMESERIES_S)
from neuronautics.ui.abstract_source import AbstractSource
from neuronautics.recordings.nn_spike import NNSpike
import pandas as pd
import numpy as np


class TestSpike(unittest.TestCase):
    def test_constructor(self):
        mock_ui = MagicMock()
        spike = Spike(ui=mock_ui)
        self.assertIsInstance(spike, AbstractSource)
        self.assertIs(spike.ui, mock_ui)
        self.assertIs(spike.data_handler, NNSpike)

    def test_load_files(self):
        mock_ui = MagicMock()
        files = ['file1.spike', 'file2.spike']
        with patch('glob.glob') as spy_glob:
            spy_glob.return_value = files
            spike = Spike(mock_ui)
            spike.load_files('/random/folder')

            call_args_list = mock_ui.spikeBtn.setEnabled.call_args_list
            self.assertEqual(call_args_list[0].args, (False,))
            self.assertEqual(call_args_list[1].args, (True,))
            self.assertListEqual(spike.filenames, files)

    def test_load_files_empty_folder(self):
        mock_ui = MagicMock()
        files = []
        with patch('glob.glob') as spy_glob:
            spy_glob.return_value = files
            spike = Spike(mock_ui)
            spike.load_files('/random/folder')

            mock_ui.spikeBtn.setEnabled.assert_called_once_with(False)
            self.assertListEqual(spike.filenames, [])

    def test_select_view(self):
        with patch('neuronautics.ui.spike.AbstractSource.select_view') as spy_select_view:
            mock_ui = MagicMock()
            spike = Spike(mock_ui)

            spike.select_view()

            spy_select_view.assert_called_once()
            mock_ui.optionStck.setCurrentWidget.assert_called_once_with(mock_ui.spikeOptPage)

    def test_plot_single_view_stacked(self):
        mock_ui = MagicMock()
        mock_ui.chkSpikeStacked.isChecked.return_value = True
        mock_ui.recording_start_s = 0
        mock_ui.single_chart_view.x_label.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.y_label.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.title.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.plot.return_value = mock_ui.single_chart_view

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        spy_nnspike.to_ms.side_effect = lambda x, _: x + 1
        spy_nnspike.get_channel_data.return_value = pd.DataFrame({'CLASS': [0]*3,
                                                                  'TS': [1, 2, 3],
                                                                  'SPK': [[1, 2], [3, 4], [4, 5]]})

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        spike._plot_single_view(path='/random/file.spike', channel_id=0)

        mock_ui.single_chart_view.x_label.assert_called_once_with('Time (ms)')
        mock_ui.single_chart_view.y_label.assert_called_once_with('Microvolts')
        mock_ui.single_chart_view.title.assert_called_once_with('Channel 0')
        mock_ui.single_chart_view.plot.assert_called_once_with(
            values=[[(0, 1), (1, 2)],
                    [(0, 3), (1, 4)],
                    [(0, 4), (1, 5)]],
            group=[0, 0, 0],
            allow_selection=True,
            xlim=None,
            progress_bar=True
        )

    def test_plot_single_view_timeseries(self):
        mock_ui = MagicMock()
        mock_ui.chkSpikeStacked.isChecked.return_value = False
        mock_ui.recording_start_s = 0
        mock_ui.single_chart_view.x_label.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.y_label.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.title.return_value = mock_ui.single_chart_view
        mock_ui.single_chart_view.plot.return_value = mock_ui.single_chart_view

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        spy_nnspike.to_ms.side_effect = lambda x, _: x + 1
        spy_nnspike.get_channel_data.return_value = pd.DataFrame({'CLASS': [0]*3,
                                                                  'TS': [1, 2, 3],
                                                                  'SPK': [[1, 2], [3, 4], [4, 5]]})

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        spike._plot_single_view(path='/random/file.spike', channel_id=0)

        mock_ui.single_chart_view.x_label.assert_called_once_with('Time (ms)')
        mock_ui.single_chart_view.y_label.assert_called_once_with('Microvolts')
        mock_ui.single_chart_view.title.assert_called_once_with('Channel 0')
        mock_ui.single_chart_view.plot.assert_called_once_with(
            values=[[(1, 1), (2, 2)],
                    [(2, 3), (3, 4)],
                    [(3, 4), (4, 5)]],
            group=[0, 0, 0],
            allow_selection=True,
            xlim=(-1, SINGLE_VIEW_LENGTH_S * 1_000),
            progress_bar=True
        )

    def test_plot_grid_view_stacked(self):
        mock_ui = MagicMock()
        mock_ui.chkSpikeStacked.isChecked.return_value = True
        mock_ui.recording_start_s = 0

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        spy_nnspike.to_ms.side_effect = lambda x, _: x + 1
        spy_nnspike.get_all_data.return_value = pd.DataFrame({'CH_ID': [1, 2, 3],
                                                              'CLASS': [0]*3,
                                                              'TS': [1, 2, 3],
                                                              'SPK': [[1, 2], [3, 4], [4, 5]]})

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        spike._plot_grid_view(path='/random/file.spike')

        expected_values = {
            1: ([[(0, 1), (1, 2)]], [0]),
            2: ([[(0, 3), (1, 4)]], [0]),
            3: ([[(0, 4), (1, 5)]], [0]),
        }
        mock_ui.multiple_chart_view.plot.assert_called_once_with(
            expected_values,
            xlim=None
        )

    def test_plot_grid_view_timeseries(self):
        mock_ui = MagicMock()
        mock_ui.chkSpikeStacked.isChecked.return_value = False
        mock_ui.recording_start_s = 0

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        spy_nnspike.to_ms.side_effect = lambda x, _: x + 1
        spy_nnspike.get_all_data.return_value = pd.DataFrame({'CH_ID': [1, 2, 3],
                                                              'CLASS': [0]*3,
                                                              'TS': [1, 2, 3],
                                                              'SPK': [[1, 2], [3, 4], [4, 5]]})

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        spike._plot_grid_view(path='/random/file.spike')

        expected_values = {
            1: ([[(1, 1), (2, 2)]], [0]),
            2: ([[(2, 3), (3, 4)]], [0]),
            3: ([[(3, 4), (4, 5)]], [0]),
        }
        mock_ui.multiple_chart_view.plot.assert_called_once_with(
            expected_values,
            xlim=(-1, GRID_VIEW_TIMESERIES_S * 1_000),
        )

    def test_plot_list_view_stacked(self):
        mock_ui = MagicMock()
        mock_ui.chkSpikeStacked.isChecked.return_value = True
        mock_ui.recording_start_s = 0

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        spy_nnspike.to_ms.side_effect = lambda x, _: x + 1
        spy_nnspike.get_channel_data.return_value = pd.DataFrame({'CLASS': [0]*3,
                                                                  'TS': [1, 2, 3],
                                                                  'SPK': [[1, 2], [3, 4], [4, 5]]})

        spike = Spike(mock_ui)
        spike.filenames = ['file.spike']
        spike.data_handler = spy_nnspike

        spike._plot_list_view(channel_id=0)

        expected_values = {
            'file': ([[(0, 1), (1, 2)],
                      [(0, 3), (1, 4)],
                      [(0, 4), (1, 5)]], [0, 0, 0]),
        }
        mock_ui.list_chart_view.plot.assert_called_once_with(
            expected_values,
            xlim=None
        )

    def test_plot_list_view_timeseries(self):
        mock_ui = MagicMock()
        mock_ui.chkSpikeStacked.isChecked.return_value = False
        mock_ui.recording_start_s = 0

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        spy_nnspike.to_ms.side_effect = lambda x, _: x + 1
        spy_nnspike.get_channel_data.return_value = pd.DataFrame({'CLASS': [0]*3,
                                                                  'TS': [1, 2, 3],
                                                                  'SPK': [[1, 2], [3, 4], [4, 5]]})

        spike = Spike(mock_ui)
        spike.filenames = ['file.spike']
        spike.data_handler = spy_nnspike

        spike._plot_list_view(channel_id=0)

        expected_values = {
            'file': ([[(1, 1), (2, 2)],
                      [(2, 3), (3, 4)],
                      [(3, 4), (4, 5)]], [0, 0, 0]),
        }
        mock_ui.list_chart_view.plot.assert_called_once_with(
            expected_values,
            xlim=(-1, GRID_VIEW_TIMESERIES_S*1_000)
        )

    def test_all_data(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.currentText.return_value = 'file.spike'

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        expected_df = pd.DataFrame({'CLASS': [0]*3,
                                    'TS': [1, 2, 3],
                                    'SPK': [[1, 2], [3, 4], [4, 5]]})
        spy_nnspike.get_all_data.return_value = expected_df

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        df = spike.all_data()

        spy_nnspike.assert_called_once_with('file.spike')
        spy_nnspike.get_all_data.assert_called_once_with(0, np.Inf)
        pd.testing.assert_frame_equal(df, expected_df)

    def test_all_channel_data(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.currentText.return_value = 'file.spike'
        mock_ui.channelSelector.currentText.return_value = '1'

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        expected_df = pd.DataFrame({'CLASS': [0]*3,
                                    'TS': [1, 2, 3],
                                    'SPK': [[1, 2], [3, 4], [4, 5]]})
        spy_nnspike.get_channel_data.return_value = expected_df

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        df = spike.all_channel_data()

        spy_nnspike.assert_called_once_with('file.spike')
        spy_nnspike.get_channel_data.assert_called_once_with(1, 0, np.Inf)
        pd.testing.assert_frame_equal(df, expected_df)

    def test_run_kmeans(self):
        mock_ui = MagicMock()

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike
        spike._get_kmeans_params = MagicMock()
        spike._get_kmeans_params.return_value = ('file.spike', 0, 2, 10)
        spike.all_channel_data = MagicMock()
        spike.all_channel_data.return_value = 'fake data'
        spike._pca_kmeans = MagicMock()
        spike.plot_single_view = MagicMock()

        spike.run_kmeans()

        spike._pca_kmeans.assert_called_once_with('fake data', 2, 10)
        spike.plot_single_view.assert_called_once()
        spy_nnspike.set_labels.assert_called_once_with(0, spike._pca_kmeans.return_value)

    def test_get_kmeans_params(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.currentText.return_value = 'file.spike'
        mock_ui.channelSelector.currentText.return_value = '123'
        mock_ui.pcaValue.value.return_value = 4
        mock_ui.kValue.value.return_value = 10

        spike = Spike(mock_ui)

        (path, channel_id, num_pca, num_clusters) = spike._get_kmeans_params()

        self.assertEqual(path, 'file.spike')
        self.assertEqual(channel_id, 123)
        self.assertEqual(num_pca, 4)
        self.assertEqual(num_clusters, 10)

    def test_pca_kmeans(self):
        mock_ui = MagicMock()
        arr = [[1, 2, 3], [3, 4, 5]]
        input_df = pd.DataFrame({'spike': arr})

        with patch('neuronautics.ui.spike.SpikeSorter') as spy_spike_sorter:
            spike = Spike(mock_ui)
            labels = spike._pca_kmeans(input_df, 2, 4)

            np.testing.assert_array_equal(spy_spike_sorter.call_args.args[0], arr)
            spy_spike_sorter.return_value.pca.assert_called_once_with(2)
            spy_spike_sorter.return_value.pca.return_value.kmeans.assert_called_once_with(4)
            spy_spike_sorter.return_value.pca.return_value.kmeans.return_value.run.assert_called_once()

            self.assertEqual(labels,
                             spy_spike_sorter.return_value
                                             .pca.return_value
                                             .kmeans.return_value
                                             .run.return_value)

    def test_run_all_kmeans(self):
        mock_ui = MagicMock()

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        input_df = pd.DataFrame({'spike': [[1, 2, 3], [3, 4, 5], [11, 12, 13], [13, 14, 15]],
                                 'channel_id': [0, 0, 1, 1]})
        spy_nnspike.get_all_data.return_value = input_df

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike
        spike._get_kmeans_params = MagicMock()
        spike._get_kmeans_params.return_value = ('file.spike', 0, 2, 10)
        spike._pca_kmeans = MagicMock()
        spike.plot_single_view = MagicMock()
        spike.plot_multiple_view = MagicMock()

        spike.run_all_kmeans()

        called_with_channel_0 = pd.DataFrame({'spike': [[1, 2, 3], [3, 4, 5]],
                                 'channel_id': [0, 0]})

        called_with_channel_1 = pd.DataFrame({'spike': [[11, 12, 13], [13, 14, 15]],
                                 'channel_id': [1, 1]})

        args = spike._pca_kmeans.call_args_list
        pd.testing.assert_frame_equal(args[0].args[0], called_with_channel_0)
        np.testing.assert_array_equal(args[1].args[0].values, called_with_channel_1.values )
        spike.plot_single_view.assert_called_once()
        spike.plot_multiple_view.assert_called_once()
        spy_nnspike.set_labels.assert_called_with(1, spike._pca_kmeans.return_value)

    def test_reset_spike_classes(self):
        mock_ui = MagicMock()

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        input_df = pd.DataFrame({'spike': [[1, 2, 3], [3, 4, 5], [11, 12, 13]]})
        spy_nnspike.get_channel_data.return_value = input_df

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike
        spike._get_kmeans_params = MagicMock()
        spike._get_kmeans_params.return_value = ('file.spike', 0, 2, 10)
        spike.plot_single_view = MagicMock()

        spike.reset_spike_classes()

        spy_nnspike.set_labels.assert_called_once_with(0, [0, 0, 0])
        spike.plot_single_view.assert_called_once()

    def test_signal_unit_changed(self):
        mock_ui = MagicMock()

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike
        input_df = pd.DataFrame({'spike': [[1, 2, 3], [3, 4, 5], [11, 12, 13]],
                                 'ts_ms': [100, 200, 300],
                                 'class': [0, 1, 2]})
        spy_nnspike.get_channel_data.return_value = input_df

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike
        spike._get_kmeans_params = MagicMock()
        spike._get_kmeans_params.return_value = ('file.spike', 0, 2, 10)

        spike.signal_unit_changed([(100, 2), (300, -1)])

        spy_nnspike.set_labels.assert_called_once_with(0, [2, 1, -1])

    def test_save_spikes(self):
        mock_ui = MagicMock()
        mock_ui.fileSelector.currentText.return_value='file.spike'

        spy_nnspike = MagicMock()
        spy_nnspike.return_value = spy_nnspike

        spike = Spike(mock_ui)
        spike.data_handler = spy_nnspike

        spike.save_spikes()

        spy_nnspike.assert_called_once_with('file.spike')
        spy_nnspike.save.assert_called_once()


if __name__ == '__main__':
    unittest.main()
