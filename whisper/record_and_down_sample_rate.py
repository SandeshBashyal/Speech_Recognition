from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
import subprocess
import os

sampling_rate = 16000

def record_audio(duration, sampling_rate=sampling_rate):
    # Record audio from the microphone
    audio_data = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished

    return audio_data.flatten()

def downsample_audio(input_file, output_file, target_sample_rate):
    command = [
        'ffmpeg',
        '-i', input_file,
        '-ar', str(target_sample_rate),
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio successfully downsampled to {target_sample_rate} Hz.")
        
        # Remove the original file after downsampling
        os.remove(input_file)
        print(f"Original file '{input_file}' removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Example: Record audio for 5 seconds
duration = 5
print('Speak')
audio_signal = record_audio(duration)

# Now you can process the audio_signal as needed
print(f"Recorded audio signal with {len(audio_signal)} samples.")

# Specify the filename for the saved audio file
output_filename = "recorded_audio.wav"

# Save the audio data to a WAV file
write(output_filename, sampling_rate, audio_signal)
print(f"Audio saved to {output_filename}")

input_audio = output_filename
output_audio = 'output_audio.wav'
target_sample_rate = 16000

downsample_audio(input_audio, output_audio, target_sample_rate)
