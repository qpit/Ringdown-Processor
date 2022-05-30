"""
Class for storing measurement related data.
"""

from math import nan
from .Misc import V2dBm,P2dBm,dBm2V,dBm2P
from .MeasurementFileReader import load_measurement_file
import math
import numpy as np
from scipy.optimize import least_squares
from .Property import Property
from . import constants
import pathlib

class AutoFitError(Exception):
    def __init__(self, path):
        s = "Failed to auto-estimate quality factor for file '{:s}'.".format(path)
        super().__init__(s)

"""
Constant parametmers
"""
INI_DB_DROP = 5 # Distance between ringdown start and the first point used for guessing appropriate interval for Q estimation.
INI_MIN_T_OFFSET = 5 # [s] minimum time offset from initial point.
DB_INTERVAL = 20 # Interval used for guessing appropriate interval for Q estimation.
ATTRIBUTES_BASIC_INFORMATION = [('measurement_ID','Measurement ID'),
                                ('mode','Mode ID'), # (<attribute name>, <label>)
                                ('datetime','Date and time'),
                                ('sampleID','Sample ID'),
                                ('measurement_type','Measurement type'),
                                ('frequency','Frequency [Hz]'),
                                ('quality_factor','Quality factor'),
                                ('temperature','Temperature [K]'),
                                ('pressure','Pressure [mBar]'),
                                ('notes','Notes'),
                                ('is_bad','Bad'),
                                ('is_gas_limited','Gas limited')]

