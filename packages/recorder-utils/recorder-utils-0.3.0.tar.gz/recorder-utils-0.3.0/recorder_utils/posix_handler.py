# Author: Chen Wang (original author), Yankun Xia (modifier)

#!/usr/bin/env python
# encoding: utf-8

from .exclusions import ignore_files


def handle_data_operations(record, offsetBook, func_list, endOfFile):
    func = func_list[record.func_id]
    rank, args = record.rank, record.args_to_strs()

    filename, offset, count = "", -1, -1

    if "writev" in func or "readv" in func:
        filename, count = args[0], int(args[1])
        offset = offsetBook[filename][rank]
        offsetBook[filename][rank] += count
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])
    elif "fwrite" in func or "fread" in func:
        filename, size, count = args[3], int(args[1]), int(args[2])
        offset, count = offsetBook[filename][rank], size*count
        offsetBook[filename][rank] += count
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])
    elif "pwrite" in func or "pread" in func:
        filename, count, offset = args[0], int(args[2]), int(args[3])
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])
    elif "write" in func or "read" in func:
        filename, count = args[0], int(args[2])
        offset = offsetBook[filename][rank]
        offsetBook[filename][rank] += count
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])
    elif "fprintf" in func:
        filename, count = args[0], int(args[1])
        offset = offsetBook[filename][rank]
        offsetBook[filename][rank] += count
        endOfFile[filename][rank] = max(endOfFile[filename][rank], offsetBook[filename][rank])

    return filename, offset, count


def handle_metadata_operations(record, offsetBook, func_list, total_ranks, closeBook, endOfFile):

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

    if "fopen" in func or "fdopen" in func:
        # TODO check fdopen
        filename = args[0]
        add_tracker(total_ranks, filename, endOfFile, offsetBook)
        offsetBook[filename][rank] = 0
        openMode = args[1]
        if 'a' in openMode:
            offsetBook[filename][rank] = get_latest_offset(filename, rank, closeBook, endOfFile)
    elif "open" in func:
        filename = args[0]
        add_tracker(total_ranks, filename, endOfFile, offsetBook)
        offsetBook[filename][rank] = 0
        openMode = int( args[1] )
        if openMode == 2:  # TODO need a better way to test for O_APPEND
            offsetBook[filename][rank] = get_latest_offset(filename, rank, closeBook, endOfFile)

    elif "seek" in func:
        filename, offset, whence = args[0], int(args[1]), int(args[2])

        if whence == 0:     # SEEK_SET
            offsetBook[filename][rank] = offset
        elif whence == 1:   # SEEK_CUR
            offsetBook[filename][rank] += offset
        elif whence == 2:   # SEEK_END
            offsetBook[filename][rank] = get_latest_offset(filename, rank, closeBook, endOfFile) + offset

    elif "close" in func or "sync" in func:
        filename = args[0]
        closeBook[filename] = endOfFile[filename][rank]


def ignore_funcs(func):
    ignore = ["MPI", "H5", "dir", "link"]
    for f in ignore:
        if f in func:
            return True
    return False


def handle_posix(reader):
    func_list = reader.funcs
    ranks = reader.GM.total_ranks
    intervals = []

    closeBook = {}  # Keep track the most recent close function and its file size so a later append operation knows the most recent file size
    offsetBook = {}
    endOfFile = {}  # endOfFile[filename][rank] keep tracks the end of file, only the local rank can see it. When close/fsync, the value is stored in closeBook so other rank can see it.

    # merge the list(reader.records) of list(each rank's records) into one flat list
    # then sort the whole list by tstart
    records = []
    for rank in range(ranks):
        for i in range(reader.LMs[rank].total_records):
            record = reader.records[rank][i]
            record.rank = rank

            # ignore user functions
            if record.func_id >= len(func_list): continue

            if not ignore_funcs(func_list[record.func_id]):
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

        handle_metadata_operations(record, offsetBook, func_list, ranks, closeBook, endOfFile)
        filename, offset, count = handle_data_operations(record, offsetBook, func_list, endOfFile)

        if not ignore_files(filename):
            file_id = list(filter(lambda x: filemap[x] == filename, filemap))[0]
            intervals.append( [file_id, rank, func, offset, count, record.tstart, record.tend] )

    return intervals
