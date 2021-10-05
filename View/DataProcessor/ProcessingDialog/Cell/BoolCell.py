from .Cell import Cell
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem,QApplication
from PyQt5.QtCore import Qt
from View.CustomWidgets import Spacer

class BoolCell(Cell):
    dtype = 'bool'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,unit='',**kwargs)

    def ini_value_widget(self):
        w = QCheckBox()
        if not self.content_editable:
            w.setEnabled(False)

        w.setContentsMargins(5, 5, 5, 5)
        w.stateChanged.connect(self.on_value_change)
        # _layout = QHBoxLayout()
        # self.layoutL.addLayout(_layout)
        # _layout.addItem(Spacer('h'))
        # _layout.addWidget(w)
        # _layout.addItem(Spacer('h'))
        return w

    def get_value(self):
        return self.w_content.isChecked()

    def update_value(self):
        value = self.retrieve_value_fcn()
        self.w_content.setChecked(value)

    def on_value_change(self,value):
        super().on_value_change(value==2)

        ''' Add possibility to check all rows at the same time. '''
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            # SHIFT pressed. Apply change throughout all rows.
            self.signal_apply_all_rows.emit(self)