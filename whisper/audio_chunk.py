import numpy as np
import pyaudio as pa

if __name__ == "__main__":

    MIC_ON_VALUE = 20

    print("rec started")
    mic = pa.PyAudio()
    stream = mic.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    chunk_duration = 0.1  # in seconds
    chunk_size = int(16000 * chunk_duration)

    while True:
        data = stream.read(4096)
        audio_chunk = np.frombuffer(data, dtype=np.int16)

        # Check if the length of the audio chunk is at least chunk_size samples
        if len(audio_chunk) >= chunk_size:
            # Take the first chunk_size samples for the 0.1-second chunk
            audio_chunk = audio_chunk[:chunk_size]

            # Process the audio chunk as needed
            # For example, you can print the mean value of the chunk
            chunk_mean = np.mean(audio_chunk)
            print(f"Mean value of the chunk: {chunk_mean}")

            # Add your further processing logic here

    # Stop the stream and close the PyAudio instance when the loop is interrupted
    stream.stop_stream()
    stream.close()
    mic.terminate()

