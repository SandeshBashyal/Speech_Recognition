# Need to update

from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import sounddevice as sd
import numpy as np
import queue
import threading
print('Libraries Imported\n\n')

# Load Whisper model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")
print('Models loaded\n\n')

# Audio parameters
sampling_rate = 16000  # Adjust according to your audio input
chunk_size = 8000  # Adjust based on your requirements

# Buffer to store audio chunks
audio_buffer = queue.Queue()

# Function to process audio chunks
def process_audio_chunk(indata, frames, time, status):
    if status:
        print(status, flush=True)

    # Add the audio chunk to the buffer
    audio_buffer.put(np.squeeze(indata))

# Function to continuously process audio from the buffer
def process_audio():
    while True:
        try:
            # Get an audio chunk from the buffer
            audio_chunk = audio_buffer.get()

            # Preprocess the audio chunk
            input_features = processor(audio_chunk, sampling_rate=sampling_rate, return_tensors="pt").input_features

            # Generate token ids
            predicted_ids = model.generate(input_features)

            # Decode token ids to text
            transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
            print(transcription)

        except queue.Empty:
            # The buffer is empty; wait for new data
            pass

print('Functions written\n\n\n\n')

# Start streaming audio input
with sd.InputStream(callback=process_audio_chunk, channels=1, blocksize=chunk_size, samplerate=sampling_rate):
    print("#" * 80)
    print("Press Ctrl+C to stop the streaming")
    print("#" * 80)

    # Start the audio processing thread
    audio_thread = threading.Thread(target=process_audio)
    audio_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nStreaming stopped.")

    # Wait for the audio processing thread to finish
    audio_thread.join()

# The rest of existing code for processing a single audio sample
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = ds[1]["audio"]
input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features 

# Generate token ids
predicted_ids = model.generate(input_features)
# Decode token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
print(transcription)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)

