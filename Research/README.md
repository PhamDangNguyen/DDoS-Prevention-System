# Research folder
Đây là thư mục nghiên cứu toàn diện chứa code về  *crawl_data*, *training*, *inference* và *preprocessing*.  
Các tiểu mục này tạo thành quy trình nghiên cứu toàn diện: từ thu thập và làm sạch dữ liệu, thử nghiệm nhiều mô hình khác nhau, lựa chọn đặc trưng, cho tới xây dựng pipeline huấn luyện.  
## Điều kiện tiên quyết
- Nên dùng Python 3.10+.
- Laptop or server GPU or CPU 16G ram.
### Chuẩn bị môi trường
Thư mục này cần chuẩn bị môi trường sau (giả định đang đứng tại thư mục root):
```
cd Research
conda create --name ddos python=3.10
conda activate ddos
pip install -r requirements.txt
```
## Pipeline xử lý
### Crawl data
Cả 2 bộ **NSL-KDD** và **CIC-IDS-2017** đều có thể dựa vào kaggle hoặc huggingface để crawl, chi tiết có thể tham khảo [Crawl data folder](crawl_data).

### Feature selection
**NSL-KDD**: Phương pháp lựa chọn feature cho tập này chính là Mutual Information (MI) - đo mức độ phụ thuộc (dependency) giữa feature và label cả tuyến tính và phi tuyến tính. Nếu MI cao → feature đó có nhiều thông tin để phân biệt class → nên giữ lại. Thông tin trong mục Feature Engineering của file [eda_NSL_KDD.ipynb](notebook/eda_NSL_KDD.ipynb).

**CIC-IDS2017**: Dựa vào paper [Enhanced Intrusion Detection via Hybrid Data Resampling and Feature Optimization - table3 release 21/08/2025](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=11141474) với phương pháp chính là  Extra Trees Classifier (ETC) chọn ra 42 feature tiềm năng nhất và từ đó lọc ra được 36 feature quan trọng nhất đối với tập data này. Bản .PDF của paper được đặt ở [Document/Paper research](../Document/Paper%20research)

### Preprocessing
**NSL-KDD**: 
* Xử lý dữ liệu:
1. Map các label attack về 3 lớp normal, dos, unauthorized. (phần ***Read the dataset*** của [eda_NSL_KDD.ipynb](notebook/eda_NSL_KDD.ipynb))
2. eda kiểm tra và loại null, nan và duplicate dữ liệu. (Trong phần ***Data Cleaning*** của [eda_NSL_KDD.ipynb](notebook/eda_NSL_KDD.ipynb))
3. Encoder các categorical label. (Trong phần ***Encoding*** của [eda_NSL_KDD.ipynb](notebook/eda_NSL_KDD.ipynb))
4. StandardScaler dữ liệu. (Phần ***Scaling*** của [eda_NSL_KDD.ipynb](notebook/eda_NSL_KDD.ipynb))
**CIC-IDS2017**: 
* Xử lý dữ liệu:
1. Load data từ Huggingface và Visualize các feature colums. (phần ***Load data*** của [eda-CICIDS2017.ipynb](notebook/eda-CICIDS2017.ipynb))
2. Chuẩn hóa tên của các feature colums để xóa đi những khoảng trẳng. (phần ***Norm name of feature colums*** của [eda-CICIDS2017.ipynb](notebook/eda-CICIDS2017.ipynb))
3. Map các label attack về 3 lớp Normal, DDoS, Unauthorized Access. (phần ***Mapping label*** của [eda-CICIDS2017.ipynb](notebook/eda-CICIDS2017.ipynb))
4. StandardScaler dữ liệu về cùng một thang gần nhau. (phần ***Scaler*** của [eda-CICIDS2017.ipynb](notebook/eda-CICIDS2017.ipynb)) 
5. Xử lý sự mất cân bằng dữ liệu (phần ***Resolve Imbalance data*** của [eda-CICIDS2017.ipynb](notebook/eda-CICIDS2017.ipynb))

### Training and infer
**NSL-KDD**: 
1. ***Training***  
Training file được đặt ở folder [NSL-KDD](training/NSL-KDD/train.py) có thể chạy bằng CMD như sau:
    ```
    cd Research/training/NSL-KDD
    python train.py --train_path ../datasets/KDDTrain+.txt --save_path ../Output_model/NSL_KDD/random_forest_model.pkl  
    ```
    Với:
    - train_path là file .txt data train đã qua xử lý.
    - save_path là nơi lưu trữ model output.
2. ***Infer***
Infer file được đặt ở folder [NSL-KDD](training/NSL-KDD/inference.py) có thể chạy bằng CMD như sau:
    ```
    cd Research/training/NSL-KDD
    python inference.py --test_path path_to_csv_file_test --save_path ../Output_model/NSL_KDD/random_forest_model.pkl    
    ```
    Với:
    - test_path file .csv mà bạn muốn bao gồm data đã xử lý.
    - save_path path model muốn load lên.

**CIC-IDS-2017**: 
1. ***Training***  
Training file được đặt ở folder [CIC-IDS-2017](training/CIC-IDS-2017/train_pipeline.py)  
Chú ý thay các trường:
    ```
    INPUT_CSV: đổi đường dẫn tới file .csv train
    OUTPUT_DIR: Model train xong sẽ save vào folder này
    USE_SCALING: Muốn dùng Scaler thì bật lên đặt bằng True
    ```
    có thể chạy bằng CMD như sau:
        ```
        cd Research/training/CIC-IDS-2017
        python train_pipeline.py
        ```  

2. ***Infer***
Infer file được đặt ở folder [CIC-IDS-2017](training/CIC-IDS-2017/infer.py)   
Chú ý thay đổi các trường sau:
    ```
    PIPELINE_PATH: Đây là path tới model được train với tập data CIC-IDS-2017 để load.
    new_point: Trường data này có thể thay đổi từng feature colum để test.
    ```

    có thể chạy bằng CMD như sau
        ```
    cd Research/training/CIC-IDS-2017
    python infer.py
        ```  