from .ListCell import ListCell
from PyQt5.QtCore import pyqtSignal,QEvent,Qt
from PyQt5.QtWidgets import QApplication
from Model import Model

class sampleID_Cell(ListCell):
    """
    Specialized cell for handling sample ID
    """
    signal_new_sampleID = pyqtSignal(str)

    def __init__(self,model:Model,*args,**kwargs):
        self.model = model
        super().__init__(*args,**kwargs)




