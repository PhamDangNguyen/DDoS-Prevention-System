from datasets import load_dataset
ds = load_dataset("c01dsnap/CIC-IDS2017")
print(ds["train"][500000])

importance_features = [
    "PSH Flag Count", "Flow IAT Max", "min_seg_size_forward", "ACK Flag Count",
    "Bwd Packet Length Mean", "Bwd Packet Length Max", "Idle Min", "Init_Win_bytes_forward",
    "Fwd IAT Max", "Idle Mean", "Idle Max", "Avg Bwd Segment Size",
    "Destination Port", "Bwd Packet Length Min", "Bwd Packet Length Std", "Fwd IAT Std",
    "Down/Up Ratio", "Max Packet Length", "Average Packet Size", "Min Packet Length",
    "Packet Length Std", "Fwd Packets/s", "Packet Length Mean", "Flow IAT Std",
    "URG Flag Count", "FIN Flag Count", "Fwd Packet Length Min", "Bwd IAT Max",
    "Packet Length Variance", "Fwd IAT Mean", "Flow Duration", "Fwd IAT Total", 
    "Bwd IAT Std", "Flow IAT Mean"
    ]