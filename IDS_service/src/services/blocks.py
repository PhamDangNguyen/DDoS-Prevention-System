from sklearn.base import BaseEstimator, TransformerMixin
from typing import List, Optional
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