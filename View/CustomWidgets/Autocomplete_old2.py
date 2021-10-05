import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QApplication, QCompleter, QCheckBox, QLabel,QLineEdit


def completion(word_list, widget, i=True):
    """ Autocompletion of sender and subject """
    word_set = set(word_list)
    completer = QCompleter(word_set)
    if i:
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    else:
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
    widget.setCompleter(completer)


class Autocomplete(QLineEdit):
    def __init__(self, items:list, parent=None,insensitivity=True):
        super().__init__(parent)
        self.insensitivity = insensitivity
        self.setAutocompletion(items)


    def setAutocompletion(self,items:list):
        self.items = items
        completer = QCompleter(set(self.items))
        if self.insensitivity:
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        else:
            completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
        self.setCompleter(completer)