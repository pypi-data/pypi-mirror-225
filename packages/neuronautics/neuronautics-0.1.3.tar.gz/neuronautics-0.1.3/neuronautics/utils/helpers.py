import os
import numpy as np
import re
from pathlib import Path

import subprocess
import platform


def moving_average(a, n=3) :
    cum_sum = np.cumsum(a, dtype=float)
    cum_sum[n:] = cum_sum[n:] - cum_sum[:-n]

    cum_sum_squares = np.cumsum(a**2, dtype=float)
    cum_sum_squares[n:] = cum_sum_squares[n:] - cum_sum_squares[:-n]

    avg = cum_sum[n-1:] / n
    moving_var = (cum_sum_squares[n-1:] - cum_sum[n-1:]**2 / n) / n
    std = np.sqrt(moving_var)
    return avg, std


def convert_to_array(array_str):
    try:
        # Extract the values from the string using regular expressions
        values = re.findall(r'-?\d+\.\d*', array_str)
        # Convert the values to integers and return as an array
        return np.array([float(value) for value in values])
    except (ValueError, TypeError):
        # Handle the case where the string representation is invalid
        return np.array()


def mkdir(*args):
    path = '/'.join(args)
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def app_path(*args):
    home_path = os.path.expanduser('~')
    return mkdir(home_path, '.neuronautics', *args)


def file_path(fn):
    fn_path = fn.split('/')
    main_folder = app_path(*fn_path[:-1])
    return '/'.join([main_folder, fn_path[-1]])


def load_yaml(filename, default=None):
    import yaml
    if Path(filename).exists():
        with open(filename, 'r') as stream:
            data = yaml.full_load(stream)
            if not data:
                return default
            return data
    else:
        return default


def open_external_editor(filename):
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

