from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import soundfile as sf
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
import subprocess
# import os
# import importlib

sampling_rate = 44100

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

# Specify the filename for the saved audio file
output_filename = "rt_recorded_audio.wav"
# Example: Record audio for 5 seconds
duration = 2
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

    var = input('Enter q for quit, else press any key: ').lower()
    if var == 'q':
        break
    frames = 44100 * 5
    sampling_rate = 44100 
