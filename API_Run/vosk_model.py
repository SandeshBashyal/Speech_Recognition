from vosk import Model, KaldiRecognizer
import pyaudio as pa

model = Model(r'/media/zetahellstar/Bashyal/Coding/Speech_Recognition/API_Run/vosk-model-en-us-0.22')
# r refers to absolute path
recognizer = KaldiRecognizer(model, 48000)

mic = pa.PyAudio()
stream = mic.open(format=pa.paInt16, channels= 1, rate= 48000, input= True, frames_per_buffer= 8192)
stream.start_stream()

while True:
    data = stream.read(4096)
    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text[14:-3])


