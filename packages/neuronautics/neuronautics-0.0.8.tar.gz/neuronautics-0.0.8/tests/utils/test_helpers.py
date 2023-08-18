import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from numpy import testing
from neuronautics.utils.helpers import (moving_stats, parse_numeric_array,
                                        mkdir, app_path, file_path, load_yaml,
                                        open_external_editor)


class HelpersTest(unittest.TestCase):
    def test_moving_stats(self):
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        expected_avg = np.array([2., 3., 4., 5., 6., 7., 8., 9.])
        expected_std = np.array([0.816496580927726]*8)

        avg, std = moving_stats(data, window=3)

        testing.assert_array_equal(avg, expected_avg)
        testing.assert_array_equal(std, expected_std)

    def test_moving_stats_insufficient_data(self):
        data = np.array([])

        with self.assertRaises(ValueError) as context:
            _ = moving_stats(data, window=3)
            self.assertTrue('array must be longer' in context.exception)

    def test_moving_stats_empty_data(self):
        data = None

        with self.assertRaises(ValueError) as context:
            _ = moving_stats(data, window=3)
            self.assertTrue('array must be longer' in context.exception)

    def test_moving_stats_small_window(self):
        data = np.array([1, 2, 3])

        with self.assertRaises(ValueError) as context:
            _ = moving_stats(data, window=2)
            self.assertTrue('window must be greater' in context.exception)

    def test_parse_numeric_array(self):
        input_str = "[  0. -0.29   0.72,   -100.  100. ]"
        expected_array = [0., -0.29, 0.72, -100.,  100.]

        array = parse_numeric_array(input_str)

        testing.assert_array_equal(array, expected_array)

    def test_parse_numeric_array_empty_array(self):
        input_str = "[  ]"
        expected_array = []

        array = parse_numeric_array(input_str)

        testing.assert_array_equal(array, expected_array)

    def test_parse_numeric_array_no_brackets(self):
        input_str = "0. -0.29   0.72   -100.  100."
        expected_array = [0., -0.29, 0.72, -100.,  100.]

        array = parse_numeric_array(input_str)

        testing.assert_array_equal(array, expected_array)

    def test_parse_numeric_array_error(self):
        input_str = [1,2,3]
        expected_array = []

        array = parse_numeric_array(input_str)

        testing.assert_array_equal(array, expected_array)

    def test_mkdir(self):
        with patch('neuronautics.utils.helpers.Path') as spy_path:
            mock_path_instance = MagicMock()
            spy_path.return_value = mock_path_instance

            mock_path_instance.mkdir.return_value = None
            new_directory = mkdir('path', 'to', 'my', 'test_directory')

            self.assertEqual(new_directory, 'path/to/my/test_directory')
            spy_path.assert_called_once_with('path/to/my/test_directory')
            mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    def test_app_path(self):
        with (patch('neuronautics.utils.helpers.mkdir') as spy_mkdir,
              patch('neuronautics.utils.helpers.os.path.expanduser') as spy_os_path):
            spy_os_path.return_value = '/home/fakeuser'
            spy_mkdir.return_value = 'mkdir output'

            directory = app_path('folder1')

            spy_mkdir.assert_called_once_with('/home/fakeuser', '.neuronautics', 'folder1')
            self.assertEqual(directory, 'mkdir output')

    def test_file_path(self):
        with patch('neuronautics.utils.helpers.app_path') as spy_app_path:
            spy_app_path.return_value = '/app/path/extra/path/to'

            filepath = file_path('extra/path/to/file.txt')

            spy_app_path.assert_called_once_with('extra', 'path', 'to')
            self.assertEqual(filepath, '/app/path/extra/path/to/file.txt')

    def test_load_yaml_file_not_found(self):
        with patch('neuronautics.utils.helpers.Path') as spy_path:
            mock_path_instance = MagicMock()
            spy_path.return_value = mock_path_instance
            mock_path_instance.exists.return_value = False

            content = load_yaml('random.yml', 'expected output')

            self.assertEqual(content, 'expected output')

    def test_load_yaml_file_found(self):
        with (patch('neuronautics.utils.helpers.Path') as spy_path,
              patch('builtins.open') as spy_open,
              patch('yaml.full_load') as spy_yaml):
            mock_path_instance = MagicMock()
            spy_path.return_value = mock_path_instance
            mock_path_instance.exists.return_value = True

            spy_open = MagicMock()
            spy_open.return_value = 'stream'
            spy_yaml.return_value = {'random': 'dict'}

            content = load_yaml('random.yml', 'unexpected output')

            spy_path.assert_called_once_with('random.yml')

            self.assertDictEqual(content, {'random': 'dict'})

    def test_load_yaml_file_empty_data(self):
        with (patch('neuronautics.utils.helpers.Path') as spy_path,
              patch('builtins.open') as spy_open,
              patch('yaml.full_load') as spy_yaml):
            mock_path_instance = MagicMock()
            spy_path.return_value = mock_path_instance
            mock_path_instance.exists.return_value = True

            spy_open = MagicMock()
            spy_open.return_value = 'stream'
            spy_yaml.return_value = None

            content = load_yaml('random.yml', 'expected output')

            spy_path.assert_called_once_with('random.yml')

            self.assertEqual(content, 'expected output')

    def test_open_external_editor_existing_os(self):
        with (patch('platform.system') as spy_system,
              patch('subprocess.run') as spy_run):
            spy_system.return_value = 'Windows'

            open_external_editor('random.txt')

            spy_run.assert_called_with(['code', 'random.txt'], check=True)

    def test_open_external_editor_unknown_os(self):
        with (patch('platform.system') as spy_system,
              patch('subprocess.run') as spy_run,
              patch('builtins.print') as spy_print):
            spy_system.return_value = 'Android'

            open_external_editor('random.txt')

            spy_run.assert_not_called()
            spy_print.assert_called_once_with("Unsupported operating system.")

    def test_open_external_editor_unable_to_open(self):
        import subprocess
        with (patch('platform.system') as spy_system,
              patch('subprocess.run') as spy_run,
              patch('builtins.print') as spy_print):
            spy_system.return_value = 'Linux'
            spy_run.side_effect = subprocess.CalledProcessError(returncode=1, cmd='mock command')

            open_external_editor('random.txt')

            spy_run.assert_any_call(['xdg-open', 'random.txt'], check=True)
            spy_print.assert_called_once_with("Unable to open the file in any editor.")




if __name__ == '__main__':
    unittest.main()
