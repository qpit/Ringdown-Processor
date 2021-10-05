from PyQt5.QtWidgets import QWidget,QVBoxLayout,QSpacerItem,QSizePolicy
from PyQt5.QtCore import pyqtSignal,Qt

from .MeasurementRow import MeasurementRow
from View.CustomWidgets import Spacer
from Model import Property

ROW_COLOR_1 = (192,)*3
ROW_COLOR_2 = (224,)*3

class MeasurementsOverview(QWidget):
    """
    Class presenting a list of measurements to be processed.
    """
    is_empty = pyqtSignal()
    show_signal = pyqtSignal(QWidget)

    def __init__(self,model,*args,**kwargs):
        self.model = model
        self.selected_row = None
        self.rows = []
        super().__init__(*args,**kwargs)
        self.inigui()



    def inigui(self):
        """
        Initialize gui of widget
        :return:
        """
        layout = QVBoxLayout()
        layout.setSpacing(0)

        # Initialize rows of measurements
        for measurement in self.model.measurements_to_be_processed:
            row = MeasurementRow(self.model,measurement)
            row.delete_signal.connect(lambda row:self._delete_row(row))
            row.show_signal.connect(lambda row: self._show_measurement(row))
            row.signal_newentry.connect(self._update_list_cells_autocompleter)
            row.signal_apply_all_rows.connect(self._set_value_all_rows)
            row.signal_newproperty_all_rows.connect(self._add_new_property_all_rows)
            layout.addWidget(row)
            self.rows.append(row)

        self.set_row_colors()

        layout.addItem(Spacer('v'))

        self.setLayout(layout)


        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)

        self.show()

    def set_row_colors(self):
        for index,row in enumerate(self.rows):
            if index % 2:
                row.set_color(*ROW_COLOR_1)
            else:
                row.set_color(*ROW_COLOR_2)

    def _delete_row(self,row:MeasurementRow,ignore_measurement_in_model=False):
        if not ignore_measurement_in_model:
            self.model.remove_loaded_measurement(row.measurement)
        if self.selected_row == row:
            self.selected_row = None
        self.rows.remove(row)
        row.deleteLater()
        if not self.model.num_of_measurements_to_be_processed:
            # No more measurements loaded. Abort.
            self.is_empty.emit()
        else:
            self.set_row_colors()

    def delete_row(self,index):
        """
        Removes row by index.
        :param index:
        :return:
        """
        self._delete_row(self.rows[index],ignore_measurement_in_model=True)

    def _show_measurement(self,row:MeasurementRow):
        self.show_signal.emit(row)
        if not self.selected_row is None:
            self.selected_row.remove_selected_color()
        self.selected_row = row
        row.set_selected_color()

    def update_selected_row(self):
        """
        Updates content of selected row.
        :return:
        """
        self.selected_row.update_content()

    def _update_list_cells_autocompleter(self, name):
        """
        Update all rows' list cell autocompleter with the given name.
        :param name:
        :return:
        """
        for row in self.rows:
            try:
                row.update_listcell_autocompleter(name)
            except RuntimeError:
                # Expected error of no consequence.
                pass

    def _set_value_all_rows(self,name:str,value:object):
        """
        Sets a value across all rows.
        :param name:
        :param value:
        :return:
        """
        for row in self.rows:
            row.set_cell_value(name,value)

    def _add_new_property_all_rows(self,p:Property):
        """
        Adds the new property across all rows
        :param p:
        :return:
        """
        for row in self.rows:
            row.add_property(p,add2measurement=True)

