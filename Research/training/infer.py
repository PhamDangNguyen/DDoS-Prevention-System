# infer.py
import joblib, pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

# --- copy y nguyên class đã dùng khi train ---
class ColumnOrderer(BaseEstimator, TransformerMixin):
    def __init__(self, columns, fill_missing=0.0):
        self.columns = list(columns)
        self.fill_missing = fill_missing

    def fit(self, X, y=None):
        # (có thể check missing tại fit)
        return self

    def transform(self, X):
        X = X.copy()
        missing = [c for c in self.columns if c not in X.columns]
        if missing:
            for c in missing:
                X[c] = self.fill_missing
        X = X[self.columns]
        return X
# --------------------------------------------

PIPELINE_PATH = r"C:\Code\DDoS-Prevention-System\Research\Output_model\CIC-IDS-2017\rf_pipeline.joblib"
pipe = joblib.load(PIPELINE_PATH)  # giờ sẽ load được

def predict_one(pipe, point: dict) -> dict:
    df_one = pd.DataFrame([point]).select_dtypes(include=["number"])
    pred = pipe.predict(df_one)[0]
    out = {"prediction": str(pred), "probas": None}
    if hasattr(pipe.named_steps["model"], "predict_proba"):
        prob = pipe.predict_proba(df_one)[0]
        classes = pipe.named_steps["model"].classes_.tolist()
        out["probas"] = {cls: float(p) for cls, p in zip(classes, prob)}
    return out

if __name__ == "__main__":
    pipe = joblib.load(PIPELINE_PATH)

    new_point = {
        "PSH Flag Count": 0,
        "min_seg_size_forward": 20,
        "Flow IAT Max": 500,
        "Flow IAT Min": 5,
        "ACK Flag Count": 1,
        "Destination Port": 443,
        "Bwd Packet Length Mean": 120.0,
        "Bwd Packet Length Max": 300,
        "Bwd Packet Length Min": 0,
        "Init_Win_bytes_forward": 256,
        "Fwd IAT Max": 400,
        "Idle Mean": 0.0,
        "Idle Max": 0,
        "Avg Bwd Segment Size": 110.0,
        "Bwd Packet Length Std": 50.0,
        "Bwd IAT Mean": 100.0,
        "Fwd IAT Std": 30.0,
        "Down/Up Ratio": 1,
        "Max Packet Length": 512,
        "Average Packet Size": 128.0,
        "Min Packet Length": 20,
        "Packet Length Std": 40.0,
        "Fwd Packets/s": 2000.0,
        "Packet Length Mean": 100.0,
        "Flow IAT Std": 60.0,
        "URG Flag Count": 0,
        "FIN Flag Count": 0,
        "Fwd Packet Length Min": 20,
        "Subflow Fwd Packets": 10,
        "Bwd IAT Max": 450,
        "Packet Length Variance": 1600.0,
        "Fwd IAT Mean": 80.0,
        "Flow Duration": 1000,
        "Fwd IAT Total": 800,
        "Bwd IAT Std": 40.0,
        "Flow IAT Mean": 85.0,
        # không cần Label/label_mapped khi predict
    }
    res = predict_one(pipe, new_point)
    print(res)
