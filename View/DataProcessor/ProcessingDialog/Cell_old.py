from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QLineEdit,QCheckBox,QDateTimeEdit,QTextEdit,QSpacerItem
from PyQt5.QtCore import QDateTime
from Model import Measurement
from datetime import datetime
from PyQt5.QtGui import QRegExpValidator,QDoubleValidator,QIntValidator
from PyQt5.QtCore import QRegExp
from View.CustomWidgets import Spacer

SIDE_MARGIN = 2

class Cell(QWidget):
    """
    Row widget used to present and modify data of a measurement
    """
    @property
    def content(self):
        return self.get_content()

    def __init__(self,
                 name='',
                 unit=None,
                 get_content=None,
                 unit_editable = True,
                 unit_hide = False,
                 content_editable = True,
                 name_editable = True,
                 multiline = False,
                 onValueChange=None):
        """

        :param name:
        :param unit:
        :param get_content: Must be a method used for retrieving content
        :param unit_editable:
        :param unit_hide:
        :param content_editable:
        :param name_editable:
        :param multiline:
        :param onValueChange: Called when value has a valid change, with the new value being passed.
        """
        self.name = name
        self.unit = unit
        self.get_content = get_content or (lambda:'')
        self.unit_editable = unit_editable
        self.unit_hide = unit_hide
        self.content_editable = content_editable
        self.name_editable = name_editable
        self.multiline = multiline
        self.onValueChange = onValueChange or (lambda s: None)
        self.dtype = None

        super().__init__()
        self.w_content = None # Widget containing content.
        self.inigui()


    def inigui(self):
        """
        Initialize widget gui.
        :return:
        """
        layout0 = QVBoxLayout()
        layout0.setContentsMargins(0, 0, 0, 0)
        layout0.setSpacing(0)

        ''' Upper layout '''
        layoutU = QHBoxLayout()
        layoutU.setContentsMargins(0, 0, 0, 0)
        layoutU.setSpacing(0)
        layout0.addLayout(layoutU)

        # Name
        if self.name_editable:
            w = QComboBox()
            w.setEditable(True)
            w.setCurrentText(self.name)
        else:
            w = QLabel(text=self.name)

        w.setContentsMargins(SIDE_MARGIN, 0, SIDE_MARGIN, 0)
        layoutU.addWidget(w)


        ''' Lower layout '''
        self.layoutL = layoutL = QHBoxLayout()
        layoutL.setContentsMargins(0, 0, 0, 0)
        layoutL.setSpacing(0)
        layout0.addLayout(layoutL)

        # Value
        if isinstance(self.content, bool):
            self.dtype = dtype = 'bool'
            self.ini_value_bool()
        elif isinstance(self.content, float):
            self.dtype = dtype = 'float'
            self.ini_value()
        elif isinstance(self.content, int):
            self.dtype = dtype = 'int'
            self.ini_value()
        elif isinstance(self.content, datetime):
            self.dtype = dtype = 'datetime'
            self.ini_value_datetime()
        elif isinstance(self.content, (str)):
            self.dtype = dtype = 'string'
            self.ini_value_string()
        else:
            raise Exception("'{:s}' is an unsupported data type.".format(type(self.content)))

        # Unit
        if not self.unit_hide and not dtype == 'bool':
            if self.unit_editable:
                w = QComboBox()
                w.setEditable(True)
                w.setCurrentText(self.unit)
                w.setContentsMargins(0, 0, 0, 0)
            else:
                w = QLabel(text=str(self.unit))
                w.setContentsMargins(SIDE_MARGIN, 0, SIDE_MARGIN, 0)
            layoutL.addWidget(w)

        ''' Initialize '''
        self.setLayout(layout0)
        #self.show()

    def ini_noneditable_value(self):
        """
        Initilizaes a non-editable value
        :return:
        """
        self.w_content = w = QLabel(text=self.val2str())
        w.setContentsMargins(SIDE_MARGIN, 0, SIDE_MARGIN, 0)
        self.layoutL.addWidget(w)

    def ini_value(self):
        if not self.content_editable:
            self.ini_noneditable_value()
        else:
            self.w_content = w = QLineEdit()
            w.setText(self.val2str())
            w.setContentsMargins(0, 0, 0, 0)
            if self.dtype == 'int':
                input_validator = QIntValidator(w)
            elif self.dtype == 'float':
                input_validator = QDoubleValidator(w)
            else:
                raise Exception()
            w.setValidator(input_validator)
            self.layoutL.addWidget(w)
            self.w_content.textEdited.connect(self._on_value_change)

    def ini_value_string(self):
        if not self.content_editable:
            self.ini_noneditable_value()
        else:
            if self.multiline:
                self.w_content = w = QTextEdit()
                w.setText(self.val2str())
                self.w_content.textChanged.connect(self._on_value_change)
            else:
                self.w_content = w = QComboBox()
                w.setEditable(True)
                w.setCurrentText(self.val2str())
                self.w_content.currentTextChanged.connect(self._on_value_change)
            w.setContentsMargins(0, 0, 0, 0)
            self.layoutL.addWidget(w)

    def ini_value_bool(self):
        self.w_content = w = QCheckBox()
        if self.content:
            w.setChecked(True)
        if not self.content_editable:
            w.setEnabled(False)

        w.setContentsMargins(0, 0, 0, 0)
        self.w_content.stateChanged.connect(self._on_value_change_bool)
        _layout = QHBoxLayout()
        self.layoutL.addLayout(_layout)
        _layout.addItem(Spacer())
        _layout.addWidget(w)
        _layout.addItem(Spacer())

    def ini_value_datetime(self):
        if not self.content_editable:
            self.ini_noneditable_value()
            return
        self.w_content = w = QDateTimeEdit()
        qdatetime = QDateTime.fromString(str(self.content), 'yyyy-MM-dd hh:mm:ss')
        w.setDateTime(qdatetime)
        w.dateTimeChanged.connect(self._on_value_change_datetime)
        w.setContentsMargins(0, 0, 0, 0)
        self.layoutL.addWidget(w)

    def _on_value_change(self,s:str):
        self.onValueChange(self.str2val(s))

    def _on_value_change_datetime(self,w:QDateTime):
        self.onValueChange(datetime.fromisoformat(w.toString('yyyy-MM-dd hh:mm:ss')))

    def _on_value_change_bool(self,i):
        self.onValueChange(i!=0)

    def val2str(self) -> str:
        """
        Converts the current value to a suitable string.
        :return:
        """
        if self.dtype == 'float':
            return "{:.5g}".format(self.content)
        else:
            # Default behaviour.
            return str(self.content)

    def str2val(self,s:str):
        """
        Converts the string to a suitable value and dataformat.
        :param s:
        :return:
        """
        if self.dtype == 'int':
            return int(s)
        elif self.dtype == 'float':
            return float(s)
        elif self.dtype == 'string':
            return str(s)
        elif self.dtype == 'datetime':
            return datetime.strptime(s,format='yyyy-MM-dd hh:mm:ss')
        elif self.dtype == 'bool':
            return bool(s.lower() == 'true')
        else:
            raise NotImplementedError("Conversion from string to value not yet implemented for datatype '{:s}'.".format(self.dtype))


