from View.windowtemplate import WindowTemplate
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QDialog,QHBoxLayout,QDialogButtonBox, QFormLayout,QSpinBox,QLineEdit,QLabel,QDoubleSpinBox,QCheckBox,QRadioButton,QComboBox
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator
from View.CustomWidgets import Autocomplete
from Model import Model
from PyQt5.QtGui import QDoubleValidator,QIntValidator
from Model.Property import Property

class AddNewPropertyDialog(WindowTemplate):
    """
    Dialog for defining new property. It suggests previously used properties when possible to streamline definitions.
    """
    windowtitle = "Define new property"

    def __init__(self,model:Model):
        self.model = model
        self.newproperty = None
        self.add2all = False
        super().__init__()

    def inigui(self):
        self.layout0 = layout0 = QVBoxLayout()
        self.setLayout(layout0)

        self._inigui_name()
        self._inigui_dtype()
        self._inigui_buttons()

        if self.properties:
            self.txt_name.setCurrentIndex(0)
        else:
            self.txt_name.setCurrentText('var')


    def _inigui_name(self):
        layout_name = QHBoxLayout()
        self.layout0.addLayout(layout_name)

        self.lbl_name = QLabel('Name')
        layout_name.addWidget(self.lbl_name)

        self.properties = self.model.properties
        self.txt_name = Autocomplete([p.name for p in self.properties])
        self.txt_name.currentIndexChanged.connect(self._new_paramter_selected)

        re = QRegularExpression('\\S+')
        validator = QRegularExpressionValidator(re)
        self.txt_name.setValidator(validator)
        layout_name.addWidget(self.txt_name)

    def _inigui_dtype(self):
        # Ini layouts
        layout_dtype = QFormLayout()
        self.layout0.addLayout(layout_dtype)

        self._inigui_value()

        # Ini radio buttons
        self.rd_int = QRadioButton(self)
        layout_dtype.addRow('Integer',self.rd_int)
        self.rd_int.toggled.connect(self._int_selected)

        self.rd_float = QRadioButton(self)
        layout_dtype.addRow('Float', self.rd_float)
        self.rd_float.toggled.connect(self._float_selected)

        self.rd_str = QRadioButton(self)
        layout_dtype.addRow('String', self.rd_str)
        self.rd_str.toggled.connect(self._str_selected)

        self.rd_bool = QRadioButton(self)
        layout_dtype.addRow('Boolean', self.rd_bool)
        self.rd_bool.toggled.connect(self._bool_selected)

        self.rd_float.setChecked(True)
        self.selected = 'float'

    def _inigui_value(self):
        layout_value = QVBoxLayout()
        self.layout0.addLayout(layout_value)

        ''' Int '''
        # Value
        self.lbl_int_value = w = QLabel('Value')
        layout_value.addWidget(w)

        self.txt_int_value = w = QLineEdit()
        w.setText('0')
        validator = QIntValidator(w)
        w.setValidator(validator)
        layout_value.addWidget(w)

        # Unit
        self.lbl_int_unit = w = QLabel('Unit')
        layout_value.addWidget(w)

        self.txt_int_unit = w = QLineEdit()
        w.setText('')
        re = QRegularExpression('\\S+')
        validator = QRegularExpressionValidator(re)
        w.setValidator(validator)
        layout_value.addWidget(w)

        ''' Float '''
        # Value
        self.lbl_float_value = w = QLabel('Value')
        layout_value.addWidget(w)

        self.txt_float_value = w = QLineEdit()
        w.setText('0.0')
        validator = QDoubleValidator(w)
        w.setValidator(validator)
        layout_value.addWidget(w)

        # Unit
        self.lbl_float_unit = w = QLabel('Unit')
        layout_value.addWidget(w)

        self.txt_float_unit = w = QLineEdit()
        w.setText('')
        re = QRegularExpression('\\S+')
        validator = QRegularExpressionValidator(re)
        w.setValidator(validator)
        layout_value.addWidget(w)

        ''' String '''
        self.lbl_str_value = w = QLabel('Value')
        layout_value.addWidget(w)

        self.txt_str_value = w = QLineEdit()
        w.setText('item')
        layout_value.addWidget(w)

        ''' Boolean '''
        self.lbl_bool_value = w = QLabel('Value')
        layout_value.addWidget(w)

        self.txt_bool_value = w = QCheckBox()
        layout_value.addWidget(w)

    def _hideall(self):
        l = [self.lbl_int_value,
             self.lbl_int_unit,
             self.txt_int_value,
             self.txt_int_unit,
             self.lbl_float_value,
             self.lbl_float_unit,
             self.txt_float_value,
             self.txt_float_unit,
             self.lbl_str_value,
             self.txt_str_value,
             self.lbl_bool_value,
             self.txt_bool_value
             ]
        for w in l:
            w.hide()

    def _update(self,l):
        """
        Updates gui using the list of selected widgets.
        :param l:
        :return:
        """
        self._hideall()
        for w in l:
            w.show()

    def _int_selected(self,selected:bool):
        if selected:
            self.selected = 'int'
            l = [self.lbl_int_value,
                 self.lbl_int_unit,
                 self.txt_int_value,
                 self.txt_int_unit]
            self._update(l)

    def _new_paramter_selected(self,index:int):
        """
        Is called whenever a predefined parameter is selected.
        :param index:
        :return:
        """
        p = self.properties[index]
        if p.dtype == int:
            self._int_selected(True)
            self.txt_int_value.setText(str(p.value))
            self.txt_int_unit.setText(str(p.unit))
        elif p.dtype == float:
            self._float_selected(True)
            self.txt_float_value.setText(str(p.value))
            self.txt_float_unit.setText(str(p.unit))
        elif p.dtype == bool:
            self._bool_selected(True)
            self.txt_bool_value.setChecked(p.value)
        elif p.dtype == str:
            self._str_selected(True)
            self.txt_str_value.setText(p.value)

    def _float_selected(self,selected:bool):
        if selected:
            self.selected = 'float'
            l = [self.lbl_float_value,
                 self.lbl_float_unit,
                 self.txt_float_value,
                 self.txt_float_unit]
            self._update(l)

    def _str_selected(self,selected:bool):
        if selected:
            self.selected = 'string'
            l = [self.lbl_str_value,
                 self.txt_str_value]
            self._update(l)

    def _bool_selected(self,selected:bool):
        if selected:
            self.selected = 'bool'
            l = [self.lbl_bool_value,
                 self.txt_bool_value]
            self._update(l)

    def _inigui_buttons(self):
        layout_buttons = QHBoxLayout()
        self.layout0.addLayout(layout_buttons)

        self.bt_close = QPushButton('Close')
        self.bt_close.clicked.connect(self.reject)
        layout_buttons.addWidget(self.bt_close)

        self.bt_add = QPushButton('Add')
        self.bt_add.clicked.connect(self._add)
        layout_buttons.addWidget(self.bt_add)

        self.bt_add2all = QPushButton('Add to all')
        self.bt_add2all.clicked.connect(self._add)
        layout_buttons.addWidget(self.bt_add2all)

    def _valid_input(self):
        return bool(len(self.txt_name.currentText()))

    def _add2all(self):
        """
        Adds new property to all rows.
        :return:
        """
        self.add2all = True
        self._add()

    def _add(self):
        """
        Adds to property
        :return:
        """
        if self._valid_input():
            # Input accepted
            name = self.txt_name.currentText()
            if self.selected == 'int':
                value = int(self.txt_int_value.text())
                unit = self.txt_int_unit.text().strip()
            elif self.selected == 'float':
                value = float(self.txt_float_value.text())
                unit = self.txt_float_unit.text().strip()
            elif self.selected == 'string':
                value = str(self.txt_str_value.text())
                unit = ''
            elif self.selected == 'bool':
                value = bool(self.txt_bool_value.isChecked())
                unit = ''
            self.newproperty = Property(name=name,unit=unit,value=value)
            self.accept()




