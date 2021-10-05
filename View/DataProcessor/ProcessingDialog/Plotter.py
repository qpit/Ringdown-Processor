from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt,pyqtSignal
from Model import Measurement
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import keyboard as kb

class Plotter(QWidget):
    """
    Class presenting the ringdown for the selected measurement.
    """
    selection_updated = pyqtSignal()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0,0,0,0)

        self.layout0 = QHBoxLayout()
        self.setLayout(self.layout0)

        self.layout0.setContentsMargins(0,0,0,0)

        self._ini_figure()

        self.show()

    def _ini_figure(self):
        # Setup figure and axes for plot
        self.fig = Figure(dpi=100)
        self.ax = self.fig.add_subplot(111)  # Plot handle

        self.canvas = FigureCanvasQTAgg(self.fig)
        self.canvas.setParent(self)
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        #self.canvas.updateGeometry()

        self.layout0.addWidget(self.canvas)

        # self.toolbar = NavigationToolbar2QT(self.canvas,self)
        # self.layout1.addWidget(self.toolbar)

    def clear_measurement(self):
        """
        Removes current measurement.
        :return:
        """
        self.measurement = None
        self.clear_plot()

    def clear_plot(self):
        self.ax.clear()

    def load_measurement(self,measurement:Measurement):
        """
        Loads measurement into the widget. Does not plot it.
        :param measurement:
        :return:
        """
        self.measurement = measurement

    def plot_measurement(self):
        """
        Plots the current loaded measurement
        :return:
        """
        self.clear_plot()
        m = self.measurement

        self.ax.plot(m.x, m.y, 'r.', label='Measurement points')
        if m.nsel > 3:
            self.ax.plot(m.xsel, m.ysel, 'g.', label='Points used for fitting')
            self.ax.plot(m.xfit, m.yfit, 'k-', label='Fitted line')
        self.ax.grid('on', zorder=0)
        self.fig.tight_layout(pad=2)

        # Set Y limit
        dy = m.y.max() - m.y.min()
        ymin = m.y.min() - dy * 0.02
        ymax = m.y.max() + dy * 0.02
        self.ax.set_ylim(ymin, ymax)

        # Set X limit
        self.ax.set_xlim(m.x.min(), m.x.max())

        # Set labels
        if m.measurement_type == 'ringdown':
            self.ax.set_xlabel('Time [s]')
        elif m.measurement_type == 'spectrum':
            self.ax.set_xlabel('Frequency [Hz]')
        self.ax.set_ylabel('Amplitude [dBm]')
        if len(m.sampleID) > 0:
            self.ax.set_title('Sample: ' + m.sampleID)
        else:
            self.ax.set_title(m.path)
        # self.ax.legend(loc = 3)

        # Draw
        self.canvas.draw()

        # Initialize rectangular selector
        toggle_selector.RS = RectangleSelector(
            self.ax,
            self._line_select_callback,
            drawtype='box', useblit=False,
            button=[1, 3],  # don't use middle button
            minspanx=5, minspany=5,
            spancoords='pixels',
            interactive=True)
        plt.connect('key_press_event', toggle_selector)

    def _line_select_callback(self, eclick, erelease):
        """
        Rectangular selection callback for plot.
        :param eclick:
        :param erelease:
        :return:
        """
        m = self.measurement

        # Rectangle defining the selection
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        # Find points inside selection and add/remove them

        # Left mouse button. Add or set selection.
        i_sel = []
        for i in range(len(m.x)):
            x = m.x[i]
            y = m.y[i]
            if (x2-x)*(x-x1) >= 0 and (y2-y)*(y-y1) >= 0:
                # Point inside selection
                i_sel.append(i)

        if eclick.button == 1:
            if kb.is_pressed('shift'):
                # Shift is pressed. Add to selection.
                m.add_selection(i_sel)
            else:
                m.set_selection(i_sel)

        else:
            # Right mouse button. Remove selection.
            m.remove_selection(i_sel)

        # Redo Q calculation if points are inside selection
        if m.nsel > 3:
            m.estimate()
            self.plot_measurement()
            self.selection_updated.emit()

def toggle_selector(event):
    '''
    Used for selecting data on plot.
    :param event:
    :return:
    '''
    print(' Key pressed.')
    if event.key in ['Q', 'q'] and toggle_selector.RS.active:
        print(' RectangleSelector deactivated.')
        toggle_selector.RS.set_active(False)
    if event.key in ['A', 'a'] and not toggle_selector.RS.active:
        print(' RectangleSelector activated.')
        toggle_selector.RS.set_active(True)