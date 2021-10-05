from .Cell import Cell
from .StringCell import StringCell
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem
from PyQt5.QtGui import QRegExpValidator,QDoubleValidator,QIntValidator

class IntCell(StringCell):
    dtype = 'int'
    def ini_value_widget_editable(self) -> QWidget:
        """
        Initialized the editable version of the value widget
        :return:
        """
        w = super().ini_value_widget_editable()
        w.setValidator(QIntValidator())
        return w

    def value2str(self,value):
        """
        Retrieves value as a suitable string.
        :return:
        """
        return str(value)

    def str2value(self,string:str):
        """
        Convert string to a suitable value datatype.
        :param string:
        :return:
        """
        return int(string)

