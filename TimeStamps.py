import csv
import os
import statistics

def process_csv(input_csv, output_csv):
    # Step 1: Import CSV file with a time series in the 1st column and the data in the second column
    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Step 2: Initialize Events array with headers This is assuming it's the mech stim trace
    events = [['Force', 'Start', 'Stop']]

    # Step 3: Process Time_Stamps and populate Events array
    start_time = None
    force_values = []
    M_Scaling = 30  # Set the scaling factor. This is emperically calculated and isn't linear across the force range, but 1-16-24 had 30x scaling as a good approximation.

    for row in data[1:]:
        time_point = float(row[0])
        force_value = float(row[1])

        if force_value > 0.15 and start_time is None:
            # Above the threshold and not already triggered, note the start time. The force_value is the voltage which best thresholds the step function. 0.1 was too low bc of the oscilations in the FFT transform. 
            start_time = time_point
            force_values = [force_value]
        elif force_value < 0.15 and start_time is not None:
            # Below the threshold and recording, stop recording
            stop_time = time_point
            median_force = statistics.median(force_values) * M_Scaling
            events.append([median_force, start_time, stop_time])
            start_time = None
            force_values = []

        # Accumulate force values for the current event
        if start_time is not None:
            force_values.append(force_value)

    # Step 4: Write Events array back to CSV
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(events)



# Specify the directory containing your CSV files
directory = 'Y:/DRGS project/#505 12-18-23/SDH Recording/Final FOV/Functional/ThorSync/H5 files/pedal/'

# Iterate over CSV files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        input_csv_file = os.path.join(directory, filename)
        output_csv_file = os.path.join(directory, f"Events_{filename}")
        process_csv(input_csv_file, output_csv_file)
