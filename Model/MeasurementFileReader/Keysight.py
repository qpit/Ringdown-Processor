"""
This module contains routines for processing ringdowns by a zero-span Keysight spectrum analyzer.
"""
import csv
import numpy as np
from datetime import datetime
import os

def valid(path:str) -> bool:
    """
    Tests if the given file is supported by this module.
    :param path: Path to file.
    :return: Returns true if supported.
    """
    # Open file
    valid = False
    with open(path, 'r') as f:
        linenum = 1
        f1 = None
        f2 = None
        try:
            for line in f:
                if linenum == 1 and not line == "Trace\n":
                    break
                elif linenum == 2 and line == "Swept SA\n":
                    valid = True
                    break

                linenum += 1
        except:
            return False

    return valid

def load_data_file(path: str) -> dict:
    """
    Tries to open and process datafile specified by the path string.
    :param path:
    :return:
    """
    # Open file
    with open(path, 'r') as f:
        reader = csv.reader(f)
        csvList = list(reader)

    data = dict()

    # Read key vaules
    row = 0
    f1 = f2 = None
    while csvList[row][0] != "DATA":
        if csvList[row][0] == "Start Frequency":
            f1 = float(csvList[row][1])
        if csvList[row][0] == "Stop Frequency":
            f2 = float(csvList[row][1])
        row += 1
    csvList[row].append("")
    data['frequency'] = (f1+f2)/2

    # Convert measurement data to numpy matrix
    mat = np.array(csvList[row + 1:-1], dtype='float64')

    minThresh = -1000
    for j in range(0, len(mat[:, 1])):
        if mat[j, 1] <= minThresh:
            break

    data['x'] = mat[1:j, 0]  # x data
    data['y'] = mat[1:j, 1]  # dBm data

    # Read file creation date. Use as a guess on when experiment was performed.
    data['datetime'] = datetime.fromtimestamp(os.path.getmtime(path))  # .strftime('%Y-%m-%d %H:%M:%S')

    # Type
    if f1 == f2:
        data['type'] = 'ringdown'
    else:
        data['type'] = 'spectrum'

    return data