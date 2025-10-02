from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from typing import Optional
from src.services.dto import InputRequestNSLKDD, Response, InputRequestCICIDS2017, SelectedFeaturetCICIDS2017
from src.services.anomaly import AnomalyService
from src.services.blocks import ColumnOrderer

router = APIRouter()

@router.post("/NSL-KDD")
def check_anomaly(input_request:InputRequestNSLKDD):
    try:
        anomalyService = AnomalyService(data_name="NSL-KDD")
        pred, pred_probs = anomalyService.infer(input_request)
        result = {
            "status_code": 200,
            "result": pred,
            "confidence": pred_probs
        }
        return Response(**result)
    except Exception as e:
        return JSONResponse(status_code=400, content=str(e))

@router.post("/CIC-IDS2017")
def check_anomaly(input_request:InputRequestCICIDS2017):
    try:
        anomalyService = AnomalyService(data_name="CIC-IDS2017")
        # Create a dictionary of ModelA fields
        input_request_dict = input_request.dict()
        # Get only the fields that are also in ModelB
        select_feat_dict = {key: input_request_dict[key] for key in input_request_dict if key in SelectedFeaturetCICIDS2017.__annotations__}
        # Create ModelB instance using the filtered fields
        model_b_instance = SelectedFeaturetCICIDS2017(**select_feat_dict)
        pred = anomalyService.infer(model_b_instance)
        result = {
            "status_code": 200,
            "result": pred.get("prediction", "normal"),
            "confidence": pred.get("probas", None)
        }
        return Response(**result)
    except Exception as e:
        return JSONResponse(status_code=400, content=str(e))