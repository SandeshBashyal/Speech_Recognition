from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import soundfile as sf
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
import subprocess
import os

sampling_rate = 44100

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

def record_audio(duration, sampling_rate=sampling_rate):
        # Record audio from the microphone for duration of t sec
        audio_data = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1, dtype=np.int16)
        sd.wait()  # Wait until recording is finished

        return audio_data.flatten()

def downsample_audio(input_file, output_file, target_sample_rate):
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

        # Remove the original file after downsampling
        # os.remove(input_file)
        # print(f"Original file '{input_file}' removed.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Specify the filename for the saved audio file
output_filename = "rt_output_recorded_audio.wav"

# Example: Record audio for 5 seconds
duration = 5

while True:
    print('Rec started:')
    audio_signal = record_audio(duration)

    # Now you can process the audio_signal as needed
    print(f"Recorded audio signal with {len(audio_signal)} samples.")    

    # Save the audio data to a WAV file
    write(output_filename, sampling_rate, audio_signal)
    print(f"Audio saved to {output_filename}")

    input_audio = output_filename
    output_audio = 'rt_output_audio.wav'
    target_sample_rate = 16000

    downsample_audio(input_audio, output_audio, target_sample_rate)

    # read audio file
    audio_path = output_audio
    audio_data, sampling_rate = sf.read(audio_path)
    print('WhisperProcessor model is trained in 16000 sampling rate, so it must be 16000')
    print(f'Audio data: {audio_data}, Sampling_rate: {sampling_rate}')

    if sampling_rate == 16000:
        input_feature = processor(audio_data, sampling_rate=sampling_rate, return_tensors="pt").input_features
    else:
        print('Use audio having sampling rate of 16000, the audio you gave had sampling rate {sampling_rate}')
    # os.remove(audio_path)
    # generate token_ids
    predicted_id = model.generate(input_feature)

    # decode token ids to text
    transcription = processor.batch_decode(predicted_id, skip_special_tokens=True)
    print(transcription)

    var = input('Enter q for quit, else press any key: ').lower()
    if var == 'q':
        break
