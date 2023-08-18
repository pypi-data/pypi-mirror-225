# Prerequisite

MPI implementation such as openmpi or MPICH


# Install

Install from source
```
pip install -r requirements.txt
pip install .
```

Or Install from pip
```
pip install recorder-utils
```

# Usage

```
recorder2csv /path/to/your_trace_folder/   /path/to/output.csv/
```
A csv trace file will be generated to the output file you specified


# Test

Use the test file under test directory, the output will be in the data directory


## Example

Under Recorder-util directory
```
python3 test/test_convert_text.py
```


# API

## RecorderReader:
- GM : RecorderMetadata
- funcs : string[], utf-8
- records : *PyRecord[], range(): 0 - total_rank-1
- LMs : LocalMetadata[], range(): 0 - total_rank-1


### RecorderMetadata: 
- total_ranks : c_int
- start_ts : c_double
- time_resolution : c_double
- ts_buffer_elements : c_int
- ts_compression_algo : c_int


### LocalMetadata:
- total_records : c_size_t
- num_files : int
- filemap : set()
- function_count : int[], share the index with Recorder.funcs


### PyRecord:
- tstart : c_double
- tend : c_double
- level : c_ubyte
- func_id : c_ubyte
- tid : c_int
- arg_count : c_ubyte
    
args_to_strs : string[], utf-8

## Intervals

Current intervals are taken from POSIX and MPIIO layers. They are stored in the dataframe that return by the function ```build_offset_intervals```. The intervals contain I/O records and corresponding ```filename, rank, function, offset, size, start time, and end time```.
