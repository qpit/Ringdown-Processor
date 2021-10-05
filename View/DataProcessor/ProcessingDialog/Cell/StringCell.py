from .Cell import Cell,SIDE_MARGIN
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem,QSizePolicy
from PyQt5.QtCore import pyqtSignal,QEvent,Qt

class StringCell(Cell):
    dtype = 'string'
    signal_newentry = pyqtSignal(Cell)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.changed = False

    def ini_value_widget(self) -> QWidget:
        if self.content_editable:
            w = self.ini_value_widget_editable()
            w.setFocusPolicy(Qt.StrongFocus)
            w.installEventFilter(self)
            w.setContentsMargins(0, 0, 0, 0)
        else:
            w = self.ini_value_widget_noneditable()
            w.setContentsMargins(SIDE_MARGIN, SIDE_MARGIN, SIDE_MARGIN, SIDE_MARGIN)
        return w

    def ini_value_widget_editable(self) -> QWidget:
        """
        Initialized the editable version of the value widget
        :return:
        """
        w = QLineEdit(self)
        w.textChanged.connect(self.on_value_change)
        return w

    def ini_value_widget_noneditable(self) -> QWidget:
        """
        Initialized the ini_value_widget_noneditable version of the value widget
        :return:
        """
        return QLabel()

    def get_value(self):
        return self.str2value(self.w_content.text())

    def update_value(self):
        if self.content_editable:
            self.update_value_editable(self.retrieve_value_fcn())
        else:
            self.update_value_noneditable(self.retrieve_value_fcn())

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
        return string

    def update_value_editable(self,value):
        """
        Updates value for an editable cell.
        :param value:
        :return:
        """
        self.w_content.setText(self.value2str(value))

    def update_value_noneditable(self,value):
        """
        Updates value for a noneditable cell.
        :param value:
        :return:
        """
        self.w_content.setText(self.value2str(value))

    def on_value_change(self, string):
        """
        Called when the value is changed in the cell. Passes the value to the onValueChange method. DO NOT OVERWRITE
        :param s:
        :return:
        """
        if not self.initializing:
            self.changed = True
            try:
                self.onValueChange(self.str2value(string))
            except ValueError:
                pass

    def keyPressEvent(self, event):
        """
        :param event:
        :return:
        """
        if event.key() in [Qt.Key_Return,Qt.Key_Enter]:
            self._done_edit()
        super().keyPressEvent(event)

    def eventFilter(self, widget, event):
        b = super().eventFilter(widget,event)
        if event.type() == QEvent.FocusOut:
            self._done_edit()
        return b

    def _done_edit(self):
        """
        Called when a major edit is done
        :return:
        """
        if self.changed:
            self.signal_newentry.emit(self)
            self.changed = False