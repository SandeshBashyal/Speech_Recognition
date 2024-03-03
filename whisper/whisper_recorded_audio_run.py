from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset
import soundfile as sf

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

# read audio file
audio_path = "/media/zetahellstar/Bashyal/Coding/Speech_Recognition/API_Run/whisper/recorded_audio.wav"
audio_data, sampling_rate = sf.read(audio_path)
print('WhisperProcessor model is trained in 16000 sampling rate, so it must be 16000')
print(f'Audio data: {audio_data}, Sampling_rate: {sampling_rate}')

if sampling_rate == 16000:
    input_feature = processor(audio_data, sampling_rate=sampling_rate, return_tensors="pt").input_features
else:
    print('Use audio having sampling rate of 16000, the audio you gave had sampling rate {sampling_rate}')

# generate token_ids
predicted_id = model.generate(input_feature)

# decode token ids to text
transcription = processor.batch_decode(predicted_id, skip_special_tokens=False)
print(transcription)
transcription = processor.batch_decode(predicted_id, skip_special_tokens=True)
print(transcription)