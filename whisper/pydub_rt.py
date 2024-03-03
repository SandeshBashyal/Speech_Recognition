from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import soundfile as sf
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
from pydub import AudioSegment

sampling_rate = 44100
target_sample_rate = 16000

# Load Whisper model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

def record_audio(duration, sampling_rate=sampling_rate):
    # Record audio from the microphone for the specified duration
    audio_data = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished

    return audio_data.flatten()

def convert_sample_rate(input_path, output_path, target_sample_rate):
    audio = AudioSegment.from_file(input_path, format="wav")
    converted_audio = audio.set_frame_rate(target_sample_rate)
    converted_audio.export(output_path, format="wav")

# Specify the filename for the saved audio file
output_filename = "rt_recorded_audio.wav"

# Example: Record audio for 5 seconds
duration = 5

while True:
    print('Rec started:')
    audio_signal = record_audio(duration)

    # Save the audio data to a WAV file
    write(output_filename, target_sample_rate, audio_signal)
    print(f"Audio saved to {output_filename}")

    # Convert sample rate to 16000 Hz
    converted_filename = "rt_recorded_audio_converted.wav"
    convert_sample_rate(output_filename, converted_filename, target_sample_rate)

    # Read the converted audio file
    audio_data, sampling_rate = sf.read(converted_filename)
    print(f'Audio data: {audio_data}, Sampling_rate: {sampling_rate}')

    if sampling_rate == target_sample_rate:
        input_feature = processor(audio_data, sampling_rate=target_sample_rate, return_tensors="pt").input_features
    else:
        print(f'Use audio having a sampling rate of {target_sample_rate}, the audio you gave had a sampling rate of {sampling_rate}')

    # Generate token_ids
    predicted_id = model.generate(input_feature)

    # Decode token ids to text
    transcription = processor.batch_decode(predicted_id, skip_special_tokens=False)
    print(transcription)
    transcription = processor.batch_decode(predicted_id, skip_special_tokens=True)
    print(transcription)

    var = input('Enter q for quit, else press any key: ').lower()
    if var == 'q':
        break
