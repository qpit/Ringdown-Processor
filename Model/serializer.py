import json
import pathlib
from datetime import datetime
from Model import Model

from . import constants
import numpy as np
from Model.Measurement import Measurement,Property

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
KWARGS_DUMP = {'sort_keys': True,
               'indent': 4}

"""
Module contains classes for saving model non-raw meta data and loading it again in the json format.
"""

class _Encoder_measurements(json.JSONEncoder):
    """
    Encoder used for serializing measurements meta data.
    """
    def default(self, o):
        if isinstance(o,Measurement):
            d = {'__class__':'Measurement'}
            for key,value in o.__dict__.items():
                if key in ['path','_x','_y','_i_sel','xfit','yfit']:
                    # To be skipped
                    continue
                # elif key in ['datetime']: #['_path2data','datetime']:
                #     # Convert to string.
                #     value = str(value)
                d[key] = value
            return d

        elif isinstance(o,Property):
            d = {'__class__': 'Property'}
            for key, value in o.__dict__.items():
                d[key] = value
            return d

        elif isinstance(o,datetime):
            return {'__class__': 'datetime',
                    'datetime': o.strftime(DATETIME_FORMAT)}

        else:
            return super().default(o)


def _serialize_measurements(measurements:list):
    """
    Serilizes a list of measurements.
    :param measurements:
    :return:
    """
    path = pathlib.Path(constants.path_measurements_list)
    with path.open('w') as f:
        f.write(json.dumps(measurements, cls=_Encoder_measurements, **KWARGS_DUMP))


def is_class(s:str,dct:object):
    if isinstance(dct,dict):
        if '__class__' in dct:
            if dct['__class__'] == s:
                return True
    return False


def _decoder_measurements(dct:dict):
    if is_class('Measurement',dct):
        m = Measurement()
        for key,value in dct.items():
            if key == "__Measurement__":
                continue
            m.__dict__[key] = value
        return m

    if is_class('Property',dct):
        return Property(name=dct['name'],value=dct['value'],unit=dct['unit'])

    if is_class('datetime',dct):
        return datetime.strptime(dct['datetime'],DATETIME_FORMAT)

    return dct


def _deserialize_measurements() -> list:
    """
    Deserializes a list of measurements
    :return:
    """
    path = pathlib.Path(constants.path_measurements_list)
    if path.is_file():
        with path.open('r') as f:
            data = f.read()
            list = json.loads(data, object_hook=_decoder_measurements)
    else:
        list = []
    return list


def serialize_model(model:Model):
    """
    Serializes model data.
    :return:
    """
    # Serialize measurements metadata
    _serialize_measurements(model._saved_measurements)

    # Serialize model metadata
    d = {
        'lastID': model._lastID
    }
    path = pathlib.Path(constants.path_modeldata)
    with path.open('w') as f:
        f.write(json.dumps(d, **KWARGS_DUMP))


def deserialize_model(model:Model) -> Model:
    """
    Loads model data
    :return:
    """
    # Measurements
    model._saved_measurements = _deserialize_measurements()

    # Model metadata
    path = pathlib.Path(constants.path_modeldata)
    if path.is_file():
        with path.open('r') as f:
            data = f.read()
            d = json.loads(data)
        model._lastID = d['lastID']

