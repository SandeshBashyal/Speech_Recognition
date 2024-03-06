from transformers import WhisperProcessor, WhisperForConditionalGeneration
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
import serial
import time
import requests

url = 'http://192.168.11.107:4000/api'

mapped_phrase_to_character ={
	'turn on the led' : 'A',
	'turn off the led' : 'B',
	'turn on the fan' : 'C',
	'turn off the fan' : 'D',
    'open the door' : 'E',
    'close the door' : 'F',
    'turn on the bulb' : 'G',
    'turn off the bulb': 'H',
    }



def map_character(input_phrase, mapped_phrase = mapped_phrase_to_character):
    mapped_character = mapped_phrase.get(input_phrase, 'Not mapped')
    return mapped_character

sampling_rate = 44100

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

# Specify the filename for the saved audio file
output_filename = "rt_recorded_audio.wav"
# Example: Record audio for 5 seconds
duration = 5
frames = sampling_rate * duration

while True:
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

    print('Rec started:')
    # Print the duration before recording
    # print(f"Recording audio with duration: {duration} seconds")
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
        print('Hello')

    elif 'open the door' in string or 'upon the door' in string or 'up on the door' in string or 'open door' in string or 'upon door' in string:
        text = 'open the door'
        print(text)
        char = map_character(text)
        print(char)
        data =  {'Door':True}
        ser.write(char.encode())
        # time.sleep(1)

    elif 'close the door' in string or 'close door' in string or 'lock the door' in string or 'lock door' in string:
        text = 'close the door'
        print(text)
        char = map_character(text)
        print(char)
        data =  {'Door':False}
        ser.write(char.encode())
        # time.sleep(1)
    
    elif 'turn on the led' in string or 'turn on led' in string or 'turn on bulb' in string or 'turn on the bulb' in string or 'lights on' in string or 'light on' in string:
        text = 'turn on the led'
        print(text)
        char = map_character(text)
        print(char)
        ser.write(char.encode())
        # time.sleep(1)

    elif 'turn off the led' in string or 'turn off led' in string or 'turn off the bulb' in string or 'turn off bulb' in string or 'turn on the lights' in string or 'lights off' in string or 'turn off the light' in string or 'light off' in string:
        text = 'turn off the led'
        char = map_character(text)
        ser.write(char.encode())
        # time.sleep(1)

    elif 'turn on the fan' in string or 'turn on fan' in string or 'rotate the fan' in string or 'rotate fan' in string or 'fan on' in string:
        text = 'turn on the fan'
        print(text)
        char = map_character(text)
        print(char)
        ser.write(char.encode())
        # time.sleep(1)

    elif 'turn off the fan' in string or 'turn off fan' in string or 'shut the fan' in string or 'shut fan' in string:
        text = 'turn off the fan'
        print(text)
        char = map_character(text)
        print(char)
        ser.write(char.encode())
        # time.sleep(1)

    elif 'close' in string or 'shut' in string:
        text = 'close'
        print(text)
        break

    else:
        print('Command not found')
   
    
    try:
        response = requests.post(url, json = data)
        
        if response.status_code == 200:
            print('Post Command Successful')

        else:
            print('Post Command not Successful')

    except requests.exceptions.RequestException as e:
        print(f'Error as {e}')

    
    frames = 44100 * 5
    sampling_rate = 44100
