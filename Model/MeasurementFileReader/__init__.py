from . import Keysight,MSA_Ringdown,SSA3000X


class InvalidRingdownFileError(Exception):
    def __init__(self,path):
        s = "Cannot identify content of file '{:s}'. Unable to load file.".format(path)
        super().__init__(s)

def load_measurement_file(path:str)->dict:
    """
    Tries to open and process datafile specified by the path string.
    :param path:
    :return:
    """
    modules = [Keysight,MSA_Ringdown,SSA3000X]

    for module in modules:
        if module.valid(path):
            return module.load_data_file(path)
    raise InvalidRingdownFileError(path)
