# INCOMPLETE

from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import soundfile as sf
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
import subprocess
import pyttsx3 as tts
import pyaudio as pa
# import os
# import importlib
import string
import keyboard

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

def remove_punctuation(input_string):
    # Make a translation table
    translator = str.maketrans('', '', string.punctuation)

    # Use the translate method to remove punctuation
    no_punct = input_string.translate(translator)

    return no_punct

sampling_rate = 44100

def speak(text):
    engine = tts.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    print('KYBS__NYHU: ' + text + '\n')
    engine.say(text)
    engine.runAndWait()

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

# Specify the filename for the saved audio file
output_filename = "rt_recorded_audio.wav"
# Example: Record audio for 5 seconds
duration = 2
frames = sampling_rate * duration

while True:
    MIC_ON_VALUE = 20
    def record_audio(frames = frames, sampling_rate=sampling_rate):
        # Record audio from the microphone for duration of t sec
        audio_data = sd.rec(int(frames), samplerate=sampling_rate, channels=1, dtype=np.int16)
        sd.wait()  # Wait until recording is finished

        return audio_data.flatten()
    
    def downsample_audio(input_file, output_file, target_sample_rate):
    # Example FFmpeg commands
        command = [
            'ffmpeg',
            '-y',
            '-i', input_file,
            '-ar', str(target_sample_rate),
            output_file
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Audio successfully downsampled to {target_sample_rate} Hz.")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")

    print("Loudness detection started")
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

        if keyboard.is_pressed('q'):
        # Break out of the loop if 'q' is pressed
            break

    print('Rec started:')
    # Print the duration before recording
    print(f"Recording audio with duration: {duration} seconds")
    audio_signal = record_audio(frames)
    print(audio_signal)

    # Now you can process the audio_signal as needed
    print(f"Recorded audio signal with {len(audio_signal)} samples.")    

    # Save the audio data to a WAV file
    write(output_filename, sampling_rate, audio_signal)
    print(f"Audio saved to {output_filename}")

    input_audio = output_filename
    output_audio = 'output_audio.wav'
    target_sample_rate = 16000

    downsample_audio(input_audio, output_audio, target_sample_rate)
    print(f'\nDownsampled audio as a {output_audio}')

    # read audio file
    audio_path = output_audio
    audio_data, sampling_rate = sf.read(audio_path)
    print(f'\n\nAudio data: {audio_data}, Sampling_rate: {sampling_rate}')

    if sampling_rate == 16000:
        input_feature = processor(audio_data, sampling_rate = sampling_rate, return_tensors="pt").input_features
        print('\n',input_feature)
    else:
        print('Use audio having sampling rate of 16000, the audio you gave had sampling rate {sampling_rate}')

    # generate token_ids
    predicted_id = model.generate(input_feature)

    # decode token ids to text
    transcription = processor.batch_decode(predicted_id, skip_special_tokens=True)
    print(transcription)
    string = transcription[0].lower()
    print(string)
    # transcription = remove_punctuation(string)
    # print("String without punctuation:", transcription)
    if 'hello' in string:
        speak('hello')
    # var = input('Enter q for quit, else press any key: ').lower()
    # if var == 'q':
    #     break
    speak('Loop Completed')
    frames = 44100 * duration