# Author: Yankun Xia

#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import
import math
import os

from .creader_wrapper import RecorderReader
from .build_offset_intervals import build_offset_intervals


def generate_csv(reader, output_path):
    output_path = os.path.abspath(output_path)
    if output_path[-4:] != ".csv":
        output_path += ".csv"

    decimal =  int(math.log10(1 / reader.GM.time_resolution))

    df_intervals = build_offset_intervals(reader)
    df_intervals = df_intervals.sort_values(['file_id', 'rank', 'start'])
    df_intervals['start'] = df_intervals['start'].round(decimal)
    df_intervals['end'] = df_intervals['end'].round(decimal)
    df_intervals.to_csv(output_path, index=False)


def main():
    import sys
    reader = RecorderReader(sys.argv[1])
    generate_csv(reader, sys.argv[2])


if __name__ == "__main__":
    main()
