from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QFormLayout,QLabel
from PyQt5 import QtWidgets
from Model import Measurement

class FitDetailsOverview(QWidget):
    """
    Class presenting the fitting details of selected measurement.
    """
    def __init__(self,*args,**kwargs):
        self.measurement = None

        super().__init__(*args,**kwargs)

        self.layout0 = QFormLayout()
        self.setLayout(self.layout0)

        self.lbl_N = QLabel()
        self.layout0.addRow('Number of points', self.lbl_N)

        self.lbl_Nsel = QLabel()
        self.layout0.addRow('Number of selected points', self.lbl_Nsel)

        self.lbl_f = QLabel()
        self.layout0.addRow('Frequency',self.lbl_f)

        self.lbl_f_SE = QLabel()
        self.layout0.addRow(' - Standard error', self.lbl_f_SE)

        self.lbl_Q = QLabel()
        self.layout0.addRow('Quality factor', self.lbl_Q)

        self.lbl_Q_SE = QLabel()
        self.layout0.addRow(' - Standard error', self.lbl_Q_SE)

        self.lbl_R2 = QLabel()
        self.layout0.addRow('R2', self.lbl_R2)

        self.lbl_Qf = QLabel()
        self.layout0.addRow('Qf', self.lbl_Qf)

        self.setMaximumWidth(250)

        self.clear() # Initilizes the label texts to default.

    def load_measurement(self,measurement:Measurement):
        """
        Loads a measurement into the widget. Also removes any previous measurement and clears the ui.
        :return:
        """
        self.clear()
        self.measurement = measurement

    def update_ui(self):
        """
        Updates ui elements
        :return:
        """
        self.clear()
        self.lbl_N.setText(str(self.measurement.n))
        self.lbl_Nsel.setText(str(self.measurement.nsel))
        self.lbl_f.setText('{:.5g} Hz'.format(self.measurement.frequency))
        self.lbl_Q.setText('{:.5g}'.format(self.measurement.quality_factor))
        self.lbl_Q_SE.setText('{:.5g}'.format(self.measurement.quality_factor_SE))
        self.lbl_R2.setText('{:.5g}'.format(self.measurement.quality_factor_R2))
        self.lbl_Qf.setText('{:.5g} Hz'.format(self.measurement.Qf))

    def clear(self):
        """
        Clears ui and removes measurement
        :return:
        """
        l = [self.lbl_N,
             self.lbl_Nsel,
             self.lbl_f,
             self.lbl_f_SE,
             self.lbl_Q,
             self.lbl_Q_SE,
             self.lbl_R2,
             self.lbl_Qf
             ]

        for w in l:
            w.setText(' - ')