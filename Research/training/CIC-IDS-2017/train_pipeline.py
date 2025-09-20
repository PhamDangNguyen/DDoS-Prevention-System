import os
import json
import joblib
import pandas as pd
from typing import List, Optional
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split


# =========================
# Config
# =========================
INPUT_CSV  = r"..\..\data\CIC-IDS2017_processed\training\selected_dataset_raw.csv"   # đổi đường dẫn của bạn
OUTPUT_DIR = r"..\..\Output_model\CIC-IDS-2017"
USE_SCALING = True  # RandomForest không cần scale; nếu muốn bật thì đặt True


# =========================
# Helper: Enforce feature order & fill missing
# =========================
class ColumnOrderer(BaseEstimator, TransformerMixin):
    """
    - Chọn và sắp xếp cột theo danh sách 'columns' đã lưu.
    - Nếu thiếu cột ở transform(), sẽ tạo và fill giá trị fill_missing (mặc định 0).
    - Loại bỏ các cột thừa.
    """
    def __init__(self, columns: List[str], fill_missing: Optional[float] = 0.0):
        self.columns = list(columns)
        self.fill_missing = fill_missing

    def fit(self, X, y=None):
        # Kiểm tra thiếu cột ngay từ lúc fit
        missing = [c for c in self.columns if c not in X.columns]
        if missing and self.fill_missing is None:
            raise ValueError(f"Missing columns at fit: {missing}")
        return self

    def transform(self, X):
        X = X.copy()
        # Thêm cột thiếu
        missing = [c for c in self.columns if c not in X.columns]
        if missing:
            if self.fill_missing is None:
                raise ValueError(f"Missing columns at transform: {missing}")
            for c in missing:
                X[c] = self.fill_missing
        # Giữ đúng thứ tự cột
        X = X[self.columns]
        return X


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1) Đọc dữ liệu
    df = pd.read_csv(INPUT_CSV)

    # 2) Xác định nhãn y và danh sách feature
    #    Dữ liệu của bạn đã có 'label_mapped' => dùng cột này làm nhãn.
    if "label_mapped" not in df.columns:
        raise KeyError("Không thấy cột 'label_mapped'. Hãy tạo trước khi train.")

    y = df["label_mapped"].astype(str)

    # Loại bỏ Label/label_mapped khỏi X
    drop_cols = [c for c in ["Label", "label_mapped"] if c in df.columns]
    X = df.drop(columns=drop_cols)

    # Chỉ giữ các cột numeric (tránh lỗi nếu có cột text/string)
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    X = X[numeric_cols]

    # Lưu thứ tự cột (feature order)
    feature_order = numeric_cols[:]  # bản sao
    print(f"Feature count: {len(feature_order)}")

    # 3) Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # 4) Xây pipeline tiền xử lý + model
    steps = [
        ("order", ColumnOrderer(feature_order, fill_missing=0.0)),
    ]
    if USE_SCALING:
        steps.append(("scale", StandardScaler()))
    steps.append((
        "model",
        RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            class_weight="balanced_subsample",  # thường hữu ích cho dữ liệu mất cân bằng
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
    ))
    pipe = Pipeline(steps=steps)

    # 5) Train
    pipe.fit(X_train, y_train)

    # 6) Đánh giá
    y_pred = pipe.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
    print("Confusion matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification report:\n", classification_report(y_test, y_pred))

    # 7) Lưu artifact
    pipe_path = os.path.join(OUTPUT_DIR, "rf_pipeline.joblib")         # gồm preprocessor + model
    # model_path = os.path.join(OUTPUT_DIR, "random_forest_model.joblib")# chỉ model (optional)
    # preproc_path = os.path.join(OUTPUT_DIR, "preprocessor.joblib")     # chỉ preprocessor (order + scaler)
    # feat_path = os.path.join(OUTPUT_DIR, "feature_order.pkl")
    # classes_path = os.path.join(OUTPUT_DIR, "class_names.json")
    # report_path = os.path.join(OUTPUT_DIR, "classification_report.txt")

    # Lưu pipeline (khuyến nghị dùng cái này để infer dễ nhất)
    joblib.dump(pipe, pipe_path)

if __name__ == "__main__":
    main()