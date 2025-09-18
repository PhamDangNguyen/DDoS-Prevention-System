import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
from sklearn.model_selection import train_test_split
# 1. Đọc dữ liệu
df_all = pd.read_csv(r"..\data\CIC-IDS2017_processed\training\all_95.csv")

# 2. Tách features (X) và label (y)
X = df_all.drop(columns=["Label"])
y = df_all["Label"]

# 3. Chia train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# 4. Khởi tạo mô hình RandomForest
rf = RandomForestClassifier(
    n_estimators=100,
    max_depth=None,
    random_state=42,
    verbose=1,
    n_jobs=-1
)

# 5. Train
rf.fit(X_train, y_train)

# 6. Dự đoán
y_pred = rf.predict(X_test)

# 7. Đánh giá
print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
joblib.dump(rf, r"..\Output_model\CIC-IDS-2017\random_forest_model.pkl")
joblib.dump(list(X.columns), r"..\Output_model\CIC-IDS-2017\feature_order.pkl")
print("RF Model saved!")