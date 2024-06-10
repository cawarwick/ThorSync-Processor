# ThorSync-Processor
TSv7_merge will stack the CSVS on top of each other after processing, TSv6_multi leaves them as 1 CSV per H5 file.
The TS scripts will intake the .H5 files from ThorSync and downsample them to the desired rate, then filter them by whichever datafiles you want to keep, and then saving them either to a single CSV per .h5 file or a merged csv. So far it seems like using the TS_Multi may be easier to implement since you don't have to worry about compounding time error. My processes was to take the single csvs, and then paste the time stamp into my existing timing templates rather than manually entering them.

![image](https://github.com/cawarwick/ThorSync-Processor/assets/81972652/616452b0-2339-4836-90d1-73c130223c1d)



Timestamp.py uses a directory of CSVs and a threshold value to find the start and stop of an event. It's agonist of framerate, but it can only take 1 of the AI channels at a time, e.g. if you need timestamps for the force steps on the mechanical stimulator and timestamps for foot pedal you'll have to run this twice. Make the CSV only have 2 columns, as shown in this example. It'll put a CSV called Events_originalname.csv back into the same directory you give it. The threshold itself may need to be changed for different stimuli as well as if we change the sampling rate. I've been using 10hz without issue so far. 

![image](https://github.com/cawarwick/ThorSync-Processor/assets/81972652/9fe8f732-d288-4a11-b67f-e246ce5ef528)

Result

![image](https://github.com/cawarwick/ThorSync-Processor/assets/81972652/300f84f3-44d3-4ed6-8db0-9c105197e207)




############################################

Some comments

mask = downsampled_data[:, selected_datasets.index("DI/2pFrames") + 1] >= 0.5

This filters the data to remove the time points that are recorded before and after the microscope is actually sacnning, e.g. Thorsync is running before and after the Scope is scanning for ~3 seconds. The Exact value will change depending on how much downsampling due to the 0's between frames being smeared, you DO NOT want to remove the zeroes between frames. At full frame rate, the scope is outputting a 1 or a 0 depending on whether it's scanning but downsampled data just looks like a 1 or a 0 with a slight smear at the transition. 
So far if you're downsampling to 10hz a value of 0.5 leaves an extra data point at the start and the end of each file, and so a value of 0.9 seems to be better. Other downsample rates have yet to be tested.


# Find_Peaks
This script works quite a bit differently than the other so it's an entirely different script.
It takes the same input as the Timestamp.py file (I'd suggest 1000hz sampling rate for mechanical stimulator) as a CSV with 2 rows, one is time the other is the force. You pass it an entire directory of CSVs.

![image](https://github.com/cawarwick/ThorSync-Processor/assets/81972652/fbdb1c08-49a1-44f0-9a30-d7fd93b2bdb2)

It works as follows:
1. Smoothes the force traces and creates a derivative of it. Smoothing is necessary because of both noise in the stimulator itself as well as artifactual noise introduced during the resampling.

![image](https://github.com/cawarwick/ThorSync-Processor/assets/81972652/7000b995-43a7-41c2-8cb4-2af9abdd91e4)

   
3. Finds values above or below a threshold and then locates the peak of that and notes that as an event (which I emperically set to ~2, 1-3 ish, but it may change with different frame rates or stimualtions) 
4. Saves the force applied 0.25s after the peak of the derivative (this is because the derivative finds the peak during the step rather than during the steady state)
5. It then scales the voltage to force (which needs to be emperically calibrated)
6. and then saves the times and forces of each peak derivated to a bunch of csvs

It should output 4 values per stimulation, e.g. touch down, force on, force off, and liftoff. 

# Frame out
Instead of finding the time of each event we can use the frame counter in the thorsync file to instead output the frame at which things happened. 
When used in combination, TS_FrameOut.py (which outputs the force data and the frames) and find_peaks_frames.py (which finds the responses), it should report the frames at which there are changes in force which 'should' provide a better alignment of stimuli to the calcium data.
