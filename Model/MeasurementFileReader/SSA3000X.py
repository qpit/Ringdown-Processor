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
        try:
            for line in f:
                if linenum == 1 and line == "Machine Module,SSA3021X\n":
                    valid = True
                    break

                if linenum > 20:
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
    while csvList[row][0] != "Trace Data":
        if csvList[row][0] == "Start Frequency":
            f1 = float(csvList[row][1])
        if csvList[row][0] == "Stop Frequency":
            f2 = float(csvList[row][1])
        elif csvList[row][0] == "Number of Points":
            numOfPoints = int(csvList[row][1])
        elif csvList[row][0] == "Sweep Time(s)":
            sweeptime = float(csvList[row][1])
        row += 1
    csvList[row].append("")
    data['frequency'] = (f1 + f2) / 2
    mat = np.array(csvList[row + 1:-1], dtype='float64')

    # Type
    if f1 == f2:
        data['type'] = type = 'ringdown'
    else:
        data['type'] = type = 'spectrum'

    # x-data
    if type == 'ringdown':
        # Time data
        data['x'] = np.linspace(0, sweeptime, num=numOfPoints-1)  # Time data
    else:
        # Frequency data
        data['x'] = mat[:, 0]

    # Load dBm data.
    data['y'] = mat[:, 1]  # dBm data

    # Read file creation date. Use as a guess on when experiment was performed.
    data['datetime'] = datetime.fromtimestamp(os.path.getmtime(path))  # .strftime('%Y-%m-%d %H:%M:%S')


    return data