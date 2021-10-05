from .Cell import Cell
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem,QSizePolicy,QApplication
from PyQt5.QtCore import Qt,QObject,QEvent,QTimer,pyqtSignal
from PyQt5 import QtGui
from .StringCell import StringCell
from View.CustomWidgets import Autocomplete

class ListCell(StringCell):
    dtype = 'string'

    def __init__(self,*args,get_items_fcn = None,**kwargs):
        self.get_items_fcn = get_items_fcn or (lambda: [])
        super().__init__(*args,content_editable=True,unit='',**kwargs)


    def ini_value_widget_editable(self) -> QWidget:
        """
        Initialized the editable version of the value widget
        :return:
        """
        w = Autocomplete(items=self.get_items_fcn(),parent=self)
        w.currentTextChanged.connect(self.on_value_change)
        #w.textChanged.connect(self.on_value_change)

        return w

    def get_value(self):
        return self.str2value(self.w_content.currentText())

    def update_value_editable(self,value):
        """
        Updates value for an editable cell.
        :param value:
        :return:
        """
        self.w_content.setCurrentText(self.value2str(value))




    def update_completer(self):
        """
        Updates the auto completer
        :return:
        """
        self.w_content.updateAutocompletion(self.get_items_fcn())