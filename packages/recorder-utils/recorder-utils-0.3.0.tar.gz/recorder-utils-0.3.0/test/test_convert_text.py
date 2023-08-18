from recorder_utils import RecorderReader
import math

def get_func_name(reader, record):
    func_list = reader.funcs
    if record.func_id not in range(len(func_list)): return record.args_to_strs()[1]
    else : return func_list[record.func_id]


def get_func_type(reader, record):
    func_name = get_func_name(reader, record)
    if record.func_id not in range(len(reader.funcs)) : return 'USER'

    if 'H5' in func_name: return 'HDF5'
    elif 'MPI' in func_name:
        if 'MPI_File' in func_name:
            return 'MPIIO'
        else: return 'MPI'
    else: return 'POSIX'


input = "data/FLASH_Sedov3D_32Procs_IndpIO"
output = input.replace('/', '/files_txt/') + '.txt'
reader = RecorderReader(input)

with open(output, 'w') as f:
    decimal =  math.log10(1 / reader.GM.time_resolution)
    format_string = '%%.%df %%.%df %%s %%d %%s (' %(decimal, decimal)
    for rank in range(reader.GM.total_ranks):
        LM = reader.LMs[rank]
        for i in range(LM.total_records):
            record = reader.records[rank][i]
            func_name = get_func_name(reader, record)
            func_type = get_func_type(reader, record)
            f.write(format_string %(record.tstart, record.tend, func_name, record.level, func_type))
            for arg in record.args_to_strs():
                f.write(' %s' % arg)
            f.write(' )\n')