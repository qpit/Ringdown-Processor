import sys
from PyQt5.QtWidgets import QApplication
from View import MainWindow
from Model import Model

model = Model()
model.load()
app = QApplication(sys.argv)
mainwindow = MainWindow(model)
mainwindow.show()
app.exec()

