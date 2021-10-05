from PyQt5.QtWidgets import QDialog

class WindowTemplate(QDialog):
    windowtitle = 'Window'
    def __init__(self):
        """

        :return:
        """
        self.dlg = None
        super().__init__()
        self.setWindowTitle(self.windowtitle)
        self.inigui()

    def inigui(self):
        """

        :return:
        """
        pass

    def _dialog_opener(self,dlg,*args,**kwargs):
        self.hide()
        self.dlg = dlg(*args,**kwargs)
        self.dlg.finished.connect(self._dlg_finished)
        self.dlg.open()

    def _dlg_finished(self,returncode):
        self.dlg_finished(returncode)
        self.show()
        self.raise_()

    def dlg_finished(self,returncode):
        pass


