import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QApplication, QCompleter, QCheckBox, QLabel


def completion(word_list, widget, i=True):
    """ Autocompletion of sender and subject """
    word_set = set(word_list)
    completer = QCompleter(word_set)
    if i:
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    else:
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
    widget.setCompleter(completer)


class Autocomplete(QComboBox):
    def __init__(self, items:list, parent=None,insensitivity=True,activate_scroll_wheel = False):
        super().__init__(parent)
        self.insensitivity = insensitivity
        self.setEditable(True)
        self.setDuplicatesEnabled(False)
        self.setAutocompletion(items)
        self.activate_scroll_wheel = activate_scroll_wheel


    def setAutocompletion(self,items:list):
        self.clear()
        self.items = items
        self.addItems(self.items)
        self._setup_completer()

    def updateAutocompletion(self, items:list):
        for item in items:
            if not item in self.items:
                self.addItem(item)
                self.items.append(item)
        self._setup_completer()

    def _setup_completer(self):
        completer = QCompleter(set(self.items))
        if self.insensitivity:
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        else:
            completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
        self.setCompleter(completer)

    def wheelEvent(self, e) -> None:
        if self.activate_scroll_wheel:
            super().wheelEvent(e)