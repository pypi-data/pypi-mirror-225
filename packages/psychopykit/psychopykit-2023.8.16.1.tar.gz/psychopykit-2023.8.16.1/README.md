# psychopykit
PsychoPy output conversion utilities  

Current version : 2022.8.5  

## Installation

1. Clone the Git repo  
```
git clone https://github.com/adolphslab/psychopykit.git
```

2. Install the package into your active python environment  
```
cd psychopykit
pip install .
```

## Usage
```
$ et2bids -i Examples/Test.hdf5

-------------------------------------------
PsychoPy HDF5 Eyetracking to BIDS Converter
-------------------------------------------

Loading eyetracking data from /Users/jmt/GitHub/psychopykit/psychopykit/Examples/Test.hdf5
Eyetracking dataset within HDF5: /data_collection/events/eyetracker/MonocularEyeSampleEvent
Number of events : 513753

Loading monocular eyetracking dataset
Progress            0 / 513753
Progress       102751 / 513753
Progress       154126 / 513753
Progress       256877 / 513753
Progress       308252 / 513753
Progress       462378 / 513753
Complete

Converting to dataframe
Loading PsychoPy log file /Users/jmt/GitHub/psychopykit/psychopykit/Examples/Test.log

Median samp interval : 2.000 ms
Sampling frequency   : 500.014 Hz

Saving BIDS eyetracking data /Users/jmt/GitHub/psychopykit/psychopykit/Examples/Test_recording-eyetracking_physio.tsv
Saving PsychoPy log /Users/jmt/GitHub/psychopykit/psychopykit/Examples/Test_recording-eyetracking_physio.log
Saving JSON sidecar /Users/jmt/GitHub/psychopykit/psychopykit/Examples/Test_recording-eyetracking_physio.json

Done
```