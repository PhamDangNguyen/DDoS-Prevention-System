# DDoS-Prevention-System

Hệ thống này là một **Hệ thống Phát hiện và Ngăn chặn Xâm nhập (IDPS)** dựa trên **Machine Learning**, được huấn luyện để phân loại lưu lượng mạng thành ba nhóm chính:
- **Tấn công DDoS (DDos)** – lưu lượng độc hại với mục đích làm tê liệt và gián đoạn dịch vụ mạng.  
- **Truy cập trái phép(Unauthorized Access)** – các hành vi cố gắng xâm nhập hệ thống hoặc tài nguyên khi chưa được cấp quyền.  
- **Lưu lượng bình thường (Normal)** – hoạt động mạng hợp lệ, an toàn và không gây hại.  

Các mô hình được huấn luyện và đánh giá trên hai bộ dữ liệu chuẩn nổi tiếng:  
- **NSL-KDD** – [phiên bản cải tiến](https://www.unb.ca/cic/datasets/nsl.html) của bộ dữ liệu KDD’99, thường được sử dụng trong nghiên cứu phát hiện xâm nhập.  
  Đặc biệt, bộ dữ liệu này thường được áp dụng để đánh giá hiệu quả của các hệ thống phát hiện xâm nhập trong **môi trường Internet of Things (IoT)**, nơi cần những giải pháp bảo mật gọn nhẹ và hiệu quả.  

- **CIC-IDS2017** – [bộ dữ liệu hiện đại](https://www.unb.ca/cic/datasets/ids-2017.html) do **Canadian Institute for Cybersecurity, Đại học New Brunswick (Canada)** xây dựng.  
  Mục tiêu chính là mô phỏng **môi trường mạng doanh nghiệp/tổ chức**, bao gồm cả lưu lượng hợp lệ và các kịch bản tấn công đa dạng, sát với thực tế.  

# Hướng dẫn Repository
Repository này được chia thành ba phần chính, minh họa trong sơ đồ dưới đây và giải thích chi tiết phía sau:
```
DDoS-Prevention-System
        |__ Document
        |    |__ Paper research
        |    |  | . . . 
        |    |
        |    |__Service Doc
        |       | . . .
        |
        |__ IDS_service    
        |    |__ config
        |    |  | . . .
        |    |__ models
        |    |  | . . .
        |    |__ . . .
        |    
        |__ Research     
             |__ data_preprocessing
            |  | . . .
            |__ training
            |  |. . .
            |__ . . .
        
```

## Document
Thư mục **Document** lưu trữ các tài liệu liên quan, bao gồm bài nghiên cứu về các mẫu data, tài liệu thiết kế hệ thống.  
Bạn có thể truy cập trực tiếp tại [Document](Document).  

## IDS service
**IDS_system** là dịch vụ trung tâm của dự án.  
Được phát triển bằng **FastAPI**, thành phần này chịu trách nhiệm phát hiện và xử lý các yêu cầu độc hại.  
Nhấn vào [IDS_system](IDS_service) để khám phá chi tiết.  

## Research
Thư mục **Research** được tổ chức thành nhiều tiểu mục, bao gồm *crawl_data*, *training*, *inference* và *preprocessing*.  
Các tiểu mục này tạo thành quy trình nghiên cứu toàn diện: từ thu thập và làm sạch dữ liệu, thử nghiệm nhiều mô hình khác nhau, lựa chọn đặc trưng, cho tới xây dựng pipeline huấn luyện.  

Đây là nơi lưu giữ toàn bộ kết quả thí nghiệm, quyết định thiết kế và các bước tiến hành trong quá trình nghiên cứu.  
Để xem bản triển khai, nhấn vào [Research](Research).  
