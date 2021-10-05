from PyQt5.QtWidgets import QWidget,QVBoxLayout,QPushButton,QDialog,QHBoxLayout,QScrollArea,QSizePolicy,QMessageBox

from .MeasurementsOverview import MeasurementsOverview
from .MeasurementRow import MeasurementRow
from .Plotter import Plotter
from ...windowtemplate import WindowTemplate
from .FitDetailsOverview import FitDetailsOverview

class ProcessingDialog(WindowTemplate):
    windowtitle = "Measurements processor"
    def __init__(self,model):
        self.model = model
        super().__init__()

    def inigui(self):
        layout0 = QVBoxLayout()
        self.setLayout(layout0)

        self.measurement_overview = widget = MeasurementsOverview(parent=self,model=self.model)
        widget.is_empty.connect(self.close) # Signal when the last measurement has been deleted.
        widget.show_signal.connect(self.show_measurement)

        scrollarea = QScrollArea()
        scrollarea.setWidget(widget)
        scrollarea.setWidgetResizable(True)
        scrollarea.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        widget.setContentsMargins(0, 0, 0, 0)
        layout0.addWidget(scrollarea)

        # widget.setContentsMargins(0, 0, 0, 0)
        # layout0.addWidget(widget)

        layout1 = QHBoxLayout()
        layout0.addLayout(layout1)

        self.plotter = Plotter(self)
        layout1.addWidget(self.plotter)
        self.plotter.selection_updated.connect(self._current_plot_updated)

        layout2 = QVBoxLayout()
        layout1.addLayout(layout2)

        self.fitdetails = FitDetailsOverview(self)
        layout2.addWidget(self.fitdetails)

        bt_save = QPushButton('Save data')
        bt_save.clicked.connect(self.save2db)
        layout2.addWidget(bt_save)

        bt_cancel = QPushButton('Cancel')
        bt_cancel.clicked.connect(self.close)
        layout2.addWidget(bt_cancel)


        self.showMaximized()
        self.setContentsMargins(0,0,0,0)
        layout0.setSpacing(0)
        layout1.setSpacing(0)
        layout0.setContentsMargins(0,0,0,0)
        layout1.setContentsMargins(0, 0, 0, 0)

    def save2db(self):
        """
        Save remaining measurements to database.
        :return:
        """
        N = self.model.num_of_measurements_to_be_processed
        errors = self.model.save_processed_measurements()
        if not len(errors):
            self.accept()
        else:
            # Show error dialog
            self.hide()
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

            # Remove successfull measurements. Do in reverse order to preserve index numbers.
            for i in reversed(range(N)):
                if not i in [e.index for e in errors]:
                    self.measurement_overview.delete_row(i)

            # Show gui
            self.show()

    def _current_plot_updated(self):
        self.fitdetails.update_ui()
        self.measurement_overview.update_selected_row()

    def show_measurement(self,row:MeasurementRow):
        self.plotter.clear_measurement()
        self.plotter.load_measurement(row.measurement)
        self.plotter.plot_measurement()

        self.fitdetails.load_measurement(row.measurement)
        self.fitdetails.update_ui()