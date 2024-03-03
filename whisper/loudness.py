# INCOMPLETE

import pyaudio as pa


import numpy as np


def calculate_rms(audio_data):
    # Calculate the Root Mean Square (RMS)
    rms = np.sqrt(np.mean(np.square(audio_data)))
    return rms

def calculate_loudness_intervals(audio_data, sample_rate, interval_duration=0.1):
    # Calculate the number of samples in each interval
    samples_per_interval = int(sample_rate * interval_duration)

    # Calculate the RMS loudness and time intervals for each interval
    loudness_intervals = []
    time_intervals = []
    for i in range(0, len(audio_data), samples_per_interval):
        interval_data = audio_data[i:i + samples_per_interval]
        loudness = calculate_rms(interval_data)
        time_intervals.append(i / sample_rate)  # Convert sample index to time in seconds
        # loudness_intervals.append(loudness)

    return time_intervals,loudness

# Example usage:
# Replace 'your_audio_file.wav' with the path to your audio file
# file_path = '/content/drive/MyDrive/datasets/namaste.wav'

# # Load the audio file using librosa
# audio_data, sample_rate = librosa.load(file_path, sr=None)

# Calculate loudness and time intervals for each 0.1-second interval
# time_intervals, loudness_intervals = calculate_loudness_intervals(audio_data, sample_rate, interval_duration=0.1)

# # Print the results
# for i, (time_interval, loudness) in enumerate(zip(time_intervals, loudness_intervals)):
#     print(f"Interval {i + 1}: Time = {time_interval:.2f}s, Loudness = {loudness:.6f}")




if __name__ == "__main__":
    
    MIC_ON_VALUE=20


    print("rec started")
    mic = pa.PyAudio()
    stream = mic.open(format=pa.paInt16, channels= 1, rate= 16000, input= True, frames_per_buffer= 8192)
    stream.start_stream()
    chunk_duration = 0.1  # in seconds
    chunk_size = int(16000 * chunk_duration)
    while True:
        data = stream.read(4096)
        audio_chunk = np.frombuffer(data, dtype=np.int16)
        if len(audio_chunk) >= chunk_size:
        # Take the first chunk_size samples for the 0.1-second chunk
            audio_chunk = audio_chunk[:chunk_size]

        # Now you have a 0.1-second audio chunk in the form of a NumPy array

        time_intervals, loudness_intervals = calculate_loudness_intervals(audio_chunk, 16000, interval_duration=0.1)
        if loudness_intervals >MIC_ON_VALUE:
            print("speaking")
            print(loudness_intervals)
            break