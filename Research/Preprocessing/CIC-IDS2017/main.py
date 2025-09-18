from flow_process import preprocessor
from datasets import load_dataset
from resolve_imbalance_data import balance_cicids2017_with_smote
# 1. Crawl data
preprocessor_CICIDS2017 = preprocessor("CIC-IDS2017")
ds = load_dataset("c01dsnap/CIC-IDS2017")
small_ds = ds['train'].select(range(20000)) 
# Lấy 10 dòng để test
data_frame_norm = preprocessor_CICIDS2017.norm_name_columes(small_ds)

# 2. Define important columns features
importance_colums = [
    "PSH Flag Count", "min_seg_size_forward", "Flow IAT Max", "Flow IAT Min", "ACK Flag Count", "Destination Port", "Bwd Packet Length Mean", "Bwd Packet Length Max", "Bwd Packet Length Min", "Init_Win_bytes_forward",
    "Fwd IAT Max", "Idle Mean", "Idle Max", "Avg Bwd Segment Size", "Bwd Packet Length Std", "Bwd IAT Mean", "Fwd IAT Std", "Down/Up Ratio", "Max Packet Length", "Average Packet Size",
    "Min Packet Length", "Packet Length Std", "Fwd Packets/s", "Packet Length Mean", "Flow IAT Std", "URG Flag Count", "FIN Flag Count", "Fwd Packet Length Min", "Subflow Fwd Packets", "Bwd IAT Max",
    "Packet Length Variance", "Fwd IAT Mean", "Flow Duration", "Fwd IAT Total", "Bwd IAT Std", "Flow IAT Mean"
]
# 3. Map label to 3 classes: DDoS, Normal, Unauthorized Access
data_frame_mapping = preprocessor_CICIDS2017.mapping_label(data_frame_norm)
print(data_frame_mapping["label_mapped"])
# 4. Select important columns
data_frame_selected = preprocessor_CICIDS2017.select_columns(data_frame_mapping, importance_colums + ["Label"] + ["label_mapped"])
print(data_frame_selected)  # Dataset sau khi đã chọn các cột quan trọng
#5. Standardize data
data_frame_standardized = preprocessor_CICIDS2017.scale_numerical_features(data_frame_selected, importance_colums)
print(data_frame_standardized)  # Dataset sau khi đã chuẩn hóa
#6 Resolve imbalance data
ds_balanced = balance_cicids2017_with_smote(data_frame_standardized, label_category_mapping=None, importance_columns=importance_colums, verbose=True)
print(ds_balanced)  # Dataset sau khi đã cân bằng lại dữ liệu