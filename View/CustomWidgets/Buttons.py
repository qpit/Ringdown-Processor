from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QEvent,QObject,pyqtSignal
from PyQt5.QtGui import QFont

class ButtonFilter(QObject):
    def eventFilter(self, obj, event):
        if type(obj) is AddButton or issubclass(type(obj),AddButton):
            if event.type() == QEvent.Enter:
                obj.set_hover_style()
                return True
            elif event.type() == QEvent.Leave:
                obj.set_nohover_style()
                return True
            elif event.type() in [QEvent.MouseButtonPress,QEvent.MouseButtonDblClick]:
                obj.set_pressed_style()
                return True
            elif event.type() == QEvent.MouseButtonRelease:
                obj.set_released_style()
                return True
        return super().eventFilter(obj, event)


class AddButton(QLabel):
    """
    '+' button
    """
    label = '+'
    clicked = pyqtSignal()
    fontsize = 14

    def __init__(self,*args,**kwargs):
        super().__init__(self.label,*args,**kwargs)
        # Variables
        self.ispressed = False
        self.ishovered = False

        # Set large bold font.
        font = QFont()
        font.setBold(True)
        font.setPointSize(self.fontsize)
        self.setFont(font)

        # Setup event filter
        self.eventfilter = ButtonFilter()
        self.installEventFilter(self.eventfilter)

    def set_hover_style(self):
        self.ishovered = True
        if not self.ispressed:
            self.setStyleSheet("color: rgb(128, 128, 128);")

    def set_nohover_style(self):
        self.ishovered = False
        if not self.ispressed:
            self.setStyleSheet("color: rgb(0, 0, 0);")

    def set_pressed_style(self):
        self.ispressed = True
        self.setStyleSheet("color: rgb(255, 255, 255);")

    def set_released_style(self):
        self.ispressed = False
        if self.ishovered:
            self.set_hover_style()
            self.clicked.emit()
        else:
            self.set_nohover_style()

class DeleteButton(AddButton):
    """
    'X' button
    """
    label = 'X'
    fontsize = 12
