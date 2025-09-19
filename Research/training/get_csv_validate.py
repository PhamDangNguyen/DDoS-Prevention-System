import pandas as pd
from pathlib import Path

# ==== CẤU HÌNH ====
INPUT_CSV = r"C:\Code\DDoS-Prevention-System\Research\data\CIC-IDS2017\Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv"          # Đổi thành đường dẫn file của bạn
OUTPUT_CSV = r"filtered_sampled_2.csv"  # File CSV output

# Liệt kê các cột bạn muốn giữ (KHÔNG gồm Label, mình sẽ tự thêm Label)
KEEP_COLS = [
    "PSH Flag Count","min_seg_size_forward","Flow IAT Max","Flow IAT Min",
    "ACK Flag Count","Destination Port","Bwd Packet Length Mean","Bwd Packet Length Max",
    "Bwd Packet Length Min","Init_Win_bytes_forward","Fwd IAT Max","Idle Mean","Idle Max",
    "Avg Bwd Segment Size","Bwd Packet Length Std","Bwd IAT Mean","Fwd IAT Std","Down/Up Ratio",
    "Max Packet Length","Average Packet Size","Min Packet Length","Packet Length Std",
    "Fwd Packets/s","Packet Length Mean","Flow IAT Std","URG Flag Count","FIN Flag Count",
    "Fwd Packet Length Min","Subflow Fwd Packets","Bwd IAT Max","Packet Length Variance",
    "Fwd IAT Mean","Flow Duration","Fwd IAT Total","Bwd IAT Std","Flow IAT Mean"
]
N_PER_CLASS = 10
RANDOM_STATE = 42
# ===================

# 1) Đọc CSV
df = pd.read_csv(INPUT_CSV)
df.columns = (
    df.columns
      .astype(str)
      .str.replace('\ufeff', '', regex=False)   # bỏ BOM nếu có
      .str.replace('\u00A0', ' ', regex=False)  # NBSP -> space thường
      .str.strip()                               # bỏ space đầu/cuối
)

# 2) Tìm cột Label (khớp không phân biệt hoa/thường)
label_col = None
for c in df.columns:
    if c.casefold() == "label":
        label_col = c
        break
if label_col is None:
    raise KeyError("Không tìm thấy cột 'Label' trong file CSV.")

# 3) Lọc chỉ các cột cần + Label (tự động bỏ qua cột không tồn tại)
keep = [c for c in KEEP_COLS if c in df.columns]
if label_col not in keep:
    keep.append(label_col)
df_keep = df[keep].copy()

# 4) Lấy tối đa N_PER_CLASS mẫu cho mỗi class Label
df_sampled = (
    df_keep.groupby(label_col, group_keys=False)
           .apply(lambda g: g.sample(n=min(N_PER_CLASS, len(g)), random_state=RANDOM_STATE))
           .reset_index(drop=True)
)

# 5) Lưu CSV
Path(OUTPUT_CSV).parent.mkdir(parents=True, exist_ok=True)
df_sampled.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
print(f"✅ Saved: {OUTPUT_CSV}")
print(df_sampled[label_col].value_counts())
