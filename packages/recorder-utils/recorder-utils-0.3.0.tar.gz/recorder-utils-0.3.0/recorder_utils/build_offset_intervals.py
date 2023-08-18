# Author: Yankun Xia

#!/usr/bin/env python
# encoding: utf-8

import itertools
import pandas as pd

from .posix_handler import handle_posix
from .mpiio_handler import handle_mpiio


def build_offset_intervals(reader):
    all_intervals_posix = handle_posix(reader)
    all_intervals_mpiio = handle_mpiio(reader)
    all_intervals_hdf5 = []

    all_intervals = list(itertools.chain(all_intervals_posix, all_intervals_mpiio, all_intervals_hdf5))

    head = ['file_id', 'rank', 'function', 'offset', 'size', 'start', 'end']
    df_intervals = pd.DataFrame(all_intervals, columns=head)

    return df_intervals
