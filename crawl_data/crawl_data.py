from datasets import load_dataset

ds = load_dataset("c01dsnap/CIC-IDS2017")

print(ds["train"][500000])

importance_features = [ "Source IP", "Flow Bytes/s"

]