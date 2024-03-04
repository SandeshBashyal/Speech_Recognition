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
import serial
import time

mapped_phrase_to_character = {
	'turn on the led' : 'A',
	'turn off the led' : 'B',
	'turn on the fan' : 'C',
	'turn off the fan' : 'D',
	'open the door' : 'E',
        'close the door' : 'F',
    }

def map_character(input_phrase, mapped_phrase = mapped_phrase_to_character):
	mapped_character = mapped_phrase.get(input_phrase, 'Not mapped')
	return mapped_character

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

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
ser.reset_input_buffer()

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
		# speak('hello')

	elif 'open the door' or 'unlock the door' in string:
		text = 'open the door'
		# speak('Opening the door')
		char = map_character(text)
		print(char)
		ser.write(char.encode())
		time.sleep(1)
		# var = input('Enter q for quit, else press any key: ').lower()

	elif 'close the door' or 'close door' or 'lock the door' or 'lock door' or 'shut the door' or 'shut door' or 'shutdown the door' or 'shutdown door' or 'closes the door' or 'closes door' or 'locks the door' or 'locks door' or 'shuts the door' or 'shuts door' or 'shutdowns the door' or 'shutdowns door' in string:
		text = 'close the door'
		# speak('Closing the door')
		char = map_character(text)
		print(char)
		ser.write(char.encode())
		time.sleep(1)

	elif 'turn on the led' or 'turn on led' or 'turn on the bulb' or 'turn on bulb' or 'light the bulb' or 'light bulb' or 'light led' or 'light the led' or 'switch on the led' or 'switch on the bulb' or 'switch on led' or 'switch on bulb' in string:
		text = 'turn on the led'
		# speak('Turning on the led')
		char = map_character(text)
		print(char)
		ser.write(char.encode())
		time.sleep(1)

	elif 'turn off the led' or 'turn of the led' or 'turn off led' or 'turn of led' or 'turn off the bulb' or 'turn off bulb' or 'turn of bulb' or 'turn of the bulb' or 'switch off the bulb' or 'switch of the bulb' or 'switch off bulb' or 'switch of bulb' or 'close bulb' or 'close led' or 'light off led' or 'light off the led' or 'light of led' or 'light of the led' or 'light off bulb' or 'light off the bulb' or 'light of the bulb' or 'light of bulb' in string:
		text = 'turn off the led'
		# speak('Turning off the led')
		char = map_character(text)
		print(char)
		ser.write(char.encode())
		time.sleep(1)

	elif 'turn on the fan' or 'switch on the fan' or 'turn on fan' or 'switch on fan' or 'rotate the fan' or 'rotate fan' in string:
		text = 'turn on the fan'
		# speak('Turning on the fan')
		char = map_character(text)
		print(char)
		ser.write(char.encode())
		time.sleep(1)

	elif 'turn off the fan' or 'turn of the fan' or 'turn off fan' or 'turn of fan' or 'shut down the fan' or 'shut down fan' or 'shutdown the fan' or 'shutdown fan' or 'switch off the fan' or 'switch off fan' in string:
		text = 'turn off the fan'
		# speak('Turning off the fan')
		char = map_character(text)
		print(char)
		ser.write(char.encode())
		time.sleep(1)

	elif 'close' or 'quit' or 'shut down' or 'shutdown' or 'shut' in string:
		# speak('closing')
		break
   
	else:
		print('Command not found')

	frames = 44100 * 5
	sampling_rate = 44100
	# speak('Speak Again')
