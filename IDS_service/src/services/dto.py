from pydantic import BaseModel
from typing import Union, List

class InputRequestNSLKDD(BaseModel):
    duration: Union[int, float] = None
    protocol_type: Union[int, float] = None
    service: int = None
    flag: int  = None
    src_bytes: int = None
    dst_bytes: int = None
    wrong_fragment: int = None
    hot: int = None
    logged_in: int = None
    num_compromised: int = None
    count: int = None
    srv_count: int = None
    serror_rate: Union[int, float]
    srv_serror_rate: Union[int, float]
    rerror_rate: Union[int, float]

class InputRequestCICIDS2017(BaseModel):
    psh_flag_count: int
    min_seg_size_forward: int
    flow_iat_max: int
    flow_iat_min: int
    ack_flag_count: int
    destination_port: int
    bwd_packet_length_mean: float
    bwd_packet_length_max: int
    bwd_packet_length_min: int
    init_win_bytes_forward: int
    fwd_iat_max: int
    idle_mean: float
    idle_max: int
    avg_bwd_segment_size: float
    bwd_packet_length_std: float
    bwd_iat_mean: float
    fwd_iat_std: float
    down_up_ratio: int
    max_packet_length: int
    average_packet_size: float
    min_packet_length: int
    packet_length_std: float
    fwd_packets_s: float
    packet_length_mean: float
    flow_iat_std: float
    urg_flag_count: int
    fin_flag_count: int
    fwd_packet_length_min: int
    subflow_fwd_packets: int
    bwd_iat_max: int
    packet_length_variance: float
    fwd_iat_mean: float
    flow_duration: int
    fwd_iat_total: int
    bwd_iat_std: float
    flow_iat_mean: float

class Response(BaseModel):
    status_code: int = 200
    result: str = "normal"
    confidence: Union[float, int, dict, str] = None