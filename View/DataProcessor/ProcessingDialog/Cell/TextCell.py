from .Cell import Cell
from .StringCell import StringCell
from PyQt5.QtWidgets import QWidget,QTextEdit,QSizePolicy

class TextCell(StringCell):
    """
    A multiline cell for large texts.
    """
    value_sizepolicy_v = QSizePolicy.MinimumExpanding
    value_sizepolicy_h = QSizePolicy.Expanding

    def ini_value_widget_editable(self) -> QWidget:
        """
        Initialized the editable version of the value widget
        :return:
        """
        w = QTextEdit(self)
        w.textChanged.connect(self.on_value_change)
        w.setMaximumHeight(60)
        return w


    def on_value_change(self):
        super().on_value_change(self.get_value())

    def get_value(self):
        return self.w_content.toPlainText()