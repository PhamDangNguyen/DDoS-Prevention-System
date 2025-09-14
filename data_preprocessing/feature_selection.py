from datasets import load_dataset
ds = load_dataset("c01dsnap/CIC-IDS2017")
print(ds["train"][500000])

importance_features = [
    "Idle Max", "Idle Mean", "Flow Duration", 
    "Packet Length Std", "Idle Min", "FIN Flag Count", "SYN Flag Count", "RST Flag Count", "PSH Flag Count", "ACK Flag Count", "URG Flag Count", "CWE Flag Count","ECE Flag Count",
    "",
]