from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import pyaudio as pa
import sounddevice as sd
import numpy as np


def record_audio(duration, sampling_rate=16000):
    # Record audio from the microphone
    audio_data = sd.rec(int(sampling_rate * duration), samplerate=sampling_rate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished

    return audio_data.flatten()

# Need to update

if __name__ == "__main__":
	# load model and processor
	processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
	model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")
	
	
	# Record audio in real-time
	duration = 5  # Adjust the duration based on your requirements
	sampling_rate = 16000

	print("Recording started...")
	audio_signal = record_audio(duration, sampling_rate)

	# Process the recorded audio with Whisper
	input_features = processor(audio_signal, sampling_rate=sampling_rate, return_tensors="pt").input_features

	# Generate token ids
	predicted_ids = model.generate(input_features)

	# Decode token ids to text
	transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
	print("Transcription:")
	print(transcription)
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
			


