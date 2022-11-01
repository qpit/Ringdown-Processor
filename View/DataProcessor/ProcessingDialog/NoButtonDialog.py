from View.windowtemplate import WindowTemplate
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QDialog,QHBoxLayout,QDialogButtonBox, QFormLayout,QSpinBox,QLineEdit,QLabel,QDoubleSpinBox,QCheckBox,QRadioButton,QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

class NoButtonDialog(QWidget):
    def __init__(self,windowtitle:str):
        super().__init__()
        self.setWindowTitle(windowtitle)
        self.layout0 = layout0 = QVBoxLayout()
        self.setLayout(layout0)

        self.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.txt_msg = w = QLabel("Test")
        w.setMinimumWidth(400)
        self.layout0.addWidget(self.txt_msg)

    def settext(self,s:str):
        self.txt_msg.setText(s)
        QApplication.processEvents()
        # self.show()