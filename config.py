"""
This module contains IO for a config file storing basic parameters
"""
import pathlib

CONFIG_FILE_NAME = "config.txt"
DELIMITER = " = "

def save_parameter(name,value):
    d = _open_file()
    d[name] = value
    _save_file(d)

def load_parameter(name):
    d = _open_file()
    if name in d:
        return d[name]
    return None

def _open_file() -> dict:
    """
    Opens file and returns dictionary of parameter-value pairs.
    :return:
    """
    path = pathlib.Path(CONFIG_FILE_NAME)
    d = {}
    if not path.exists():
        return d
    with open(path,'r') as f:
        for line in f:
            if line:
                args = line.split(DELIMITER)
                key = args[0]
                value = args[1]
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        if value.lower() == 'true':
                            value = True
                        elif value.lower() == 'false':
                            value = False
                d[key] = value
    return d

def _save_file(d:dict):
    path = pathlib.Path(CONFIG_FILE_NAME)
    with open(path, 'w') as f:
        for key,value in d.items():
            f.write(key + DELIMITER + str(value) + "\n")

