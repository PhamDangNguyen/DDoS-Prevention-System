# NSL_KDD.py (ví dụ)
import json, sys, requests

URL = "http://127.0.0.1:8080/NSL-KDD"   # <-- dùng 127.0.0.1 hoặc localhost
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
PAYLOAD = {
  "duration": 0, "protocol_type": 1, "service": 45, "flag": 1,
  "src_bytes": 0, "dst_bytes": 0, "wrong_fragment": 0, "hot": 0,
  "logged_in": 0, "num_compromised": 0, "count": 136, "srv_count": 1,
  "serror_rate": 0, "srv_serror_rate": 0, "rerror_rate": 1
}

try:
    r = requests.post(URL, headers=HEADERS, json=PAYLOAD, timeout=5)
    print("Status:", r.status_code)
    print("Body:", r.text)
except requests.RequestException as e:
    print("Request failed:", e, file=sys.stderr)
    sys.exit(1)
