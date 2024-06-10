import os
import numpy as np
import pandas as pd
from scipy.signal import savgol_filter

# Function to process a single CSV file
# Set the scaling factor. This is emperically calculated and isn't linear across the force range, but 1-16-24 had 30x scaling as a good approximation.
def process_file(csv_file, output_dir, threshold=2.0, window_length=51, polyorder=0, scaling_factor=30):
    data = pd.read_csv(csv_file).values
    time_series = data[:, 0]
    data_series = data[:, 1]

    # Apply Savitzky-Golay filter to smooth the data
    smoothed_data = savgol_filter(data_series, window_length, polyorder)

    # Create a derivative of the smoothed data series
    dt = np.diff(time_series)
    derivative = np.diff(smoothed_data) / dt

    # Find peaks in the derivative
    above_threshold = np.abs(derivative) > threshold
    peak_indices = []
    i = 0
    while i < len(above_threshold):
        if above_threshold[i]:
            start = i
            while i < len(above_threshold) and above_threshold[i]:
                i += 1
            end = i
            # Find the peak value within the range where derivative is above threshold
            peak_index = start + np.argmax(np.abs(derivative[start:end]))
            peak_indices.append(peak_index)
        else:
            i += 1

    # Find the value of the original data 0.25 seconds after the peak
    peak_times = time_series[peak_indices]
    values_after_peak = []

    for peak_time in peak_times:
        target_time = peak_time + 0.25
        # Find the index of the closest time greater than the target_time
        index = np.searchsorted(time_series, target_time)
        if index < len(time_series):
            value = data_series[index] * scaling_factor
            values_after_peak.append(value)
        else:
            values_after_peak.append(np.nan)  # If target time is out of bounds

    # Combine peak times and values into an array
    results = np.column_stack((peak_times, values_after_peak))

    # Save the times and corresponding values back to a CSV
    results_df = pd.DataFrame(results, columns=['Peak Time', 'Scaled Value After 0.25s'])
    results_filename = os.path.join(output_dir, f'peaks_and_values_{os.path.basename(csv_file)}')
    results_df.to_csv(results_filename, index=False)

    # Save the derivative to a CSV
    #derivative_df = pd.DataFrame({'Time': time_series[:-1], 'Derivative': derivative})
    #derivative_filename = os.path.join(output_dir, f'derivative_{os.path.basename(csv_file)}')
    #derivative_df.to_csv(derivative_filename, index=False)

    print(f"Processed {csv_file} and saved results to {results_filename}")

# Directory containing input CSV files
input_dir = 'E:/#518/Thorsync/1000hz force with 0,40 smoothing/'  # Replace with your input directory
output_dir = input_dir+'/output/'  # Replace with your output directory

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Iterate over all CSV files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        csv_file = os.path.join(input_dir, filename)
        process_file(csv_file, output_dir)

print("All files processed.")
