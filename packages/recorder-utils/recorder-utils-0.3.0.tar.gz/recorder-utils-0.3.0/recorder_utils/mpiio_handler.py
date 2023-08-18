# Author: Yankun Xia

#!/usr/bin/env python
# encoding: utf-8

from .exclusions import ignore_files
from mpi4py import MPI


def type2size(type_name):
    if type_name == 'MPI_TYPE_UNKNOWN': return 0
    else: return eval(type_name.replace('MPI_', 'MPI.')).Get_size()


def handle_data_operations(record, offsetBook, func_list, endOfFile, idNameMap):
    func = func_list[record.func_id]
    rank, args = record.rank, record.args_to_strs()

    filename, offset, count = "", -1, -1

    if 'write_at' in func or 'read_at' in func:
        fid, offset, count = args[0], int(args[1]), int(args[3]) * type2size(args[4])
        filename = idNameMap[fid]
        offsetBook[filename][rank] = offset + count
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])
    elif 'write' in func or 'read' in func:
        fid, count = args[0], int(args[2]) * type2size(args[3])
        filename = idNameMap[fid]
        offset = offsetBook[filename][rank]
        offsetBook[filename][rank] += count
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])

    return filename, offset, count


def handle_metadata_operations(record, offsetBook, func_list, total_ranks, closeBook, endOfFile, idNameMap):

    def add_tracker(total_ranks, filename, endOfFile, offsetBook): 
        if filename not in endOfFile:
            endOfFile[filename] = [0] * total_ranks
            offsetBook[filename] = [0] * total_ranks

    def get_latest_offset(filename, rank, closeBook, endOfFile):
        if filename in closeBook:
            return max(endOfFile[filename][rank], closeBook[filename])
        else:
            return endOfFile[filename][rank]

    rank, func = record.rank, func_list[record.func_id]
    args = record.args_to_strs()

    if 'open' in func:
        filename, openMode, fid = args[1], int(args[2]), args[4]
        add_tracker(total_ranks, filename, endOfFile, offsetBook)
        offsetBook[filename][rank] = 0
        idNameMap[fid] = filename
        if openMode == MPI.MODE_APPEND:  # TODO need a better way to test for MPI_MODE_APPEND
            offsetBook[filename][rank] = get_latest_offset(filename, rank, closeBook, endOfFile)
    elif 'seek' in func: # TODO: check seek_shared
        fid, offset, whence = args[0], int(args[1]), int(args[2])
        filename = idNameMap[fid]
        if whence == MPI.SEEK_SET:
            offsetBook[filename][rank] = offset
        elif whence == MPI.SEEK_CUR:
            offsetBook[filename][rank] += offset
        elif whence == MPI.SEEK_END:
            offsetBook[filename][rank] = get_latest_offset(filename, rank, closeBook, endOfFile) + offset
    elif 'close' in func or 'sync' in func:
        fid = args[0]
        filename = idNameMap[fid]
        closeBook[filename] = endOfFile[filename][rank]


def handle_mpiio(reader):
    func_list = reader.funcs
    ranks = reader.GM.total_ranks
    intervals = []

    closeBook = {}  # Keep track the most recent close function and its file size so a later append operation knows the most recent file size
    offsetBook = {}
    endOfFile = {}  # endOfFile[filename][rank] keep tracks the end of file, only the local rank can see it. When close/fsync, the value is stored in closeBook so other rank can see it.
    idNameMap = {}

    # merge the list(reader.records) of list(each rank's records) into one flat list
    # then sort the whole list by tstart
    records = []
    for rank in range(ranks):
        for i in range(reader.LMs[rank].total_records):
            record = reader.records[rank][i]
            record.rank = rank

            if 'MPI_File' in func_list[record.func_id]:
                records.append( record )

    records = sorted(records, key=lambda x: x.tstart)

    endOfFile["stdin"] = [0] * ranks
    endOfFile["stderr"] = [0] * ranks
    endOfFile["stdout"] = [0] * ranks

    filemap = {}
    for rank in range(ranks):
        filemap.update(reader.LMs[rank].filemap)

    for record in records:

        rank = record.rank
        func = func_list[record.func_id]

        handle_metadata_operations(record, offsetBook, func_list, ranks, closeBook, endOfFile, idNameMap)
        filename, offset, count = handle_data_operations(record, offsetBook, func_list, endOfFile, idNameMap)

        if not ignore_files(filename) and filename in filemap.values():
            file_id = list(filter(lambda x: filemap[x] == filename, filemap))[0]
            intervals.append( [file_id, rank, func, offset, count, record.tstart, record.tend] )

    return intervals
