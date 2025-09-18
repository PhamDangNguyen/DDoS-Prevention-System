from pydantic import BaseModel
from typing import Union, List

class InputRequest(BaseModel):
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

class Response(BaseModel):
    status_code: int = 200
    result: str = "normal"
    confidence: Union[float, int] = None