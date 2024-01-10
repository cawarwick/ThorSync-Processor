# ThorSync-Processor
This script will intake the .H5 files from ThorSync and downsample them to the desired rate, then filter them by whichever datafiles you want to keep, and then saving them either to a single CSV per .h5 file or a merged csv.

I haven't flesh it out particularly fully as to whether it'll be standalone or integrated with the main Calcium Imaging repo, but at least it's here.

##this value will change depending on how much downsampling due to the 0's between frames being smeared, you DO NOT want to remove the zeroes between frames
So far if you're downsampling to 10hz a value of 0.5 leaves an extra data point at the start and the end of each file, and so a value of 0.9 seems to be better. Other downsample rates have yet to be tested.
mask = downsampled_data[:, selected_datasets.index("DI/2pFrames") + 1] >= 0.5

