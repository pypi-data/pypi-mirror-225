"""
Psychopy HDF5 eyetracking handler class

AUTHOR : Mike Tyszka
PLACE  : Caltech Brain Imaging Center

MIT LICENSE
"""

import os.path as op
import numpy as np
import h5py
import pandas as pd
import json


class EyeTracking:

    def __init__(self, hdf5_fname):

        self._hdf5_fname = hdf5_fname
        self._log_fname = hdf5_fname.replace('.hdf5', '.log')

        self.mese_df = pd.DataFrame()
        self.log_df = pd.DataFrame()

        print(f'Loading eyetracking data from {op.basename(self._hdf5_fname)}')
        self.load_hdf5()

    def load_hdf5(self):

        # Check HDF5 file exists
        if not op.isfile(self._hdf5_fname):
            raise FileNotFoundError(f'* HDF5 file {self._hdf5_fname} not found')

        # Open the HDF5 file
        with h5py.File(self._hdf5_fname, 'r') as f:
            # Current PsychoPy ET HDF5 format has two top-level keys:
            # class_table_mapping: event dataset list
            # data_collection: ET data

            # Dump class table mapping for reference
            ctm_cols = ['ClassID', 'ClassTypeID', 'ClassName', 'TablePath']
            ctm_list = [list(row) for row in f['class_table_mapping']]
            ctm_df = pd.DataFrame(ctm_list, columns=ctm_cols)

            # Find mapping to monocular eye samples
            class_name = b'MonocularEyeSampleEvent'
            table_path = ctm_df.loc[ctm_df['ClassName'] == class_name, 'TablePath'].values[0]
            print(f'Eyetracking dataset within HDF5: {table_path.decode()}')

            # Extract monocular sample event dataset
            mese = f[table_path]
            print(f'Number of events : {mese.len()}')

            # Hard code this for now
            # TODO: Pull column names from HDF5 dataset object
            col_names = [
                'ExperimentID', 'SessionID', 'DeviceID', 'EventID', 'Type',
                'DeviceTime', 'LoggedTime', 'Time',
                'ConfidenceInterval', 'Delay',
                'FilterID', 'Eye',
                'GazeX', 'GazeY', 'GazeZ',
                'EyeCamX', 'EyeCamY', 'EyeCamZ',
                'AngleX', 'AngleY',
                'RawX', 'RawY',
                'PupilMeasure1', 'PupilMeasure1Type',
                'PupilMeasure2', 'PupilMeasure2Type',
                'PPDX', 'PPDY',
                'VelocityX', 'VelocityY', 'VelocityXY',
                'Status'
            ]

            # Init monocular eye sample event list
            mese_list = []
            nr = len(mese)
            print('\nLoading monocular eyetracking dataset')
            print('--------')

            # For some reason, mese[0:-1] results in much faster looping than mese
            for rc, row in enumerate(mese[0:-1]):

                # Report progress
                progress = int(rc * 1e6 / nr)
                if progress % 1e5 == 0:
                    print(f'Progress {rc:12d} / {nr:d}')

                # Add current row to the grand list
                mese_list.append(list(row))

            # Convert list of lists to dataframe
            print('Building eyetracking dataframe')
            self.mese_df = pd.DataFrame(mese_list, columns=col_names)

            # Load the TSV log file into a dataframe
            if op.isfile(self._log_fname):
                print(f'\nLoading PsychoPy log file {op.basename(self._log_fname)}')
                self.log_df = pd.read_csv(self._log_fname, sep='\t', names=['Time (s)', 'Label', 'Text'])
            else:
                print(f'* Problem loading {self._log_fname}')

    def to_bids(self, out_dir, bids_stub):

        # Estimate median sampling frequency
        samp_freq = self.get_sampling_freq()

        # Output physio TSV and JSON filenames
        tsv_fname = op.join(out_dir, f'{bids_stub}.tsv')
        json_fname = op.join(out_dir, f'{bids_stub}.json')
        log_fname = op.join(out_dir, f'{bids_stub}.log')

        # Subset of dataframe columns to save
        # ExperimentID: skip
        # SessionID: skip
        # DeviceID: skip
        # EventID: skip
        # Type: skip
        # DeviceTime: skip
        # LoggedTime: skip
        # > Time: retain
        # > ConfidenceInterval: retain
        # > Delay: retain
        # FilterID: skip
        # Eye: skip
        # > GazeX: retain
        # > GazeY: retain
        # GazeZ: skip
        # EyeCamX, EyeCamY, EyeCamZ: skip
        # AngleX, AngleY: skip
        # RawX, RawY: skip
        # > PupilMeasure1: right eye - retain
        # PupilMeasure1Type: skip
        # PupilMeasure2: skip
        # PupilMeasure2Type: skip
        # PPDX, PPDY: Pixels per degree - skip
        # VelocityX, VelocityY, VelocityXY: can be calculated in post - skip
        # Status: zero in almost all recordings - skip
        req_cols = ['Time', 'ConfidenceInterval', 'Delay', 'GazeX', 'GazeY', 'PupilMeasure1']

        # Save BIDS physio TSV
        print(f'Saving BIDS eyetracking data {tsv_fname}')
        self.mese_df.to_csv(tsv_fname, columns=req_cols, header=False, index=False, sep='\t')

        # Save PyschoPy log as a TSV with .log extension (non-BIDS)
        print(f'Saving PsychoPy log {log_fname}')
        self.log_df.to_csv(log_fname, index=False, sep='\t')

        # Create dictionary of metadata and write to JSON sidecar
        json_dict = {
            "SamplingFrequency": samp_freq,
            "StartTime": np.min(self.mese_df['Time'].values),
            "Columns": req_cols,
            "Time": {
                "Units": "s"
            }
        }

        # Finally write JSON sidecar
        print(f'Saving JSON sidecar {json_fname}')
        self._write_json(json_fname, json_dict, overwrite=True)

    def trim_to_stimulus(self, stim_str=None):

        # Get start time of movie
        # Search text depends on original PsychoPy script variable names

        if stim_str:

            stim_start = self.log_df['Text'].str.contains(stim_str)
            t0 = self.log_df[stim_start]['Time (s)'].values[0]

            # Drop mese rows before stimulus start
            print(f'Stimulus start string \"{stim_str}" found at time {t0} s')
            print(f'Trimming eyetracking data before {t0} s')
            self.mese_df.drop(self.mese_df[self.mese_df['Time'] < t0].index, inplace=True)

            return t0

    def get_sampling_freq(self):

        dt = np.median(np.diff(self.mese_df['Time'].values))
        samp_freq = 1.0 / dt

        print(f'\nEyetracking Sampling Details')
        print(f'--------')
        print(f'Median samp interval : {dt * 1e3:0.3f} ms')
        print(f'Sampling frequency   : {samp_freq:0.3f} Hz\n')

        return samp_freq

    @staticmethod
    def _write_json(json_fname, json_dict, overwrite=False):

        if op.isfile(json_fname):
            if overwrite:
                create_file = True
            else:
                create_file = False
        else:
            create_file = True

        if create_file:
            with open(json_fname, 'w') as fd:
                json.dump(json_dict, fd, indent=4, separators=(',', ':'))
