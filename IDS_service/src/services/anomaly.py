from src.services.abstract import IAnomalyService
import pickle
from src.services.dto import InputRequest
from src.configs import APP_CONFIGS
import numpy as np

class AnomalyService(IAnomalyService):
    def __init__(self,data_name):
        self.data_name = data_name
        self.model = None
        self.preprocessor = None
        self.label_encoder = None
        self.load_model(data_name)
    
    def load_model(self, data_name):
        if data_name == "NSL-KDD":
            with open(APP_CONFIGS["APP"]["MODEL"]["NSL-KDD"]["MODEL_PATH"], 'rb') as f:
                bundle = pickle.load(f)
                self.model = bundle["model"]
                self.preprocessor = bundle["preprocessor"]
                self.label_encoder = bundle["label_encoder"]

    def preprocess(self, input_request: InputRequest):
        FEATURE_ORDER = [
            "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
            "wrong_fragment", "hot", "logged_in", "num_compromised", "count", "srv_count",
            "serror_rate", "srv_serror_rate", "rerror_rate"
        ]
        data = [getattr(input_request, feature) for feature in FEATURE_ORDER]
        data = np.array(data).reshape(1, -1)
    
        # Apply scaler
        data_transformed = self.preprocessor.transform(data)
        return data_transformed
    
    def infer(self, input_request: InputRequest):
        data_transformed = self.preprocess(input_request)
        pred = self.model.predict(data_transformed)
        pred = self.label_encoder.inverse_transform(pred)
        return pred[0]