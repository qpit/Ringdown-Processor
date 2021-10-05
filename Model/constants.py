# import pathlib


# path_raw_data = pathlib.Path('raw measurements data')
# path_measurements_list = pathlib.Path('measurements_list.txt')
# path_modeldata = pathlib.Path('modeldata.txt')

path_raw_data = 'raw measurements data'
path_measurements_list = 'measurements_list.txt'
path_modeldata = 'modeldata.txt'

data_file_format = lambda measurement_ID, sampleID: "measID_{:g}_sampleID_{:s}.txt".format(measurement_ID,sampleID)

NMAX = 100