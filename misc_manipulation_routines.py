from Model import Model,Measurement

def change_value(filters, propertyname,value):
    model = Model()
    model.load()

    measurements = [m for m in model.saved_measurements if all(f(m) for f in filters)]
    for m in measurements:
        if propertyname in m.__dict__:
            setattr(m, propertyname, value)
        else:
            m[propertyname] = value

    model.save()

def change_waferID(filters, old,new):
    model = Model()
    model.load()

    measurements = [m for m in model.saved_measurements if all(f(m) for f in filters)]
    for m in measurements:
        s = m.sampleID
        m.sampleID = s.replace(old,new)

    model.save()

class filt_base():
    def __call__(self, m:Measurement):
        return True

class filt_sampleID(filt_base):
    def __init__(self,substring:str):
        self.substring = substring
        super().__init__()

    def __call__(self, m:Measurement):
        return self.substring.lower() in m.sampleID.lower()

class filt_property(filt_base):
    def __init__(self,property_name,value,type):
        self.property_name = property_name
        self.value = value
        self.type = type
        super().__init__()

    def __call__(self, m:Measurement):
        if self.type == '<':
            return m[self.property_name] < self.value
        elif self.type == '>':
            return m[self.property_name] > self.value
        elif self.type == '==':
            return m[self.property_name] == self.value
        raise NotImplementedError()


change_waferID([filt_sampleID('DP206'),
                                    filt_property('Lp',100,'<')],
                                    'DP206','DP209')

for waferID in ['DP206','DP207','DP196']:
    change_value([filt_sampleID(waferID)],
                 'Lp',221)