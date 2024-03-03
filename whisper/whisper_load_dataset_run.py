from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-base.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base.en")

# load dummy dataset 
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation", trust_remote_code = True)
print(ds,'\n')
sample = ds[0]["audio"]
print(sample,'\n')
input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features 

# generate token ids
predicted_ids = model.generate(input_features)

# decode token ids to text
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
print(transcription)
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)
