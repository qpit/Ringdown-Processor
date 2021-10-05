class Property():
    @property
    def dtype(self):
        return type(self.value)

    def __init__(self,name,value,unit=''):
        super().__init__()
        self.name = name
        self.value = value
        self.unit = unit

    def copy(self):
        return Property(name=self.name,value=self.value,unit=self.unit)
