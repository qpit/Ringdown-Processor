from .Cell import Cell,SIDE_MARGIN
from .StringCell import StringCell
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem
from PyQt5.QtGui import QRegExpValidator,QDoubleValidator,QIntValidator

class FloatCell(StringCell):
    dtype = 'float'
    def ini_value_widget_editable(self) -> QWidget:
        """
        Initialized the editable version of the value widget
        :return:
        """
        w = super().ini_value_widget_editable()
        w.setValidator(QDoubleValidator())
        return w

    def value2str(self,value):
        """
        Retrieves value as a suitable string.
        :return:
        """
        return "{:.5g}".format(value)

    def str2value(self,string:str):
        """
        Convert string to a suitable value datatype.
        :param string:
        :return:
        """
        return float(string)

