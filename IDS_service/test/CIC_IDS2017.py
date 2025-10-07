# NSL_KDD.py (ví dụ)
import sys, requests
import random
import time
URL = "http://127.0.0.1:8080/CIC-IDS2017"   # <-- dùng 127.0.0.1 hoặc localhost
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
PAYLOAD = {
    "src_ip": f"192.168.0.{random.randint(1, 255)}",
    "dst_ip": f"10.0.0.{random.randint(1, 255)}",
    "src_port": random.randint(1024, 65535),
    "dst_port": random.choice([80, 443, 21, 22, 53, 8080, 3306]),
    "protocol": random.choice([6, 17, 1]),  # TCP=6, UDP=17, ICMP=1
    "timestamp": int(time.time()),
    "flow_duration": random.randint(1, 100000),

    # flow-level stats
    "flow_byts_s": round(random.uniform(0, 10), 2),
    "flow_pkts_s": round(random.uniform(0, 10000), 2),
    "fwd_pkts_s": round(random.uniform(0, 10000), 2),
    "bwd_pkts_s": round(random.uniform(0, 10000), 2),

    "tot_fwd_pkts": random.randint(0, 1000),
    "tot_bwd_pkts": random.randint(0, 1000),
    "totlen_fwd_pkts": random.randint(0, 10),
    "totlen_bwd_pkts": random.randint(0, 10),

    "fwd_pkt_len_max": random.randint(0, 1500),
    "fwd_pkt_len_min": random.randint(0, 1500),
    "fwd_pkt_len_mean": round(random.uniform(0, 1500), 2),
    "fwd_pkt_len_std": round(random.uniform(0, 500), 2),

    "bwd_pkt_len_max": random.randint(0, 1500),
    "bwd_pkt_len_min": random.randint(0, 1500),
    "bwd_pkt_len_mean": round(random.uniform(0, 1500), 2),
    "bwd_pkt_len_std": round(random.uniform(0, 500), 2),

    "pkt_len_max": random.randint(0, 1500),
    "pkt_len_min": random.randint(0, 1500),
    "pkt_len_mean": round(random.uniform(0, 1500), 2),
    "pkt_len_std": round(random.uniform(0, 500), 2),
    "pkt_len_var": round(random.uniform(0, 5e5), 2),

    "fwd_header_len": random.randint(0, 500),
    "bwd_header_len": random.randint(0, 500),
    "fwd_seg_size_min": random.randint(0, 1500),
    "fwd_act_data_pkts": random.randint(0, 50),

    # IAT features
    "flow_iat_mean": round(random.uniform(0, 2000), 2),
    "flow_iat_max": random.randint(1, 5000),
    "flow_iat_min": random.randint(0, 100),
    "flow_iat_std": round(random.uniform(0, 2000), 2),

    "fwd_iat_tot": random.randint(0, 50000),
    "fwd_iat_max": random.randint(1, 5000),
    "fwd_iat_min": random.randint(0, 100),
    "fwd_iat_mean": round(random.uniform(0, 2000), 2),
    "fwd_iat_std": round(random.uniform(0, 2000), 2),

    "bwd_iat_tot": random.randint(0, 50000),
    "bwd_iat_max": random.randint(1, 5000),
    "bwd_iat_min": random.randint(0, 100),
    "bwd_iat_mean": round(random.uniform(0, 2000), 2),
    "bwd_iat_std": round(random.uniform(0, 2000), 2),

    # Flags
    "fwd_psh_flags": random.randint(0, 1),
    "bwd_psh_flags": random.randint(0, 1),
    "fwd_urg_flags": random.randint(0, 1),
    "bwd_urg_flags": random.randint(0, 1),
    "fin_flag_cnt": random.randint(0, 1),
    "syn_flag_cnt": random.randint(0, 1),
    "rst_flag_cnt": random.randint(0, 1),
    "psh_flag_cnt": random.randint(0, 1),
    "ack_flag_cnt": random.randint(0, 1),
    "urg_flag_cnt": random.randint(0, 1),
    "ece_flag_cnt": random.randint(0, 1),

    "down_up_ratio": random.randint(0, 10),
    "pkt_size_avg": round(random.uniform(40, 1000), 2),

    "init_fwd_win_byts": random.randint(0, 65535),
    "init_bwd_win_byts": random.randint(0, 65535),

    # Active/Idle
    "active_max": random.randint(0, 5000),
    "active_min": random.randint(0, 1000),
    "active_mean": round(random.uniform(0, 2000), 2),
    "active_std": round(random.uniform(0, 500), 2),

    "idle_max": random.randint(0, 5000),
    "idle_min": random.randint(0, 1000),
    "idle_mean": round(random.uniform(0, 2000), 2),
    "idle_std": round(random.uniform(0, 500), 2),

    # Avg byte/packet stats
    "fwd_byts_b_avg": round(random.uniform(0, 1500), 2),
    "fwd_pkts_b_avg": round(random.uniform(0, 100), 2),
    "bwd_byts_b_avg": round(random.uniform(0, 1500), 2),
    "bwd_pkts_b_avg": round(random.uniform(0, 100), 2),
    "fwd_blk_rate_avg": round(random.uniform(0, 100), 2),
    "bwd_blk_rate_avg": round(random.uniform(0, 100), 2),
    "fwd_seg_size_avg": round(random.uniform(0, 1500), 2),
    "bwd_seg_size_avg": round(random.uniform(0, 1500), 2),

    "cwe_flag_count": random.randint(0, 10),

    # Subflows
    "subflow_fwd_pkts": random.randint(1, 50),
    "subflow_bwd_pkts": random.randint(1, 50),
    "subflow_fwd_byts": random.randint(0, 10),
    "subflow_bwd_byts": random.randint(0, 10),
}
try:
    r = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=5)
    print("Status:", r.status_code)
    print("Body:", r.text)
except requests.RequestException as e:
    print("Request failed:", e, file=sys.stderr)
    sys.exit(1)
