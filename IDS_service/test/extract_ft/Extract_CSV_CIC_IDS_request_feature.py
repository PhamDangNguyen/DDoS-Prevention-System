#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import sniff
from cicflowmeter.flow_session import FlowSession

# --- CẤU HÌNH ---
OUTPUT_CSV = "flows.csv"
INTERFACE  = "Wi-Fi"     # hoặc "Wi-Fi", "Ethernet" trên Windows
# -----------------

# Khởi tạo FlowSession để ghi CSV trực tiếp
session = FlowSession(
    output_mode="csv",
    output=OUTPUT_CSV,
    verbose=False,
)

# Callback xử lý mỗi packet
def handle_packet(pkt):
    session.process(pkt)

print(f"🔍 Đang capture trên {INTERFACE}... (nhấn Ctrl+C để dừng)")

sniff(
    iface=INTERFACE,
    prn=handle_packet,
    filter="ip and (tcp or udp)",
    store=False
)


# Sau khi dừng -> flush toàn bộ flows ra CSV
session.flush_flows()
print(f"✅ Done! CSV saved to: {OUTPUT_CSV}")
