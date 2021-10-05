from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QDialog,QHBoxLayout,QDialogButtonBox, QFormLayout,QSpinBox,QLineEdit,QLabel,QDoubleSpinBox,QCheckBox

class AddNewPropertyDialogs():
    """
    Starts a series of dialogs for adding a new property.
    """
    def __init__(self):
        """

        """
        self.dtype = None
        self.value = None
        self.unit = None
        self.name = None
        self.success = False

    def start(self):
        """
        Starts the dialogs.
        :return:
        """
        dlg = _ChooseDType()
        dlg.show()
        dlg.exec()

        if dlg.dtype is None:
            return
        self.dtype = dlg.dtype

        if self.dtype == int:
            dlg = DefineInt()
        elif self.dtype == float:
            dlg = DefineFloat()
        elif self.dtype == str:
            dlg = DefineString()
        elif self.dtype == bool:
            dlg = DefineBool()
        dlg.show()
        dlg.exec()

        self.name = dlg.name
        self.value = dlg.value
        self.unit = dlg.unit
        self.success = dlg.is_ok





class _ChooseDType(QDialog):
    def __init__(self):
        self.dtype = None

        super().__init__()

        self.setWindowTitle("Choose datatype for new property")

        layout = QVBoxLayout()

        bt = QPushButton('int')
        bt.clicked.connect(self.chosen_int)
        layout.addWidget(bt)

        bt = QPushButton('float')
        bt.clicked.connect(self.chosen_float)
        layout.addWidget(bt)

        bt = QPushButton('string')
        bt.clicked.connect(self.chosen_string)
        layout.addWidget(bt)

        bt = QPushButton('bool')
        bt.clicked.connect(self.chosen_bool)
        layout.addWidget(bt)

        bt = QPushButton('Cancel')
        bt.clicked.connect(self.chosen_cancel)
        layout.addWidget(bt)

        self.setLayout(layout)

    def chosen_int(self):
        self.dtype = int
        self.close()

    def chosen_float(self):
        self.dtype = float
        self.close()

    def chosen_string(self):
        self.dtype = str
        self.close()

    def chosen_bool(self):
        self.dtype = bool
        self.close()

    def chosen_cancel(self):
        self.close()

class DefineInt(QDialog):
    use_unit = True

    def __init__(self):
        super().__init__()
        self.name = ''
        self.value = 1
        self.unit = ''
        self.is_ok = False

        super().__init__()

        self.setWindowTitle("Add property details")

        self.layout = layout = QFormLayout()

        self.setup_name()
        self.setup_value()
        self.setup_unit()

        bt_cancel = QPushButton('Cancel')
        bt_cancel.clicked.connect(self.cancel)

        bt_ok = QPushButton('Ok')
        bt_ok.clicked.connect(self.ok)

        self.layout.addRow(bt_cancel, bt_ok)

        self.setLayout(layout)

    def setup_name(self):
        self.txtName = QLineEdit()
        self.txtName.setText('Name')
        self.layout.addRow(QLabel(text='Name:'), self.txtName)

    def setup_value(self):
        self.txtValue = QSpinBox()
        self.txtValue.setValue(1)
        self.layout.addRow(QLabel(text='Value:'), self.txtValue)

    def setup_unit(self):
        self.txtUnit = QLineEdit()
        self.txtUnit.setText('')
        self.layout.addRow(QLabel(text='Unit:'), self.txtUnit)

    def cancel(self):
        self.close()

    def ok(self):
        self.name = self.txtName.text().strip()
        self.unit = self.txtUnit.text().strip()
        self.value = int(self.txtValue.value())
        self.is_ok = True
        self.close()


class DefineFloat(DefineInt):
    def setup_value(self):
        self.txtValue = QDoubleSpinBox()
        self.txtValue.setValue(1)
        self.layout.addRow(QLabel(text='Value:'), self.txtValue)

    def ok(self):
        self.name = self.txtName.text().strip()
        self.unit = self.txtUnit.text().strip()
        self.value = float(self.txtValue.value())
        self.is_ok = True
        self.close()

class DefineString(DefineInt):
    def setup_value(self):
        self.txtValue = QLineEdit()
        self.txtValue.setText('Name')
        self.layout.addRow(QLabel(text='Value:'), self.txtValue)

    def setup_unit(self):
        pass

    def ok(self):
        self.name = self.txtName.text().strip()
        self.value = str(self.txtValue.text().strip())
        self.is_ok = True
        self.close()

class DefineBool(DefineString):
    def setup_value(self):
        self.txtValue = QCheckBox()
        self.layout.addRow(QLabel(text='Value:'), self.txtValue)

    def ok(self):
        self.name = self.txtName.text().strip()
        self.value = bool(self.txtValue.isChecked())
        self.is_ok = True
        self.close()