from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
import subprocess
# import pyttsx3 as tts
# import pyaudio as pa
# import os
# import importlib
import string
import serial
import time
import requests

url = 'http://192.168.43.243:4000/api'


mapped_phrase_to_character ={
    'led on' : 'A',
    'led off' : 'B',
    'fan on' : 'C',
    'fan off' : 'D',
    'open door' : 'E',
    'close door' : 'F',
    'lights on' : 'G',
    'lights off' : 'H',
    'turn on everything' : 'I',
    'turn off everything' : 'J',
    }

def map_character(input_phrase, mapped_phrase = mapped_phrase_to_character):
    mapped_character = mapped_phrase.get(input_phrase, 'Not mapped')
    return mapped_character

sampling_rate = 44100
duration = 4
frames = sampling_rate * duration

def calculate_loudness(audio_signal):
    # Convert int16 array to floating point for calculations
    audio_signal_float = audio_signal.astype(np.float32)

    # Calculate RMS amplitude
    rms_amplitude = np.sqrt(np.mean(audio_signal_float**2))
    return rms_amplitude
def record_sub_audio(frames = 10000, sampling_rate=sampling_rate):
    # Record audio from the microphone for duration of t sec
    audio_data = sd.rec(int(frames), samplerate=sampling_rate, channels=1, dtype=np.int16)
    sd.wait()
    amp=calculate_loudness(audio_data)
    # print(amp) prin this to find optimal value of am 
    return amp


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


# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

# Specify the filename for the saved audio file
output_filename = "rt_recorded_audio.wav"
# Example: Record audio for 5 seconds


while True:

    print('Rec started:')

    # Print the duration before recording
    # print(f"Recording audio with duration: {duration} seconds")
    while True:
        amp = record_sub_audio()
        print(amp)
        if amp > 3500:
            break
    print('activity detected')

    ser.write('A'.encode())
    audio_signal = record_audio(frames)
    ser.write('B'.encode())


    # Now you can process the audio_signal as needed
    print(f"Recorded audio signal with {len(audio_signal)} samples.")    

    # Save the audio data to a WAV file
    write(output_filename, sampling_rate, audio_signal)

    input_audio = output_filename
    output_audio = 'output_audio.wav'
    target_sample_rate = 16000

    downsample_audio(input_audio, output_audio, target_sample_rate)

    # read audio file
    audio_path = output_audio
    audio_data, sampling_rate = sf.read(audio_path)

    if sampling_rate == 16000:
        input_feature = processor(audio_data, sampling_rate = sampling_rate, return_tensors="pt").input_features
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
        # speak('hello')
        print('Hello')

    if 'open the door' in string or 'unlock the door' in string or 'unlock door' in string or 'open door' in string or 'door open' in string:
        text = 'open door'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Door': True}
        response = requests.post(url, json = data)

    elif 'close the door' in string or 'close door' in string or 'lock the door' in string or 'lock door' in string or 'closed door' in string:
        text = 'close door'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Door': False}
        response = requests.post(url, json = data)
            
    elif 'turn on the led' in string or 'turn on led' in string or 'led on' in string:
        text = 'led on'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Led':True}
        response = requests.post(url, json = data)

    elif 'turn off the led' in string or 'turn off led' in string or 'led off' in string:
        text = 'led off'
        char = map_character(text)
        ser.write(char.encode())
        data = {'Led':False}
        response = requests.post(url, json = data)

    elif 'turn on the bulb' in string or 'lights on' in string or 'light on' in string or 'turn on bulb' in string or 'bulb on' in string:
        text = 'lights on'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Light_bulb':True}
        response = requests.post(url, json = data)

    elif 'turn off the bulb' in string or 'lights off' in string or 'light off' in string or 'turn off bulb' in string or 'bulb off' in string:
        text = 'lights off'
        char = map_character(text)
        ser.write(char.encode())
        data = {'Light_bulb':False}
        response = requests.post(url, json = data)

    elif 'turn on the fan' in string or 'turn on fan' in string or 'rotate the fan' in string or 'rotate fan' in string or 'fan on' in string or 'on fan' in string:
        text = 'fan on'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Fan':True}
        response = requests.post(url, json = data)

    elif 'turn off the fan' in string or 'turn off fan' in string or 'shut the fan' in string or 'shut fan' in string or 'fan off' in string or 'off fan' in string:
        text = 'fan off'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Fan':False}
        response = requests.post(url, json = data)

    elif 'turn off everything' in string or 'everything off' in string:
        text = 'turn off everything'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Fan': False,
        'Light_bulb': False,
        'Door': False,
        'Led': False}
        response = requests.post(url, json = data)

    elif 'turn on everything' in string or 'everything on' in string:
        text = 'turn on everything'
        print(text)
        char = map_character(text)
        ser.write(char.encode())
        data = {'Fan': True,
        'Light_bulb': True,
        'Door': True,
        'Led': True}
        response = requests.post(url, json = data)

    elif 'close' in string or 'shut' in string:
        # speak('Closing')
        text = 'close'
        print(text)
        break

    else:
        print('Command not found')

    # speak('Loop Completed')
    frames = 44100 * 4
    sampling_rate = 44100

