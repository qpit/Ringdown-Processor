from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QLabel,QMessageBox,QPushButton,QErrorMessage,QSizePolicy
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtGui import QPalette,QColor
from Model import Measurement,Model
#from .Cell_old import Cell
from . import Cell
from View.CustomWidgets import AddButton,DeleteButton,Spacer
import math
from Model.Property import Property
#from .AddNewPropertyDialogs_old import AddNewPropertyDialogs
from .AddNewPropertyDialog import AddNewPropertyDialog

COLOR_SELECTED = (0,255,255)

class MeasurementRow(QWidget):
    """
    Row widget used to present and modify data of a measurement
    """
    delete_signal = pyqtSignal(QWidget)
    show_signal = pyqtSignal(QWidget)
    signal_newentry = pyqtSignal(str)
    signal_apply_all_rows = pyqtSignal(str,object)
    signal_newproperty_all_rows = pyqtSignal(Property)

    def __init__(self,model:Model,measurement:Measurement):
        self.measurement = measurement
        self.cells = []
        self.model = model
        self.dlg = None # Placehodler for opened dialogs.
        self._maincolor = (128, 128, 128)
        super().__init__()
        self.inigui()
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed)

    def inigui(self):
        """
        Initialize widget gui.
        :return:
        """
        ''' Layouts '''
        # Main Layout
        layout0 = QHBoxLayout()
        layout0.setContentsMargins(0, 0, 0, 0)
        layout0.setSpacing(0)

        # Left part of row
        layout_left = QVBoxLayout()
        layout_left.setContentsMargins(0, 0, 0, 0)
        layout_left.setSpacing(0)
        layout0.addLayout(layout_left)

        # Upper layout
        layoutU = QHBoxLayout()
        layoutU.setContentsMargins(0, 0, 0, 0)
        layoutU.setSpacing(0)
        layout_left.addLayout(layoutU)

        # Outer Lower layout
        self.layoutL0 = layoutL0 = QHBoxLayout()
        layoutL0.setContentsMargins(0, 0, 0, 0)
        layoutL0.setSpacing(0)
        layout_left.addLayout(layoutL0)

        # Inner Lower layout
        self.layoutL = layoutL = QHBoxLayout()
        layoutL.setContentsMargins(0, 0, 0, 0)
        layoutL.setSpacing(0)
        layoutL0.addLayout(layoutL)

        ''' Special cells '''
        # Path
        cell = Cell.StringCell(name="Path",
                    retrieve_value_fcn=lambda:self.measurement.path,
                    content_editable=False)
        self.cells.append(cell)
        layoutU.addWidget(cell)

        # Sample ID
        cell = Cell.ListCell(name="Sample ID",
                             retrieve_value_fcn=lambda:self.measurement.sampleID,
                             onValueChange=lambda v:setattr(self.measurement,'sampleID',v),
                             get_items_fcn=lambda:self.model.sampleIDs)
        cell.signal_newentry.connect(self._new_sampleID)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        self.cells.append(cell)
        layoutU.addWidget(cell)


        # Design type
        self.cell_design_type = cell = Cell.ListCell(name="Design type",
                    retrieve_value_fcn=lambda:self.measurement.design_type,
                    onValueChange=lambda v:setattr(self.measurement,'design_type',v),
                             get_items_fcn=lambda:self.model.design_types)
        self.cells.append(cell)
        cell.signal_newentry.connect(self._list_cell_new_entry)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # Mode
        cell = Cell.ListCell(name="Mode",
                             retrieve_value_fcn=lambda:self.measurement.mode,
                             onValueChange=lambda v:setattr(self.measurement,'mode',v),
                             get_items_fcn=lambda:self.model.modes)
        self.cells.append(cell)
        cell.signal_newentry.connect(self._list_cell_new_entry)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # Frequency type
        value_editable = False
        if self.measurement.frequency == math.nan:
            value_editable = True
        cell = Cell.FloatCell(name="Frequency",
                    retrieve_value_fcn=lambda:self.measurement.frequency,
                    content_editable=value_editable,
                    unit='Hz')
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        self.cells.append(cell)
        layoutU.addWidget(cell)

        # Quality factor
        cell = Cell.FloatCell(name="Quality factor",
                    retrieve_value_fcn=lambda:self.measurement.quality_factor,
                    content_editable=False)
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # Temperature
        cell = Cell.FloatCell(name="Temperature",
                    retrieve_value_fcn=lambda:self.measurement.temperature,
                    unit='K',
                    onValueChange=lambda v:setattr(self.measurement,'temperature',v))
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # Pressure
        cell = Cell.FloatCell(name="Pressure",
                    retrieve_value_fcn=lambda:self.measurement.pressure,
                    unit='mBar',
                    onValueChange=lambda v:setattr(self.measurement,'pressure',v))
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # Datetime
        cell = Cell.DateTimeCell(name="Datetime",
                    retrieve_value_fcn=lambda:self.measurement.datetime,
                    onValueChange=lambda v:setattr(self.measurement,'datetime',v))
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # is bad
        cell = Cell.BoolCell(name="Bad",
                    retrieve_value_fcn=lambda:self.measurement.is_bad,
                    onValueChange=lambda v:setattr(self.measurement,'is_bad',v))
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # is gas limited
        cell = Cell.BoolCell(name="Gas limited",
                    retrieve_value_fcn=lambda:self.measurement.is_gas_limited,
                    onValueChange=lambda v:setattr(self.measurement,'is_gas_limited',v))
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layoutU.addWidget(cell)

        # Notes
        cell = Cell.TextCell(name="Notes",
                    retrieve_value_fcn=lambda:self.measurement.notes,
                    onValueChange=lambda v:setattr(self.measurement,'notes',v))
        self.cells.append(cell)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        layout0.addWidget(cell)

        ''' Extra properties '''
        # Add already existing properties
        for p in self.measurement.properties:
            self.add_property(p)

        # Add possibility of defining new properties
        w = AddButton()
        w.clicked.connect(self.define_new_property)
        self.layoutL0.addWidget(w)

        # Add spacer
        self.layoutL0.addItem(Spacer('v'))

        # Right part of row
        self.layout_right = layout_right = QVBoxLayout()
        layout_right.setContentsMargins(0, 0, 0, 0)
        layout_right.setSpacing(0)
        layout0.addLayout(layout_right)

        # Add delete button
        w = DeleteButton()
        w.setContentsMargins(5,2,5,2)
        w.clicked.connect(lambda: self.delete_signal.emit(self))
        self.layout_right.addWidget(w)

        # Add show button
        w = QPushButton('Show')
        w.clicked.connect(self.pressed_show)
        w.setMaximumWidth(100)
        self.layout_right.addWidget(w)

        # Add bottom spacers
        layout_left.addItem(Spacer('v'))
        layout_right.addItem(Spacer('v'))

        #
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout0)

    def set_color(self,r:int,g:int,b:int,temporary=False):
        """
        Sets color of row.
        :param r:
        :param g:
        :param b:
        :return:
        """
        if not temporary:
            self._maincolor = (r,g,b)
        color = QColor(r,g,b)
        self.setAutoFillBackground(True)
        p = QPalette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)

    def set_selected_color(self):
        """
        Changes widget color to selected color.
        :return:
        """
        self.set_color(*COLOR_SELECTED,temporary=True)

    def remove_selected_color(self):
        """
        Removes the selected color of widget.
        :return:
        """
        self.set_color(*self._maincolor,temporary=True)

    def pressed_show(self):
        """
        Called when show button is pressed. used for inspecting the row's measurement data.
        :return:
        """
        self.show_signal.emit(self)

    def add_property(self, property:Property,add2measurement=False):
        """
        Adds new property to gui. If add2measurement is True it also adds to the measurement object.
        :param property:
        :param add2measurement:
        :return:
        """
        if add2measurement:
            if self.measurement.property_exist(property.name):
                # Abort. Already exists.
                return
            else:
                self.measurement.add_property(property)

        kwargs = {'name':property.name,
                  'retrieve_value_fcn': lambda p=property:property.value,
                  #'onValueChange':lambda v,p=property: self._modify_property(p.name,v),
                  'onValueChange':lambda value:self.measurement.set_property_value(property.name,value),
                  'deletable': True}
        if property.dtype is int:
            cell = Cell.IntCell(unit=property.unit,**kwargs)
        elif property.dtype is float:
            cell = Cell.FloatCell(unit=property.unit,**kwargs)
        elif property.dtype is str:
            kwargs['get_items_fcn'] = lambda p=property: self.model.get_list_of_property_values(p.name)
            cell = Cell.ListCell(**kwargs)
            cell.signal_newentry.connect(self._list_cell_new_entry)
        elif property.dtype is bool:
            cell = Cell.BoolCell(**kwargs)
        else:
            raise Exception("'{:s}' is an unexpected type".format(str(type(property.dtype))))
        cell.signal_delete.connect(self._cell_deleted)
        cell.signal_apply_all_rows.connect(self._request_apply_all_rows)
        self.cells.append(cell)
        self.layoutL.addWidget(cell)
        return cell

    def _modify_property(self,property,value):
        self.measurement[property] = value

    def define_new_property(self):
        """
        Adds new property to measurement via a new dialog.
        :return:
        """
        self.dlg = dlg = AddNewPropertyDialog(self.model)
        dlg.finished.connect(self.define_new_property_accepted)
        self.window().hide()
        dlg.open()

        # self.window().hide()
        # o = AddNewPropertyDialogs()
        # o.start()
        # self.window().show()
        #
        # if o.success:
        #     p = self.measurement.add_property(name=o.name,value=o.value,dtype=o.dtype,unit=o.unit)
        #     self.add_property_gui(p)

    def define_new_property_accepted(self,returncode):
        if returncode:
            # Successfully defined a new property
            try:
                self.measurement.add_property(self.dlg.newproperty)
            except ValueError as e:
                err_dlg = QMessageBox()
                err_dlg.setText('ValueError')
                err_dlg.setInformativeText(str(e))
                err_dlg.setIcon(QMessageBox.Critical)
                err_dlg.setWindowTitle('Error')
                err_dlg.exec()
            else:
                self.add_property(self.dlg.newproperty)
                self.signal_newproperty_all_rows.emit(self.dlg.newproperty)
        self.window().show()

    def update_content(self):
        """
        Updates relevant content of row.
        :return:
        """
        for cell in self.cells:
            cell.update_value()

    def _cell_deleted(self,cell:Cell.Cell):
        self.cells.remove(cell)
        self.measurement.delete_property(cell.name)

    def _list_cell_new_entry(self, o:Cell.Cell):
        """
        Called whenever a new entry in any of the list cells have been made.
        :param o:
        :return:
        """
        self.signal_newentry.emit(o.name)

    def _request_apply_all_rows(self,cell:Cell.Cell):
        self.signal_apply_all_rows.emit(cell.name,cell.get_value())

    def update_listcell_autocompleter(self, name:str):
        """
        Updates list cell's autocompleter with the given name
        :param name:
        :return:
        """
        for cell in self.cells:
            if cell.name == name:
                cell.update_completer()
                return

    def set_cell_value(self,name,value):
        """
        Set value of cell.
        :param name:
        :param value:
        :return:
        """
        for cell in self.cells:
            if cell.name == name:
                cell.set_value(value)

    def _new_sampleID(self,cell:Cell):
        """
        Is called when the sampleID contianing cell is updated.
        :param cell:
        :return:
        """
        # Notify change in cell.
        self._list_cell_new_entry(cell)

        # Update row with new design type and properties if the sampleID can be identified
        if self.model.fillout_measurement(self.measurement):
            self.cell_design_type.set_value(self.measurement.design_type)

            # Remove old property guis
            for cell in self.cells:
                if cell.deletable:
                    cell.deleteLater()
                    self.cells.remove(cell)

            # Add the new properties in gui
            for p in self.measurement.properties:
                self.add_property(p)

