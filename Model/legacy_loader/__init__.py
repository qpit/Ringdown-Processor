"""
This package contains methods for migrating data from older version of the software
"""
import json
from ..Measurement import Measurement,Property
from datetime import datetime

def load(model,path):
    ''' deserialize '''
    with open(path,'r') as f:
        data = f.read()
        l = json.loads(data)

    ''' Create measurements etc for each entry and save to model '''
    for data in l:
        m = Measurement()
        m.sampleID = data['sampleID']
        m.quality_factor = data['quality_factor']
        m.frequency = data['frequency']
        m.datetime = datetime.fromisoformat(data['datetime'])
        m.is_bad = data['is_bad']
        m.is_gas_limited = data['is_gas_limited']
        m.pressure = data['pressure']
        m.design_type = data['design_type']
        m.temperature = data['temperature']
        m.measurement_type = data['measurement_type']
        m.mode = data['mode']
        m.notes = data['notes']
        m.quality_factor_R2 = data['quality_factor_R2']
        m.quality_factor_SE = data['quality_factor_SE']
        m._x = data['x']
        m._y = data['y']

        for d in data['properties']:
            m.add_property(name=d['name'],value=d['value'],unit=d['unit'])

        model.save_measurement(m)