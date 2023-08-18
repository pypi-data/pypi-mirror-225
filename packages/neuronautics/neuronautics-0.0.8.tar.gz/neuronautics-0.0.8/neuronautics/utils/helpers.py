import os
import numpy as np
import re
from pathlib import Path

import subprocess
import platform
import yaml


def moving_stats(array: np.array, window: int = 3) -> (float, float):
    """
    Calculate the moving average and standard deviation of a sequence.

    This function calculates the moving average and moving standard deviation of
    a given sequence using a specified window size.

    Args:
        array (np.array): Input sequence for which the moving average and
            standard deviation need to be calculated.
        window (int, optional): Window size for the moving average and standard
            deviation calculation. Defaults to 3.

    Returns:
        tuple: A tuple containing two arrays representing the calculated
            moving average and moving standard deviation.

    Raises:
        ValueError: If the window size `window` is not a positive integer or if it
            exceeds the length of the input sequence `array`.

    Examples:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> avg, std = moving_stats(data, window=3)
        >>> print(avg)
        [ 2.  3.  4.  5.  6.  7.  8.  9.]
        >>> print(std)
        [ 0.81649658  0.81649658  0.81649658  0.81649658  0.81649658  0.81649658]
    """

    if (array is None) or (len(array) < window):
        raise ValueError("array must be longer than window size")

    if window < 3:
        raise ValueError("window must be greater than or equal to 3")

    cum_sum = np.cumsum(array, dtype=float)
    cum_sum[window:] = cum_sum[window:] - cum_sum[:-window]

    cum_sum_squares = np.cumsum(array ** 2, dtype=float)
    cum_sum_squares[window:] = cum_sum_squares[window:] - cum_sum_squares[:-window]

    avg = cum_sum[window - 1:] / window
    moving_var = (cum_sum_squares[window - 1:] - cum_sum[window - 1:] ** 2 / window) / window
    std = np.sqrt(moving_var)
    return avg, std


def parse_numeric_array(array_str: str) -> np.array:
    """
    Convert a string representation of an array to a NumPy array.

    This function takes a string representation of an array and extracts the
    numerical values to create a NumPy array.

    Args:
        array_str (str): A string containing numerical values separated by
            non-numeric characters.

    Returns:
        numpy.ndarray: A NumPy array containing the extracted numerical values.

    Raises:
        None

    Examples:
        >>> input_str = "[1.2, 3.4, -5.6, 7.8]"
        >>> result_array = parse_numeric_array(input_str)
        >>> print(result_array)
        array([ 1.2,  3.4, -5.6,  7.8])
    """
    try:
        # Extract the values from the string using regular expressions
        values = re.findall(r'-?\d+\.\d*', array_str)
        # Convert the values to integers and return as an array
        return np.array([float(value) for value in values])
    except (ValueError, TypeError):
        # Handle the case where the string representation is invalid
        return np.array([])


def mkdir(*args):
    """
    Create a directory and its parent directories if they do not exist.

    This function constructs a directory path by joining the provided
    arguments and then creates the directory along with any necessary parent
    directories if they do not already exist.

    Args:
        *args: Variable number of string arguments that represent the path
            segments for the directory to be created.

    Returns:
        str: The path of the created directory.

    Raises:
        None

    Examples:
        >>> new_directory = mkdir('path', 'to', 'my', 'directory')
        >>> print(new_directory)
        'path/to/my/directory'
        >>> existing_directory = mkdir('path', 'to', 'existing', 'directory')
        >>> print(existing_directory)
        'path/to/existing/directory'
    """
    path = '/'.join(args)
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def app_path(*args):
    """
    Create a path within the application's directory structure.

    This function constructs a path within the application's directory
    structure by appending the provided arguments to the application's base
    directory. The base directory is typically located in the user's home
    directory and is used to organize application-specific files.

    Args:
        *args: Variable number of string arguments that represent the
            subdirectories to be added to the application path.

    Returns:
        str: The path within the application's directory structure.

    Raises:
        None

    Examples:
        >>> app_subpath = app_path('data', 'config')
        >>> print(app_subpath)
        '/home/user/.neuronautics/data/config'
    """
    home_path = os.path.expanduser('~')
    return mkdir(home_path, '.neuronautics', *args)


def file_path(fn: str) -> str:
    """
    Create a full file path within the application's directory structure.

    This function constructs a full file path within the application's directory
    structure by combining the base directory obtained from the `app_path`
    function with the provided file name.

    Args:
        fn (str): The file name or relative file path to be added to the
            application path.

    Returns:
        str: The full file path within the application's directory structure.

    Raises:
        None

    Examples:
        >>> file = 'data/settings.json'
        >>> full_file_path = file_path(file)
        >>> print(full_file_path)
        '/home/user/.neuronautics/data/settings.json'
    """
    fn_path = fn.split('/')
    main_folder = app_path(*fn_path[:-1])
    return '/'.join([main_folder, fn_path[-1]])


def load_yaml(filename, default=None):
    """
    Load YAML data from a file.

    This function reads YAML data from a specified file and returns the loaded
    data as a Python dictionary. If the file does not exist or cannot be read,
    the function returns the specified default value.

    Args:
        filename (str): The path to the YAML file to be loaded.
        default (any, optional): The default value to return if the file does
            not exist or cannot be read. Defaults to None.

    Returns:
        dict or any: A dictionary containing the loaded YAML data if the file
            exists and can be read, or the specified default value otherwise.

    Raises:
        None

    Examples:
        >>> yaml_file = 'config/settings.yaml'
        >>> config_data = load_yaml(yaml_file, default={})
        >>> print(config_data)
        {'key': 'value', 'nested': {'nested_key': 'nested_value'}}
    """
    if Path(filename).exists():
        with open(filename, 'r') as stream:
            data = yaml.full_load(stream)
            if not data:
                return default
            return data
    else:
        return default


def open_external_editor(filename):
    """
    Open a file in an external text editor based on the operating system.

    This function attempts to open a specified file in an external text editor
    based on the user's operating system. It supports Windows, Linux, and macOS.

    Args:
        filename (str): The path to the file to be opened.

    Returns:
        None

    Raises:
        None

    Examples:
        >>> open_external_editor('example.txt')
        # Opens 'example.txt' in the default text editor based on the OS
    """
    system = platform.system()
    editor_commands = {
        "Windows": ["code", "notepad"],
        "Linux": ["code", "xdg-open"],
        "Darwin": ["code", "open -a TextEdit"]
    }

    editors = editor_commands.get(system)
    if editors:
        for editor in editors:
            try:
                subprocess.run([editor, filename], check=True)
                break  # Opened successfully, no need to try other editors
            except subprocess.CalledProcessError:
                pass
        else:
            print("Unable to open the file in any editor.")
    else:
        print("Unsupported operating system.")

