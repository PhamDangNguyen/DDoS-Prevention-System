# Huấn luyện mô hình
Chi tiết xem tại file [Notebook](Research/notebook/eda_NSL_KDD.ipynb)
1. **Xử lý dữ liệu**
- Map các nhãn ở cột attack trong tập dữ liệu sang ba nhãn normal, dos, unauthorized_access.
- Phân tích dữ liệu, kiểm tra bộ dữ liệu có chứa các trường thông tin null, nan hoặc duplicate hay không.
2. **Training model**
- Chuyển các label dạng categorical (kiểu dữ liệu string) sang interger thông qua thư viện **preprocessing.LabelEncoder()** trong sklearn.
- Trích chọn feature quan trọng, tính điểm số biểu thị độ quan trọng của các feature trong bộ dữ liệu (sử dụng thư viện **mutual_info_classif** trong sklearn). Từ đó lấy 15 features có điểm số cao nhất.
- Chuẩn hóa dữ liệu, đưa các cột feature về dạng phân phối của có kỳ vọng bằng 0 và phương sai bằng 1 (sử dụng thư viện **StandardScaler** trong sklearn).
- Lựa chọn mô hình, huấn luyện và đánh giá mô hình.