from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional
from src.services.dto import InputRequest, Response
from src.services.anomaly import AnomalyService

router = APIRouter()

@router.post("/NSL-KDD")
def check_anomaly(input_request:InputRequest):
    try:
        anomalyService = AnomalyService(data_name="NSL-KDD")
        pred = anomalyService.infer(input_request)
        result = {
            "status_code": 200,
            "result": pred
        }
        return Response(**result)
    except Exception as e:
        return JSONResponse(status_code=400, content=str(e))
    