class Measurement():
    @property
    def measurement_ID(self) -> int:
        return self._measurement_ID

    @property
    def n(self):
        """
        Number of datapoints
        :return:
        """
        if not self.x is None:
            return len(self.x)
        return 0

    @property
    def x(self) -> np.ndarray:
        if not self._x is None:
            return self._x
        if not self._file2data is None:
            # Load data from file.
            self._load_saved_datafile()
            return self._x
        return None

    @x.setter
    def x(self, arr:np.ndarray):
        self._x = arr
        self._changed = True

    @property
    def y(self) -> np.ndarray:
        if not self._y is None:
            return self._y
        if not self._file2data is None:
            # Load data from file.
            self._load_saved_datafile()
            return self._y
        return None

    @y.setter
    def y(self, arr:np.ndarray):
        self._y = arr
        self._changed = True

    @property
    def i_sel(self) -> list:
        if not self._x is None:
            return self._i_sel
        if not self._file2data is None:
            # Load data from file.
            self._load_saved_datafile()
            return self._i_sel.copy()
        return []

    @i_sel.setter
    def i_sel(self, l:list):
        self._i_sel = l.copy()
        self._changed = True

    @property
    def nsel(self)->int:
        """
        Number of selected datapoints
        :return:
        """
        if not self.xsel is None:
            return len(self.xsel)
        return 0

    @property
    def Qf(self):
        """
        Returns the qf product
        :return:
        """
        return self.frequency*self.quality_factor

    @property
    def xsel(self) -> np.array:
        if len(self.i_sel):
            return self.x[self.i_sel]
        return np.array([])

    @property
    def ysel(self) -> np.array:
        if len(self.i_sel):
            return self.y[self.i_sel]
        return np.array([])

    @property
    def measurement_ID(self) -> int:
        return self._measurement_ID

    @property
    def changed(self) -> bool:
        return self._changed

    @property
    def sampleID(self)->str:
        return self._sampleID

    @sampleID.setter
    def sampleID(self, s: str):
        self._sampleID = s

    @property
    def ready_for_save(self):
        """
        Returns true if measurement is ready to be saved.
        :return:
        """
        if len(self.sampleID):
            return True
        return False

    @property
    def properties(self) -> list:
        return self._properties.copy()

    def __init__(self):
        super().__init__()
        self.quality_factor = nan
        self.frequency = nan
        self.datetime = None
        self.is_bad = False
        self.is_gas_limited = False
        self.pressure = nan
        self.design_type = ''
        self._sampleID = ''
        self.temperature = nan
        self._properties = []
        self.path = '' # Path of the original data.
        self.measurement_type = ''
        self.mode = ''
        self.notes = ''
        self._measurement_ID = None
        self._file2data = None # Path to the saved raw measurement data

        # Statistics
        self.quality_factor_R2 = nan
        self.quality_factor_SE = nan

        # Raw data points
        self._x = None # Time [s] or frequency [Hz] data from measurement.
        self._y = None

        self._changed = False

        # Selected datapoints for fit
        self._i_sel = []

        # Fitted datapoints for fit
        self.xfit = None
        self.yfit = None

    def add_property(self,*args,**kwargs):
        if len(args):
            if type(args[0]) == Property:
                p = args[0]
            else:
                p = Property(*args, **kwargs)
        else:
            p = Property(*args,**kwargs)
        if self.property_exist(p.name):
            raise ValueError("The property '{:s}' already exists.".format(p.name))
        self._properties.append(p)
        return p

    def delete_property(self,name:str):
        """
        Delete property by name
        :param name:
        :return:
        """
        for p in self._properties:
            if p.name == name:
                self._properties.remove(p)
                return
        raise ValueError("The property '{:s}' does not exist in sample '{:s}'.".format(name,self.sampleID))

    def clear_properties(self):
        """
        Deletes all properties
        :return:
        """
        self._properties.clear()

    def __getitem__(self, key: str):
        for p in self._properties:
            if p.name == key:
                return p.value
        raise ValueError("The property '{:s}' does not exist.".format(key))

    def __setitem__(self, key, value):
        for p in self._properties:
            if p.name == key:
                p.value = value
                return
        raise ValueError("The property '{:s}' does not exist.".format(key))

    def set_property_value(self,key:str,value):
        self.__setitem__(key,value)

    def loadfile(self,path:str):
        """
        Opens file containing ringdown data and extracts all relevant information.
        An attempt is made to fit the automatically.
        :param path:
        :return:
        """
        self.path = path
        data = load_measurement_file(path)

        # Save key data to self
        def save(key, attr=None, default_value=None):
            if attr == None:
                attr = key
            if key in data.keys():
                setattr(self, attr, data[key])
            elif not default_value == None:
                setattr(self, attr, default_value)

        save('frequency', default_value=math.nan)
        save('datetime')

        # Save raw data to self.
        if 'x' in data.keys():
            self.x = data['x']
            self.y = data['y']

        self.measurement_type = data['type']

    def autofit(self):
        """
        Starts the automatic fitting routine. It is not precise and should always be double checked.
        :return:
        """
        if self.measurement_type == "ringdown":
            self.autofit_ringdown()
        elif self.measurement_type == "spectrum":
            self.autofit_spectrum()
        else:
            raise Exception('Unknown measurement type.')

    def estimate(self):
        """
        Estimates quality factor and other relevant properties from selected points.
        :return:
        """
        if self.measurement_type == "ringdown":
            self.estimate_ringdown()
        elif self.measurement_type == "spectrum":
            self.estimate_spectrum()
        else:
            raise Exception('Unknown measurement type.')

    def autoselectpoints_ringdown(self):
        """
        Routine for automatically selecting points for fit for ringdown type of measurement.
        :return:
        """
        dt = self.x[2] - self.x[1]

        i0 = np.argmax(self.y)

        # Pick first point of ringdown estimation offset by a fixed number of dB
        zero_crossings = np.where(np.diff(np.signbit(self.y[i0:] - self.y[i0] + INI_DB_DROP)))[0]
        if len(zero_crossings):
            i1 = zero_crossings[0] + i0

            if self.x[i1] - self.x[i0] <= INI_MIN_T_OFFSET:
                i1 = int(round(INI_MIN_T_OFFSET / dt)) + i0
                if i1 >= self.n:
                    i1 = self.n -1

            zero_crossings = np.where(np.diff(np.signbit(self.y[i1:] + DB_INTERVAL - self.y[i1])))[0]

            if len(zero_crossings):
                i2 = zero_crossings[0] + i1
                if i2 >= len(self.x):
                    i2 = len(self.x)
            else:
                i2 = len(self.x)

            self.i_sel = list(range(i1,i2))
        else:
            raise AutoFitError(self.path)

    def estimate_ringdown(self):
        """
        Estimates quality factor and other relevant properties from selected points.
        :return:
        """
        def _fun(x):
            return 20/np.log(10) * x
        p = np.polyfit(_fun(self.xsel), self.ysel, 1)
        self.quality_factor = -self.frequency * math.pi / p[0]

        # --- Estimate fitted line
        def fun(x, p):
            return _fun(x)*p[0] + p[1]
        self.xfit = np.array([self.x[0], self.x[-1]])
        self.yfit = fun(self.xfit,p)

        # --- Statistics
        n = len(self.xsel)
        err = fun(self.xsel,p) - self.ysel
        err_var = np.var(err) / (n - 2)
        err_std = math.sqrt(err_var)
        SSE = np.sum(np.power(err, 2))
        SST = np.sum(np.power(self.ysel - np.mean(self.ysel), 2))

        Sxx = np.sum(np.power(self.xsel - np.mean(self.xsel), 2))
        p_std = math.sqrt(err_var / Sxx)
        self.quality_factor_SE = self.frequency * math.pi / math.pow(p[0], 2) * p_std
        self.quality_factor_R2 = 1 - SSE / SST

    def property_exist(self,name):
        """
        Returns true if property of the given name already exists.
        :param name:
        :return:
        """
        if name in [p.name for p in self.properties]:
            return True
        return False

    def autofit_ringdown(self):
        """
        Automatic fitting routine for ringdown type of measurements
        :return:
        """
        self.autoselectpoints_ringdown()
        if len(self.i_sel):
            self.estimate_ringdown()

    def autoselectpoints_spectrum(self):
        """
        Routine for automatically selecting points for fit for spectrum type of measurement.
        :return:
        """
        self.i_sel = list(range(self.n))

    def estimate_spectrum(self):
        """
        Estimates quality factor and other relevant properties from selected points.
        :return:
        """
        # --- Data to be fitted
        n = len(self.xsel)
        f = self.xsel
        # y = dBm2P(self.selectedPoints.y)
        y = dBm2V(self.ysel)

        # --- Initial parameters guess
        b0 = np.min(y)

        # Lorentzian peak
        y_temp = y - b0
        imax = np.argmax(y_temp)
        yc0 = y_temp[imax]
        fc0 = f[imax]

        # Lorentzian left halfwidth
        indeces = [i for i in range(0, imax - 1) if y_temp[i] - yc0 / 2 >= 0]
        if len(indeces):
            fl = f[indeces[0]]
        else:
            fl = f[0]

        # Lorentzian right halfwidth
        indeces = [i for i in range(imax + 1, len(f)) if y_temp[i] - yc0 / 2 >= 0]
        if len(indeces):
            fr = f[indeces[-1]]
        else:
            fr = f[-1]

        # Lorentzian width
        df0 = fr - fl

        # --- Fitting
        x0 = [fc0, df0, yc0, b0]


        def fun(x, t, y):
            return self.spectrumfitfun(x, t) - y

        res_lsq = least_squares(fun, x0, args=(f, y))

        # --- Extract key values
        x = res_lsq.x
        jac = res_lsq.jac
        res = res_lsq.fun
        fc = x[0]
        df = x[1]
        self.frequency = fc
        self.quality_factor = fc / df

        # Uncertainty of Q estimate
        H = np.dot(np.transpose(jac), jac)
        cov = np.linalg.inv(H) * np.sum(np.square(res)) / (len(f) - 5)
        var_f = cov[0, 0]
        var_df = cov[1, 1]
        var_Q = var_df / fc ** 2 + var_f * df ** 2 / fc ** 4
        if var_f > 0 and var_df > 0 and var_Q > 0:
            self.quality_factor_SE = math.sqrt(var_Q)

            SSE = np.sum(np.power(res, 2))
            SST = np.sum(np.power(y - np.mean(y), 2))
            self.quality_factor_R2 = 1 - SSE / SST
        else:
            self.quality_factor_SE = self.quality_factor_R2 = None

        # Fitted line
        self.xfit = self.x
        self.yfit = V2dBm(self.spectrumfitfun(x, self.x))

    @staticmethod
    def spectrumfitfun(x, t):
        """
        Lorentzian function used for fitting. Assumes units of power.
        :param t:
        :return:
        """
        # Lorentzian
        tc = x[0]  # Position
        w = x[1]  # Width
        yc = x[2]  # Height
        z = (tc - t) / (w / 2)  # Transformation
        fun1 = yc * np.reciprocal(1 + np.square(z))

        b = x[3]  # Offset
        fun2 = b

        # Residual
        return fun1 + fun2

    def autofit_spectrum(self):
        """
        Automatic fitting routine for ringdown type of measurements
        :return:
        """
        self.autoselectpoints_spectrum()
        self.estimate_spectrum()

    def set_selection(self,l:list):
        """
        Sets selection using the given list of data indices
        :param l:
        :return:
        """
        self.i_sel = l.copy()
        self.i_sel.sort()

    def add_selection(self,l:list):
        """
        Adds list of selected indices to current selection.
        :param l:
        :return:
        """
        self.i_sel.extend(l)
        self.i_sel = list(set(self.i_sel)) # Remove duplicates
        self.i_sel.sort()

    def remove_selection(self,l:list):
        """
        Remove selected indices from list.
        :param l:
        :return:
        """
        for i in l:
            if i in self.i_sel:
                self.i_sel.remove(i)

    def set_measurement_ID(self,ID:int):
        if self._measurement_ID is None:
            self._measurement_ID = ID
        else:
            raise ValueError('Measurement ID already defined.')

    def _load_saved_datafile(self):
        """
        Loads the saved data file
        :return:
        """
        if self._file2data is None:
            raise Exception('Measurement not saved to any datafile.')

        path = pathlib.Path(constants.path_raw_data,self._file2data)
        with path.open('r') as f:
            state = 'ini'
            x = []
            y = []
            i_sel = []
            for line in f:
                if state == 'ini':
                    if '% measurement data' in line:
                        state = 'pre_mdata'
                        lineskip = 1
                elif state == 'pre_mdata':
                    if lineskip > 1:
                        lineskip -= 1
                    else:
                        state = 'mdata'
                elif state == 'mdata':
                    if '% selection indexes' in line:
                        state = 'idata'
                    else:
                        strings = line.split(',')
                        x.append(float(strings[0]))
                        y.append(float(strings[1]))
                elif state == 'idata':
                    i_sel.append(int(line))

            self._x = np.array(x)
            self._y = np.array(y)
            self._i_sel = i_sel

    def save2datafile(self):
        """
        Saves the raw data into a datafile.
        :return:
        """
        if self._measurement_ID is None:
            raise Exception("Cannot save to datafile when measurement ID is undefined.")

        # Open file for writing
        self._file2data = constants.data_file_format(self.measurement_ID, self.sampleID)
        path_folder = pathlib.Path(constants.path_raw_data)
        pathlib.Path.mkdir(path_folder,exist_ok=True)
        path = pathlib.Path(path_folder, self._file2data)
        with path.open('w') as f:
            ''' Write basic information '''
            for attr,label in ATTRIBUTES_BASIC_INFORMATION:
                s = "% {:s}: ".format(label)
                if attr == 'notes':
                    s += "\n% "
                    s2 = getattr(self,attr)
                    s2 = s2.replace('\n','\n% ').strip()
                else:
                    s2 = "{:s}\n".format(str(getattr(self,attr)))
                s += s2
                f.write(s)

            ''' Write measurement data '''
            s = "\n%\n% measurement data\n% "
            if self.measurement_type.lower() == 'ringdown':
                s += "time [s], power [dBm]"
            elif self.measurement_type.lower() == 'spectrum':
                s += "frequency [Hz], power [dBm]"
            s += '\n'
            f.write(s)

            _i = 0
            for i in range(self.n):
                f.write("{:}, {:}\n".format(self._x[i],self._y[i]))
                _i += 1

            ''' Write selection data '''
            if self.nsel:
                s = "% selection indexes\n"
                f.write(s)
                for i in range(self.nsel):
                    f.write("{:}\n".format(self._i_sel[i]))

        self._changed = False

    def has_property(self,name:str):
        """
        Returns True if properpy exists
        :param name:
        :return:
        """
        return name in [p.name for p in self._properties]