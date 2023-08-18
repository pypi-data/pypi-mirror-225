from recorder_utils import RecorderReader
from recorder_utils import generate_csv


input = "data/FLASH_Sedov3D_32Procs_IndpIO"
output = input.replace('/', '/files_csv/') + '.csv'
reader = RecorderReader(input)
generate_csv(reader, output)
