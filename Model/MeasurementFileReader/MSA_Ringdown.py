"""
This module contains routines for processing ringdowns by a zero-span Keysight spectrum analyzer.
"""
import csv
import numpy as np
from datetime import datetime
import os
import re

def valid(path:str) -> bool:
    """
    Tests if the given file is supported by this module.
    :param path: Path to file.
    :return: Returns true if supported.
    """
    # Open file
    with open(path, 'r') as f:
        linenum = 1
        try:
            for line in f:
                strings = line.split(':')
                if linenum == 1 and len(strings) == 2:
                    if not strings[0] == "% Module" and not strings[1] == " DAQ, ID":
                        return False
                else:
                    return False
                if linenum == 2 and strings[0] == "% Devices":
                    return True

                if linenum > 20:
                    return False

                linenum += 1
        except:
            return False

    return False

def load_data_file(path: str) -> dict:
    """
    Tries to open and process datafile specified by the path string.
    :param path:
    :return:
    """
    # Open file
    with open(path, 'r') as f:
        reader = csv.reader(f,delimiter=';')
        csvList = list(reader)

    data = dict()

    # Read key vaules
    unit_time = None
    unit_amplitude = None
    row = 0
    while csvList[row][0][0] == "%":
        if csvList[row][0][0:8] == "% Time: ":
            # Timestamp of measurement.
            s = csvList[row][0][8:-1]
            data['datetime'] = datetime.strptime(s,'%Y/%m/%d %H:%M:%S')
        if csvList[row][0][0:7] == "% Time ":
            def fun(s:str)->str:
                l = s.split('(')
                l = l[-1].split(')')
                return l[0]

            l = csvList[row][0].split(',')
            # Time unit
            unit_time = fun(l[0])

            # Amplitude unit
            unit_amplitude = fun(l[1])

        row += 1
    csvList[row].append("")

    # Convert measurement data to numpy matrix
    mat = np.array(csvList[row + 1:-1], dtype='float64')

    if unit_time == "s":
        data['x'] = mat[:, 0]  # Time data
    else:
        raise Exception('Unrecognized time unit.')

    if unit_amplitude == "dBm":
        data['y'] = mat[:, 1]  # dBm data
    elif unit_amplitude == "V":
        data['y'] = 10 + 20*np.log10(mat[:, 1])
    else:
        raise Exception("Unrecognized amplitude unit.")

    # Read file creation date. Use as a guess on when experiment was performed.
    data['datetime'] = datetime.fromtimestamp(os.path.getmtime(path))  # .strftime('%Y-%m-%d %H:%M:%S')

    data['type'] = 'ringdown'

    return data