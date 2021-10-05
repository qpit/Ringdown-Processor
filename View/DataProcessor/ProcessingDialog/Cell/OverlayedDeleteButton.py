from View.CustomWidgets import DeleteButton
from PyQt5.QtCore import QEvent,QObject,QPoint

class OverlayedDeleteButton(DeleteButton):
    """
    A delete button overlayer on parent widget
    """
    def __init__(self,parent,*args,**kwargs):
        # Require parent widget
        super().__init__(*args,parent=parent,**kwargs)
        self.setFixedSize(self.fontsize,self.fontsize+2)
        self.hide()

        ''' Setup events for showing and hiding itself when mouse is hovering the parent '''
        self.parent().installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj is self.parent():
            if event.type() == QEvent.Enter:
                self.show()
                return True
            elif event.type() == QEvent.Leave:
                self.hide()
                return True
        return super().eventFilter(obj, event)


    def show(self):
        """
        Overwrite the show method tp ensure proper placement of the button each time.
        :return:
        """
        super().show()
        p = QPoint(self.parent().geometry().width()-self.geometry().width()-2,-2)
        self.move(p)