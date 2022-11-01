from PyQt5.QtWidgets import QFileDialog,QMessageBox
from PyQt5.QtCore import QObject,pyqtSignal
from Model import Model
from .ProcessingDialog import ProcessingDialog
import config
import pathlib
from .ProcessingDialog.NoButtonDialog import NoButtonDialog

class processor(QObject):
    """

    :return:
    """
    finished = pyqtSignal(int)

    def __init__(self,model:Model):
        self.model = model
        self.dlg = None
        super().__init__()

    def open(self):
        model = self.model

        # Select files for processing

        self.dlg = dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFiles)
        directory = config.load_parameter("open_measurement_directory")
        if not directory is None:
            dialog.setDirectory(directory)
        if not dialog.exec():
            # No files selected. Abort.
            self.cancel()
            return
        filenames = dialog.selectedFiles()

        # Save folder path for later use
        directory = pathlib.Path(filenames[0]).parent
        config.save_parameter("open_measurement_directory",directory)

        # Load and preprocess files.
        infowindow = NoButtonDialog("Processing files...")
        infowindow.show()

        for file in filenames:
            model.load_measurement_file(file)
        errors = model.process_loaded_files(msg_method=lambda s: infowindow.settext(s))

        infowindow.destroy()

        # Display errors if any
        if errors:
            s = "Encountered the following errors:\n"
            for e in errors:
                s += '- '
                s += str(e)
                s += '\n'
            dlg = QMessageBox()
            dlg.setIcon(QMessageBox.Critical)
            dlg.setWindowTitle("Errors")
            dlg.setText(s)
            dlg.exec()

        # Check if any measurements left.
        if model.num_of_measurements_to_be_processed == 0:
            # No valid measurements left for processing. Abort.
            dlg = QMessageBox()
            dlg.setIcon(QMessageBox.Warning)
            dlg.setText("No valid measurement files remaining.")
            dlg.setWindowTitle("Warning")
            dlg.exec()
            model.clear_measurements_to_be_processed()
            self.finish()
            return

        # Open dialog for manual processing
        self.dlg = dlg = ProcessingDialog(model)
        self.dlg.finished.connect(self._finished)
        dlg.open()

    def finish(self):
        self.finished.emit(1)

    def cancel(self):
        self.finished.emit(0)

    def _finished(self):
        # Clear loaded measurments
        self.model.clear_measurements_to_be_processed()
        self.finish()