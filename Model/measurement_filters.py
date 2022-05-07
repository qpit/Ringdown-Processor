from . import Measurement

class filt_base():
    def __call__(self, m:Measurement):
        return True

class filt_sampleID(filt_base):
    def __init__(self,substring:str):
        self.substring = substring
        super().__init__()

    def __call__(self, m:Measurement):
        return self.substring.lower() in m.sampleID.lower()

class filt_design_type(filt_base):
    def __init__(self,design_type:str):
        self.design_type = design_type
        super().__init__()

    def __call__(self, m:Measurement):
        return self.design_type.lower() == m.design_type.lower()

class filt_property(filt_base):
    def __init__(self,property_name,value,type):
        self.property_name = property_name
        self.value = value
        self.type = type
        super().__init__()

    def __call__(self, m:Measurement):
        try:
            mvalue = m[self.property_name]
        except ValueError:
            mvalue = getattr(m,self.property_name)

        if self.type == '<':
            return mvalue < self.value
        elif self.type == '>':
            return mvalue > self.value
        elif self.type == '==':
            return mvalue == self.value
        raise NotImplementedError()