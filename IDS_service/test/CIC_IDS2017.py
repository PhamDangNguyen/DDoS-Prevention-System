# NSL_KDD.py (ví dụ)
import sys, requests
import random
URL = "http://127.0.0.1:8080/CIC-IDS2017"   # <-- dùng 127.0.0.1 hoặc localhost
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
PAYLOAD = {
        "psh_flag_count": random.randint(0, 1),                 # cờ 0/1
        "min_seg_size_forward": random.randint(0, 50),          # bytes nhỏ
        "flow_iat_max": random.randint(1, 5000),                # microseconds/ms
        "flow_iat_min": random.randint(0, 100),
        "ack_flag_count": random.randint(0, 10),
        "destination_port": random.choice([80, 443, 21, 22, 53, 8080, 3306]),
        "bwd_packet_length_mean": round(random.uniform(0, 1500), 2),  # MTU max 1500
        "bwd_packet_length_max": random.randint(0, 1500),
        "bwd_packet_length_min": random.randint(0, 500),
        "init_win_bytes_forward": random.randint(0, 65535),
        "fwd_iat_max": random.randint(1, 5000),
        "idle_mean": round(random.uniform(0, 1000), 2),
        "idle_max": random.randint(0, 5000),
        "avg_bwd_segment_size": round(random.uniform(0, 1500), 2),
        "bwd_packet_length_std": round(random.uniform(0, 500), 2),
        "bwd_iat_mean": round(random.uniform(0, 2000), 2),
        "fwd_iat_std": round(random.uniform(0, 2000), 2),
        "down_up_ratio": random.randint(0, 10),
        "max_packet_length": random.randint(40, 1500),
        "average_packet_size": round(random.uniform(40, 1000), 2),
        "min_packet_length": random.randint(0, 100),
        "packet_length_std": round(random.uniform(0, 500), 2),
        "fwd_packets_s": round(random.uniform(0, 10000), 2),
        "packet_length_mean": round(random.uniform(40, 1000), 2),
        "flow_iat_std": round(random.uniform(0, 2000), 2),
        "urg_flag_count": random.randint(0, 1),
        "fin_flag_count": random.randint(0, 1),
        "fwd_packet_length_min": random.randint(0, 100),
        "subflow_fwd_packets": random.randint(1, 20),
        "bwd_iat_max": random.randint(1, 5000),
        "packet_length_variance": round(random.uniform(0, 500000), 2),
        "fwd_iat_mean": round(random.uniform(0, 2000), 2),
        "flow_duration": random.randint(1, 100000),             # ms
        "fwd_iat_total": random.randint(0, 50000),
        "bwd_iat_std": round(random.uniform(0, 2000), 2),
        "flow_iat_mean": round(random.uniform(0, 2000), 2),
    }

try:
    r = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=5)
    print("Status:", r.status_code)
    print("Body:", r.text)
except requests.RequestException as e:
    print("Request failed:", e, file=sys.stderr)
    sys.exit(1)
