from datasets import load_dataset

ds = load_dataset("Mireu-Lab/NSL-KDD")

print(ds["train"][11000])