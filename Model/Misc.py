"""Contains a number of common functions used through the app"""
import numpy as np

# http://www.sengpielaudio.com/calculator-volt.htm
P0 = 1e-3 # [W] Reference power.
R0 = 50 # [Ohm] Reference impedance.
def dBm2P(dBm:float)->float:
    """
    Converts value from dBm to power
    :param dBm:
    :return:
    """
    return P0*np.power(10,dBm/10)

def P2dBm(P:float)->float:
    """
    Converts value from power to dBm
    :param P:
    :return:
    """
    return 10*np.log10(P/P0)

def dBm2V(dBm:float)->float:
    """
    Converts value from dBm to voltage
    :param dBm:
    :return:
    """
    P = dBm2P(dBm)
    return np.sqrt(P*R0)

def V2dBm(V:float)->float:
    """
    Converts value from voltage to dBm
    :param V:
    :return:
    """
    P = np.square(V)/R0
    return P2dBm(P)
