import pvporcupine
import struct
import pyaudio

# Set the wake word (you can replace it with your desired wake word)
wake_word = "porcupine"

# Initialize Porcupine
handle = pvporcupine.create(keyword = wake_word)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(
    rate=pvporcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=pvporcupine.frame_length,
)

print("Listening for the wake word...")

try:
    while True:
        pcm = stream.read(pvporcupine.frame_length)
        pcm_array = struct.unpack_from("h" * pvporcupine.frame_length, pcm)
        result = handle.process(pcm_array)
        
        if result:
            print("Wake word detected! Perform your action here.")
            # Replace the following line with your desired action or function call
            print("Your action: Open the door")
except KeyboardInterrupt:
    print("Stopping...")
finally:
    # Release resources
    stream.close()
    p.terminate()
    handle.delete()
