# Kiến trúc chung của IDS system
```text
┌────────────────────────┐
│ 1️⃣ Packet Capture      │   ← scapy / cicflowmeter
│  (Sniff or PCAP input) │
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────┐
│ 2️⃣ Flow Generation     │   ← cicflowmeter.flow_session
│  (Extract 80+ features)│
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────┐
│ 3️⃣ Pre-processing      │   ← xử lý thiếu dữ liệu, chuẩn hoá,
│  (Normalization/Scaling│      encoding categorical features, v.v.)
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────┐
│ 4️⃣ Machine Learning    │
│     Model Inference     │
│  ➤ Random Forest Classifier │
│    (hoặc ExtraTrees/ETC)│
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────┐
│ 5️⃣ Threat Detection    │
│  (Normal / Attack type) │  → ví dụ: DDoS, PortScan, BruteForce...
└──────────┬─────────────┘
           │
           ▼
┌────────────────────────┐
│ 6️⃣ API Response / Log  │   ← FastAPI endpoint `/CIC-IDS2017`
│  (JSON output + CSV)    │
└────────────────────────┘
```
## 1. Packet Capture – Giai đoạn thu thập gói tin
**Mô tả**:
Đây là bước đầu tiên, nơi hệ thống sử dụng Scapy hoặc module cicflowmeter để bắt (sniff) các gói tin trực tiếp từ giao diện mạng (ví dụ Wi-Fi, eth0) hoặc đọc từ tệp .pcap.
Mỗi gói tin chứa thông tin cơ bản như: địa chỉ IP nguồn/đích, cổng, giao thức (TCP, UDP, ICMP), kích thước gói, và thời gian gửi.

**Vai trò**:  
Cung cấp dữ liệu thô đầu vào cho hệ thống.  
Giữ nguyên toàn bộ ngữ cảnh lưu lượng mạng thật.  
Có thể hoạt động theo hai chế độ:  
- Online mode: bắt gói tin trực tiếp.  
- Offline mode: đọc tệp .pcap.  
## 2. Flow Generation – Tạo luồng dữ liệu (Flow)
**Mô tả**:
Các gói tin sau khi thu thập sẽ được nhóm (aggregate) thành flows dựa trên 5-tuple:
(source IP, destination IP, source port, destination port, protocol).  

Module cicflowmeter.flow_session sẽ tính toán hơn 80 đặc trưng thống kê cho mỗi flow, bao gồm:

- Thông tin cơ bản: src_ip, dst_ip, src_port, dst_port, protocol

- Đặc trưng thống kê: flow_duration, flow_byts_s, flow_pkts_s

- Đặc trưng hướng truyền: fwd_packet_length_mean, bwd_packet_length_std

- Đặc trưng thời gian: flow_iat_mean, active_mean, idle_mean, v.v.
## 3. Pre-processing – Tiền xử lý dữ liệu
**Mô tả**:
Ở bước này, hệ thống chuẩn hóa và xử lý dữ liệu để đảm bảo chất lượng đầu vào cho mô hình học máy.
Các công việc chính bao gồm:

- Xử lý giá trị thiếu (NaN) bằng phương pháp trung bình, mode, hoặc median.

- Chuẩn hóa (Normalization / Standardization) các đặc trưng số để đảm bảo chúng cùng thang đo (min-max scaling hoặc z-score).

- Mã hóa dữ liệu phân loại (Label Encoding / One-hot Encoding) với các trường như protocol_type hay service.

- Loại bỏ hoặc chọn lọc đặc trưng (Feature selection) nhằm giảm nhiễu và tăng hiệu năng mô hình.

**Vai trò**:

- Đảm bảo dữ liệu sạch, đồng nhất và tối ưu cho quá trình dự đoán.

- Chuẩn bị input vector chính xác cho mô hình Random Forest.

## 4. Machine Learning Model Inference – Dự đoán bằng mô hình học máy (Random Forest) 
**Mô tả:**
Đây là trái tim của hệ thống IDS. Sau khi có dữ liệu đã được chuẩn hóa, hệ thống sẽ chuyển vector đặc trưng (feature vector) đến mô hình học máy để phân loại lưu lượng mạng.

Tại đây, thuật toán Random Forest Classifier được sử dụng.
Random Forest là mô hình học máy dựa trên tập hợp (ensemble) của nhiều cây quyết định (Decision Trees), hoạt động theo cơ chế:

- Mỗi cây học trên một tập con ngẫu nhiên của dữ liệu (bagging).

- Khi dự đoán, mỗi cây “bỏ phiếu” cho nhãn (normal/attack).

- Kết quả cuối cùng là nhãn có số phiếu nhiều nhất, giúp giảm overfitting và tăng độ chính xác.

**Cách hệ thống sử dụng RF:**

- Trong giai đoạn huấn luyện (training): dữ liệu từ bộ CIC-IDS2017 / NSL-KDD được chia train/test, huấn luyện mô hình Random Forest để học được các mẫu hành vi tấn công.

- Trong giai đoạn suy luận (inference/runtime): mô hình RF đã huấn luyện được tải vào FastAPI backend; mỗi flow mới sinh ra sẽ được gửi đến model này để phân loại.
## 5. Threat Detection – Phát hiện và phân loại tấn công
**Mô tả:**
Sau khi mô hình RF trả về nhãn dự đoán, hệ thống sẽ diễn giải kết quả đó theo từng loại tấn công cụ thể.
Ví dụ:

Normal → Lưu lượng hợp lệ.

DDoS → Lưu lượng tấn công từ chối dịch vụ.

Unauthorized access → Tấn công truy cập trái phép

Vai trò:

Cung cấp kết quả nhận diện tấn công cụ thể.

Có thể dùng để kích hoạt các hành động phản ứng (alert, block IP, log event) về sau.

## API Response / Logging – Trả kết quả và lưu log
**Mô tả:**
Kết quả cuối cùng được đóng gói lại dưới dạng JSON và gửi về client qua API FastAPI, ví dụ:
```json
{
  "src_ip": "192.168.1.12",
  "dst_ip": "10.0.0.8",
  "protocol": "TCP",
  "prediction": "DDoS",
  "confidence": 0.984
}
```
Đồng thời, hệ thống cũng ghi lại toàn bộ các flow đã xử lý cùng nhãn dự đoán vào file .csv để phục vụ thống kê và huấn luyện lại trong tương lai.