from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QDialog,QFileDialog

from View.DataProcessor import processor
from Model import Model
from ..windowtemplate import WindowTemplate

# Wra

class MainWindow(WindowTemplate):
    windowtitle = 'Ringdown Processor V2'

    def __init__(self,model:Model):
        """

        :return:
        """
        self.model = model
        super().__init__()

    def inigui(self):
        """

        :return:
        """
        self.layout = layout = QVBoxLayout()
        self.setLayout(layout)

        b = QPushButton('Process measurements')
        layout.addWidget(b)
        b.clicked.connect(lambda: self._dialog_opener(processor,self.model))

        b = QPushButton('Load legacy data')
        layout.addWidget(b)
        b.clicked.connect(self._load_legacy)



    def _load_legacy(self):
        """
        Loads legacy data from older version.
        :return:
        """
        self.hide()
        self.dlg = dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        if dialog.exec():
            path = dialog.selectedFiles()[0]
            self.model.load_legacy_data(path)
            self.model._changed()
            self.model.save()
        self.show()
