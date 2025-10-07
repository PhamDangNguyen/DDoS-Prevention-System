#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.utils import PcapReader
from cicflowmeter.flow_session import FlowSession

# --- ĐỔI 2 DÒNG NÀY THEO Ý BẠN ---
INPUT_PCAP  = r"C:\temp\scapy_capture.pcap"
OUTPUT_CSV  = r"output.csv"
# ----------------------------------

# Khởi tạo FlowSession để xuất CSV
session = FlowSession(
    output_mode="csv",
    output=OUTPUT_CSV,
    fields=None,     # hoặc "flow_id,src_ip,src_port,..."
    verbose=False,
)

# Đọc từng packet từ file PCAP và xử lý
count = 0
with PcapReader(INPUT_PCAP) as reader:
    for pkt in reader:
        session.process(pkt)
        count += 1

# Xả toàn bộ flow còn lại ra CSV
session.flush_flows()
print(f"✅ Done. Packets read: {count}\n➡️ CSV: {OUTPUT_CSV}")
