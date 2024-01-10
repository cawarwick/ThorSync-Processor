# ThorSync-Processor
This script will intake the .H5 files from ThorSync and downsample them to the desired rate, then filter them by whichever datafiles you want to keep, and then saving them either to a single CSV per .h5 file or a merged csv.

I haven't flesh it out particularly fully as to whether it'll be standalone or integrated with the main Calcium Imaging repo, but at least it's here.


############################################

Some comments

mask = downsampled_data[:, selected_datasets.index("DI/2pFrames") + 1] >= 0.5

This filters the data to remove the time points that are recorded before and after the microscope is actually sacnning, e.g. Thorsync is running before and after the Scope is scanning for ~3 seconds. The Exact value will change depending on how much downsampling due to the 0's between frames being smeared, you DO NOT want to remove the zeroes between frames. At full frame rate, the scope is outputting a 1 or a 0 depending on whether it's scanning but downsampled data just looks like a 1 or a 0 with a slight smear at the transition. 
So far if you're downsampling to 10hz a value of 0.5 leaves an extra data point at the start and the end of each file, and so a value of 0.9 seems to be better. Other downsample rates have yet to be tested.


