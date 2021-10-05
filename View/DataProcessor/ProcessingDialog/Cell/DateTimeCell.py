from PyQt5.QtWidgets import QWidget,QDateTimeEdit,QSizePolicy
from PyQt5.QtCore import QDateTime
from .Cell import Cell
from datetime import datetime

SIDE_MARGIN = 2

class DateTimeCell(Cell):
    dtype = 'datetime'

    @property
    def content(self):
        return self.get_content()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, unit='',content_editable=True, **kwargs)


    def ini_value_widget(self) -> QWidget:
        """
        Initializes the widget containing the value
        :return:
        """
        w = _QDateTimeEdit()
        w.dateTimeChanged.connect(self.on_value_change)
        return w

    def get_value(self):
        """
        Returns the cell's value in a suitable data type.
        :return:
        """
        return datetime.fromisoformat(self.w_content.dateTime().toString('yyyy-MM-dd hh:mm:ss'))

    def update_value(self):
        """
        Updates the value in the cell
        :return:
        """
        qdatetime = QDateTime.fromString(str(self.retrieve_value_fcn()), 'yyyy-MM-dd hh:mm:ss')
        self.w_content.setDateTime(qdatetime)

    def on_value_change(self, value):
        """
        Called when the value is changed in the cell. Passes the value to the onValueChange method. DO NOT OVERWRITE
        :param s:
        :return:
        """
        if not self.initializing:
            self.onValueChange(self.get_value())

class _QDateTimeEdit(QDateTimeEdit):
    """
    Identical to QDateTimeEdit, but with scroll wheel deactivated
    """
    def wheelEvent(self, e) -> None:
        pass

