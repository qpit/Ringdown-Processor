"""
Dialog for exporting data as csv files
"""
from ..windowtemplate import WindowTemplate
from Model import Model
from PyQt5.QtWidgets import QFormLayout,QVBoxLayout,QHBoxLayout,QLabel,QLineEdit,QCheckBox,QPushButton,QFileDialog
from ..CustomWidgets import Autocomplete
import config
import pathlib

ENTRY_ALL = '(all)'

class DlgExporter(WindowTemplate):
    windowtitle = 'Export Dialog'
    def __init__(self,model:Model):
        self.model = model
        self.valid_design_types = [ENTRY_ALL] + self.model.design_types
        super().__init__()

    def inigui(self):
        # Setup layouts
        layout0 = QVBoxLayout(self)
        self.setLayout(layout0)

        layout_form = QFormLayout(self)
        layout0.addLayout(layout_form)

        layout_buttons = QHBoxLayout(self)
        layout0.addLayout(layout_buttons)

        # Add form content
        self.cb_design = Autocomplete(self.valid_design_types,self)
        layout_form.addRow(QLabel('Design Type:'),self.cb_design)

        self.le_substring = QLineEdit()
        layout_form.addRow(QLabel('Sample ID substring:'), self.le_substring)

        self.chk_bad = QCheckBox()
        layout_form.addRow(QLabel('Include bad samples:'), self.chk_bad)

        self.chk_gas = QCheckBox()
        layout_form.addRow(QLabel('Include gas limited samples:'), self.chk_gas)

        # Add buttons
        self.bt_cancel = b = QPushButton('Cancel')
        layout_buttons.addWidget(b)
        b.clicked.connect(lambda: self.close())

        self.bt_export = b = QPushButton('Export')
        layout_buttons.addWidget(b)
        b.clicked.connect(lambda: self.export())

    def export(self):
        """
        Starts the export sequence based on user input.
        :return:
        """
        self.setEnabled(False)

        ''' Select export path '''
        self.dlg = dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)

        directory = config.load_parameter("open_export_directory")
        if not directory is None:
            dialog.setDirectory(directory)
        dialog.setDefaultSuffix('xlsx')
        dialog.setNameFilter('*.xlsx *.xls')

        filename = ''
        if not self.cb_design.currentText().lower().strip() == ENTRY_ALL.lower().strip():
            filename = self.cb_design.currentText().strip() + " "
        filename += 'export.xlsx'
        dialog.selectFile(filename)

        if not dialog.exec():
            # No files selected. Abort.
            self.close()
            return

        filename = dialog.selectedFiles()[0]

        directory = pathlib.Path(filename).parent
        config.save_parameter("open_export_directory", directory)

        ''' Generate export file '''
        kwargs = {}
        selected_design_type = self.cb_design.currentText().strip()
        if not (selected_design_type == ENTRY_ALL.lower()) and (selected_design_type in self.valid_design_types):
            kwargs['design_type'] = selected_design_type

        substring = self.le_substring.text().strip()
        if substring:
            kwargs['sampleID_substring'] = substring

        if self.chk_bad.isChecked():
            kwargs['include_bad'] = True

        if self.chk_gas.isChecked():
            kwargs['include_gas_limited'] = True

        self.model.export_csv(filename,**kwargs)

        ''' Finish '''
        self.done(1)

