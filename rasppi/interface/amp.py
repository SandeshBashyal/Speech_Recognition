import numpy as np
import sounddevice as sd

sampling_rate = 44100

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

while True:
    amp = record_sub_audio()
    print(amp)
    if amp > 230:
        break
    print('activity detected')
