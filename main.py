import sys
from PyQt5.QtWidgets import QApplication
from View import MainWindow
from Model import Model

if __name__ == '__main__':
    model = Model()
    model.load()
    app = QApplication(sys.argv)
    mainwindow = MainWindow(model)
    mainwindow.show()
    app.exec()

    # Export all data if changes has occured
    model.export_csv('All ringdown results.xlsx')



