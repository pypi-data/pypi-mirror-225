#!/usr/bin/env python
"""

AUTHORS
----
Mike Tyszka

PLACE
----
Caltech Brain Imaging Center
"""

import pandas as pd
import argparse


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--log', required=True, help='Input PsychoPy log filename')

    args = parser.parse_args()
    log_fname = args.log

    # Load the TSV log file into a dataframe
    df = pd.read_csv(log_fname, sep='\t', names=['Time (s)', 'Label', 'Text'])

    print(f'\nFirst five rows of {log_fname}\n')
    print(df.head(5))

    # Search for mp4 substring to identify movie used
    print('\nSearching for movie files in log\n')
    for ind, row in df.iterrows():
        if 'mp4' in row['Text']:
            print(row['Text'])


if "__main__" in __name__:

    main()