# I. IDS Service

Đây là service chính của **DDoS Prevention System**, được xây với **FastAPI**.  
Nó cung cấp 2 endpoints:  
- **CIC-IDS2017** dataset endpoint  
- **NSL-KDD** dataset endpoint  

---

## Điều kiện tiên quyết
- [Docker](https://docs.docker.com/get-docker/) installed  
- [Docker Compose](https://docs.docker.com/compose/install/) installed  
- Python 3.10+ (for local testing scripts)  
- Download model từ Google driver theo [link](https://drive.google.com/drive/folders/1OgVOAnj52M3MJOGkwx9kn883yW4EXKET?usp=sharing) và đặt vào trong thư mục IDS_service
```
|__ IDS_service    
|    |__ models
|       | . . .
```
---

## Chạy Service
Để chạy service lên cần làm các bước (giả định thư mục root đang đứng là DDoS-Prevention-System):
```bash
cd IDS_service
docker-compose up --build -d
```
## Tắt Service
Để tắt service đi cần làm các bước (giả định thư mục root đang đứng là DDoS-Prevention-System):
```bash
cd IDS_service
docker-compose down
```
## API Endpoints
URL có sẵn để sử dụng sau khi run docker:

* **CIC-IDS2017 URL**: http://127.0.0.1:8080/CIC-IDS2017
* **NSL-KDD URL**: http://127.0.0.1:8080/NSL-KDD


# II. Hệ thống testing the Service using Cicflowmeter
Sau khi service lên rồi bạn có thể test service sử dụng Python scripts sau:
### B1.Tạo môi trường test bằng conda
```bash
cd IDS_service/test
conda create --name ddos python=3.10
conda activate ddos
pip install -r requirements.txt
```
### B2. Test service bằng python file
```bash
cd /test
python CIC_IDS2017.py
python NSL_KDD.py
```

## Testing the Service using cicflowmeter (Ubuntu)
Để sử dụng tool cicflowmeter, ta có thể thực hiện như sau
### B1.Tạo môi trường test mới bằng conda
```bash
cd IDS_service/test
conda create --name test_ddos python=3.10
conda activate tets_ddos
pip install cicflowmeter==0.1.6
pip install scapy==2.4.3
pip install numpy==1.26.4
pip install requests==2.32.5
```

### B2: Sửa thư viện
Trong folder [resource](resource) copy tất cả các thông tin sau vào thư mục cicflowmeter trong môi trường conda tại "anaconda3/envs/ddos/lib/python3.10/site-packages/cicflowmeter/".  
Bố trí thư mục như sau:
```json
|__ cicflowmeter    
|    |__ features
|    |   |__ flow_bytes.py
|    |   |__ ....
|    |__ flow_session.py
|    |__ flow.py
|    |__ sniffer.py

```
**Note**:  ```flow_bytes.py``` sẽ được để trong folder **features** còn  ```flow_session.py```, ```flow.py```, ```sniffer.py``` thì để thẳng trong folder cha là cicflowmeter.

### B3. Chạy tool cicflowmeter
```bash
ifconfig # Lấy tên một interface muốn theo dõi
sudo cicflowmeter -i {interface_name} -u http://localhost:8080/CIC-IDS2017
```
Ex: ```cicflowmeter -i "Wi-Fi" -c flow.csv -u http://localhost:8080/CIC-IDS2017```