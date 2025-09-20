import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.base import BaseEstimator, TransformerMixin

# --- Phải định nghĩa lại y như lúc train để joblib.load pipeline không lỗi ---
class ColumnOrderer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, fill_missing=0.0):
        self.columns = list(columns)
        self.fill_missing = fill_missing
    def fit(self, X, y=None): return self
    def transform(self, X):
        X = X.copy()
        for c in self.columns:
            if c not in X.columns:
                X[c] = self.fill_missing
        return X[self.columns]
# ---------------------------------------------------------------------------

PIPELINE_PATH = r"..\..\Output_model\CIC-IDS-2017\rf_pipeline.joblib"
INPUT_CSV     = r"validate\filtered_sampled.csv"

# 1) Load pipeline
pipe = joblib.load(PIPELINE_PATH)

# 2) Đọc CSV và clean tên cột
df = pd.read_csv(INPUT_CSV, low_memory=False)
df.columns = (
    df.columns.astype(str)
              .str.replace('\ufeff', '', regex=False)  # BOM
              .str.replace('\u00A0', ' ', regex=False) # NBSP -> space
              .str.replace(r'\s+', ' ', regex=True)    # gộp nhiều space
              .str.strip()
)

# 3) Map Label -> label_mapped (đủ đầy đủ các nhãn CIC-IDS2017 phổ biến)
def map_label(s: str) -> str:
    s = str(s).strip()
    mapping = {
        'BENIGN': 'Normal',
        'DoS Hulk': 'DDoS',
        'DoS GoldenEye': 'DDoS',
        'DoS slowloris': 'DDoS',
        'DoS Slowhttptest': 'DDoS',
        'DDoS': 'DDoS',
        'PortScan': 'Unauthorized Access',
        'FTP-Patator': 'Unauthorized Access',
        'SSH-Patator': 'Unauthorized Access',
        'Web Attack � Brute Force': 'Unauthorized Access',
        'Web Attack � XSS': 'Unauthorized Access',
        'Web Attack � Sql Injection': 'Unauthorized Access',
        'Web Attack � SQL Injection': 'Unauthorized Access',
        'Infiltration': 'Unauthorized Access',
        'Bot': 'Unauthorized Access',
        'Heartbleed': 'Unauthorized Access',
    }
    return mapping.get(s, 'Other')

if 'label_mapped' not in df.columns:
    if 'Label' not in df.columns:
        raise KeyError("Không thấy cột 'Label' trong file.")
    df['label_mapped'] = df['Label'].map(map_label)

# 4) Chọn feature (bỏ Label/label_mapped), giữ numeric, fill NA
feature_cols = [c for c in df.columns if c not in ('Label', 'label_mapped')]
X = df[feature_cols].select_dtypes(include=[np.number]).fillna(0.0)
y_true = df['label_mapped'].astype(str)

# 5) Predict & đánh giá
y_pred = pipe.predict(X)

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Confusion matrix:\n", confusion_matrix(y_true, y_pred))
print("Classification report:\n", classification_report(y_true, y_pred))

# (tuỳ chọn) xem phân bố nhãn thật & dự đoán:
print("y_true counts:\n", y_true.value_counts())
print("y_pred counts:\n", pd.Series(y_pred).value_counts())
