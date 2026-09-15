from datasets import load_dataset

dataset = load_dataset(
    "apptek-com/apptek_callcenter_dialogues",
    "diarization",
    split="test"
)

print(dataset)
print(dataset[0])