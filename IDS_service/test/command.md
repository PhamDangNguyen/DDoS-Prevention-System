curl -X 'POST' \
  'http://0.0.0.0:8080/NSL-KDD' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "duration": 0,
  "protocol_type": 1,
  "service": 45,
  "flag": 1,
  "src_bytes": 0,
  "dst_bytes": 0,
  "wrong_fragment": 0,
  "hot": 0,
  "logged_in": 0,
  "num_compromised": 0,
  "count": 136,
  "srv_count": 1,
  "serror_rate": 0,
  "srv_serror_rate": 0,
  "rerror_rate": 1
}'