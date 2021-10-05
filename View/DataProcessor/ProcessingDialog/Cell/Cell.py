from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem,QSizePolicy,QApplication
from .OverlayedDeleteButton import OverlayedDeleteButton
from PyQt5.QtCore import pyqtSignal,Qt
from View.CustomWidgets import Spacer


SIDE_MARGIN = 3

class Cell(QWidget):
    """
    Base class for a cell in a measurement row.
    """
    dtype = ''
    value_sizepolicy_h = QSizePolicy.Fixed
    value_sizepolicy_v = QSizePolicy.Fixed

    @property
    def value(self):
        return self.get_value()

    @value.setter
    def value(self,value):
        self.set_value(value)

    signal_delete = pyqtSignal(QWidget)
    signal_apply_all_rows = pyqtSignal(QWidget)

    def __init__(self,
                 name='',
                 unit='',
                 retrieve_value_fcn=None,
                 content_editable = True,
                 onValueChange=None,
                 deletable=False):
        """

        :param name:
        :param unit:
        :param retrieve_value_fcn: Must be a method used for retrieving content
        :param content_editable:
        :param multiline:
        :param onValueChange: Called when value has a valid change, with the new value being passed.
        """
        self.initializing = True

        self.name = name
        self.unit = unit
        self.retrieve_value_fcn = retrieve_value_fcn or (lambda: '')
        self.content_editable = content_editable
        self.onValueChange = onValueChange or (lambda s: None)
        self.dtype = None
        self.deletable = deletable

        super().__init__()
        self.w_content = None # Widget containing content.
        self.inigui()
        self.update_value()

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        if not self.w_content is None:
            self.w_content.setSizePolicy(self.value_sizepolicy_h, self.value_sizepolicy_v)

        self.initializing = False


    def inigui(self):
        """
        Initialize widget gui.
        :return:
        """
        layout0 = QVBoxLayout()
        layout0.setContentsMargins(0, 0, 0, 0)
        layout0.setSpacing(0)
        self.setLayout(layout0)

        ''' Upper layout '''
        layoutU = QHBoxLayout()
        layoutU.setContentsMargins(0, 0, 0, 0)
        layoutU.setSpacing(0)
        layout0.addLayout(layoutU)

        # Name
        w = QLabel(text=self.name)
        w.setContentsMargins(SIDE_MARGIN, 0, SIDE_MARGIN, 0)
        layoutU.addWidget(w)


        ''' Lower layout '''
        self.layoutL = layoutL = QHBoxLayout()
        layoutL.setContentsMargins(0, 0, 0, 0)
        layoutL.setSpacing(0)
        layout0.addLayout(layoutL)

        # Value
        self.w_content = w = self.ini_value_widget()
        self.layoutL.addWidget(w)

        # Unit
        if len(self.unit):
            w = self.ini_unit_widget()
            self.layoutL.addWidget(w)

        ''' Rest '''
        # Spacer
        layout0.addItem(Spacer('v'))

        # Delete button
        self.bt_delete = None
        if self.deletable:
            self.bt_delete = OverlayedDeleteButton(self)
            self.bt_delete.clicked.connect(self._delete)

    def ini_value_widget(self) -> QWidget:
        """
        Initializes the widget containing the value
        :return:
        """
        raise NotImplementedError()

    def ini_unit_widget(self) -> QWidget:
        """
        Initializes the widget containing the unit
        :return:
        """
        w = QLabel(text=self.unit)
        w.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)
        w.setContentsMargins(SIDE_MARGIN, SIDE_MARGIN, SIDE_MARGIN, SIDE_MARGIN)
        return w

    def get_value(self)->object:
        """
        Returns the cell's value in a suitable data type.
        :return:
        """
        raise NotImplementedError()

    def set_value(self,o:object):
        """
        Sets both gui and measurement-object value.
        :return:
        """
        self.onValueChange(o)
        self.update_value()

    def update_value(self):
        """
        Updates the value in the cell
        :return:
        """
        raise NotImplementedError()

    def on_value_change(self, value):
        """
        Called when the value is changed in the cell. Passes the value to the onValueChange method. DO NOT OVERWRITE
        :param s:
        :return:
        """
        if not self.initializing:
            self.onValueChange(value)

    def _delete(self):
        """
        Delete itself
        :return:
        """
        self.signal_delete.emit(self)
        self.deleteLater()

    def delete(self):
        """
        Delete itself.
        :return:
        """
        self._delete()

    def keyPressEvent(self, event):
        """
        For Enter+Shift send signal to apply value across all rows.
        :param event:
        :return:
        """
        if event.key() in [Qt.Key_Return,Qt.Key_Enter]:
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.ShiftModifier:
                # ENTER + SHIFT pressed. Apply change throughout the column.
                self.signal_apply_all_rows.emit(self)
        super().keyPressEvent(event)

