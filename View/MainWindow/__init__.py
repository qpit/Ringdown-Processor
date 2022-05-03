from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QDialog,QFileDialog,QSpacerItem

from View.DataProcessor import processor
from Model import Model
from ..windowtemplate import WindowTemplate
from ..Exporter import DlgExporter

import xlsxwriter

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

        b = QPushButton('Export data')
        layout.addWidget(b)
        b.clicked.connect(lambda: self._dialog_opener(DlgExporter, self.model))

        layout.addSpacing(10)

        b = QPushButton('Load legacy data')
        layout.addWidget(b)
        b.clicked.connect(self._load_legacy)

        b = QPushButton('Export TOT115')
        layout.addWidget(b)
        b.clicked.connect(self._export_TOT115)



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


    def _export_TOT115(self):
        measurements = self.model.saved_measurements
        l = [m for m in measurements if "TOT115" in m.sampleID]
        workbook = xlsxwriter.Workbook('TOT115.xlsx')
        worksheet = workbook.add_worksheet()
        row = 0
        worksheet.write(row, 0, "Sample ID")
        worksheet.write(row, 1, "Frequency [Hz]")
        worksheet.write(row, 2, "Quality factor")
        worksheet.write(row, 3, "Q*f [Hz]")
        for m in l:
            row += 1
            worksheet.write(row, 0, m.sampleID)
            worksheet.write(row, 1, m.frequency)
            worksheet.write(row, 2, m.quality_factor)
            worksheet.write(row, 3, m.Qf)

        workbook.close()
