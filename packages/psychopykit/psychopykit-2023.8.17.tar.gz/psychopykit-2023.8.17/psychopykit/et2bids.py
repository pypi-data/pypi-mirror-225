#!/usr/bin/env python
"""
Convert PsychoPy HDF5 eyetracking results to BIDS format physiological waveform
- Requires both .hdf5 and .log files for a given series.

AUTHORS
----
Mike Tyszka

PLACE
----
Caltech Brain Imaging Center
"""


import argparse
import os

import os.path as op
from .eyetracking import EyeTracking


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--hdf5', required=True,
                        help='Input PsychoPy HDF5 eyetracker data filename')
    parser.add_argument('-o', '--outdir', required=False, default='',
                        help='Output directory')
    parser.add_argument('-b', '--bidsstub', required=False, default='recording-eyetracking_physio',
                        help="Output BIDS filename stub")
    parser.add_argument('-s', '--stimstr', required=False, default=None,
                        help="Log file string at start of stimulus")

    args = parser.parse_args()
    hdf5_fname = op.abspath(args.hdf5)

    if args.outdir:
        out_dir = args.outdir
        os.makedirs(out_dir, exist_ok=True)
    else:
        out_dir = op.dirname(hdf5_fname)

    bids_stub = args.bidsstub
    stim_str = args.stimstr

    print('\nPsychoPy HDF5 Eyetracking to BIDS Converter')
    print('-------------------------------------------\n')
    print(f'HDF5 eyetracking data : {hdf5_fname}')
    print(f'Output directory      : {out_dir}')
    print(f'BIDS filename stub    : {bids_stub}')
    print(f'Stimulus start string : {stim_str}')
    print()

    # Load HDF5 data into an ET object
    et = EyeTracking(hdf5_fname)

    # Trim data prior to stimulus start
    et.trim_to_stimulus(stim_str)

    # Export to BIDS format
    et.to_bids(out_dir, bids_stub)


# Main entry point boilerplate
if "__main__" in __name__:

    main()