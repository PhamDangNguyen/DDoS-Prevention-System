from src.services.abstract import IAnomalyService
import pickle
from src.services.dto import InputRequestNSLKDD, InputRequestCICIDS2017
from src.configs import APP_CONFIGS
import numpy as np
import joblib
from typing import Union
import pandas as pd
from src.services.blocks import ColumnOrderer

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
		elif data_name == "CIC-IDS2017":
			model_path = APP_CONFIGS["APP"]["MODEL"]["CIC-IDS2017"]["MODEL_PATH"]
			self.model = joblib.load(model_path)

	def preprocess(self, input_request: Union[InputRequestNSLKDD, InputRequestCICIDS2017]):
		if self.data_name == "NSL-KDD":
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
		elif self.data_name == "CIC-IDS2017":
			COL2FIELD = {
				"PSH Flag Count": "psh_flag_count",
				"min_seg_size_forward": "min_seg_size_forward",
				"Flow IAT Max": "flow_iat_max",
				"Flow IAT Min": "flow_iat_min",
				"ACK Flag Count": "ack_flag_count",
				"Destination Port": "destination_port",
				"Bwd Packet Length Mean": "bwd_packet_length_mean",
				"Bwd Packet Length Max": "bwd_packet_length_max",
				"Bwd Packet Length Min": "bwd_packet_length_min",
				"Init_Win_bytes_forward": "init_win_bytes_forward",
				"Fwd IAT Max": "fwd_iat_max",
				"Idle Mean": "idle_mean",
				"Idle Max": "idle_max",
				"Avg Bwd Segment Size": "avg_bwd_segment_size",
				"Bwd Packet Length Std": "bwd_packet_length_std",
				"Bwd IAT Mean": "bwd_iat_mean",
				"Fwd IAT Std": "fwd_iat_std",
				"Down/Up Ratio": "down_up_ratio",
				"Max Packet Length": "max_packet_length",
				"Average Packet Size": "average_packet_size",
				"Min Packet Length": "min_packet_length",
				"Packet Length Std": "packet_length_std",
				"Fwd Packets/s": "fwd_packets_s",
				"Packet Length Mean": "packet_length_mean",
				"Flow IAT Std": "flow_iat_std",
				"URG Flag Count": "urg_flag_count",
				"FIN Flag Count": "fin_flag_count",
				"Fwd Packet Length Min": "fwd_packet_length_min",
				"Subflow Fwd Packets": "subflow_fwd_packets",
				"Bwd IAT Max": "bwd_iat_max",
				"Packet Length Variance": "packet_length_variance",
				"Fwd IAT Mean": "fwd_iat_mean",
				"Flow Duration": "flow_duration",
				"Fwd IAT Total": "fwd_iat_total",
				"Bwd IAT Std": "bwd_iat_std",
				"Flow IAT Mean": "flow_iat_mean",
			}
			cols_dict = {col: getattr(input_request, field) for col, field in COL2FIELD.items()}
			return cols_dict
	def infer(self, input_request: Union[InputRequestNSLKDD, InputRequestCICIDS2017]):
		if self.data_name == "NSL-KDD":
			data_transformed = self.preprocess(input_request)
			pred = self.model.predict(data_transformed)
			pred = self.label_encoder.inverse_transform(pred)
			return pred[0]
		elif self.data_name == "CIC-IDS2017":
			def predict_one(pipe, point: dict) -> dict:
				df_one = pd.DataFrame([point]).select_dtypes(include=["number"])
				pred = pipe.predict(df_one)[0]
				out = {"prediction": str(pred), "probas": None}
				if hasattr(pipe.named_steps["model"], "predict_proba"):
					prob = pipe.predict_proba(df_one)[0]
					classes = pipe.named_steps["model"].classes_.tolist()
					out["probas"] = {cls: float(p) for cls, p in zip(classes, prob)}
				return out
			return predict_one(self.model, self.preprocess(input_request))




if __name__ == "__main__":
	# anomaly_service = AnomalyService("NSL-KDD")
	# input_request = InputRequestNSLKDD(
	# 	duration=0,
	# 	protocol_type=1,
	# 	service=45,
	# 	flag=1,
	# 	src_bytes=0,
	# 	dst_bytes=0,
	# 	wrong_fragment=0,
	# 	hot=0,
	# 	logged_in=0,
	# 	num_compromised=0,
	# 	count=136,
	# 	srv_count=1,
	# 	serror_rate=0,
	# 	srv_serror_rate=0,
	# 	rerror_rate=1
	# )
	# PAYLOAD = {
	# "duration": 0, "protocol_type": 1, "service": 45, "flag": 1,
	# "src_bytes": 0, "dst_bytes": 0, "wrong_fragment": 0, "hot": 0,
	# "logged_in": 0, "num_compromised": 0, "count": 136, "srv_count": 1,
	# "serror_rate": 0, "srv_serror_rate": 0, "rerror_rate": 1
	# }
	# print(anomaly_service.infer(InputRequestNSLKDD(**PAYLOAD)))
	
	anomaly_service = AnomalyService("CIC-IDS2017")
	COL2FIELD = {
		"PSH Flag Count": "psh_flag_count",
		"min_seg_size_forward": "min_seg_size_forward",
		"Flow IAT Max": "flow_iat_max",
		"Flow IAT Min": "flow_iat_min",
		"ACK Flag Count": "ack_flag_count",
		"Destination Port": "destination_port",
		"Bwd Packet Length Mean": "bwd_packet_length_mean",
		"Bwd Packet Length Max": "bwd_packet_length_max",
		"Bwd Packet Length Min": "bwd_packet_length_min",
		"Init_Win_bytes_forward": "init_win_bytes_forward",
		"Fwd IAT Max": "fwd_iat_max",
		"Idle Mean": "idle_mean",
		"Idle Max": "idle_max",
		"Avg Bwd Segment Size": "avg_bwd_segment_size",
		"Bwd Packet Length Std": "bwd_packet_length_std",
		"Bwd IAT Mean": "bwd_iat_mean",
		"Fwd IAT Std": "fwd_iat_std",
		"Down/Up Ratio": "down_up_ratio",
		"Max Packet Length": "max_packet_length",
		"Average Packet Size": "average_packet_size",
		"Min Packet Length": "min_packet_length",
		"Packet Length Std": "packet_length_std",
		"Fwd Packets/s": "fwd_packets_s",
		"Packet Length Mean": "packet_length_mean",
		"Flow IAT Std": "flow_iat_std",
		"URG Flag Count": "urg_flag_count",
		"FIN Flag Count": "fin_flag_count",
		"Fwd Packet Length Min": "fwd_packet_length_min",
		"Subflow Fwd Packets": "subflow_fwd_packets",
		"Bwd IAT Max": "bwd_iat_max",
		"Packet Length Variance": "packet_length_variance",
		"Fwd IAT Mean": "fwd_iat_mean",
		"Flow Duration": "flow_duration",
		"Fwd IAT Total": "fwd_iat_total",
		"Bwd IAT Std": "bwd_iat_std",
		"Flow IAT Mean": "flow_iat_mean",
	}
	input_request = InputRequestCICIDS2017(
		psh_flag_count=0,
		min_seg_size_forward=0,
		flow_iat_max=0,
		flow_iat_min=0,
		ack_flag_count=0,
		destination_port=0,
		bwd_packet_length_mean=0,
		bwd_packet_length_max=0,
		bwd_packet_length_min=0,
		init_win_bytes_forward=0,
		fwd_iat_max=0,
		idle_mean=0,
		idle_max=0,
		avg_bwd_segment_size=0,
		bwd_packet_length_std=0,
		bwd_iat_mean=0,
		fwd_iat_std=0,
		down_up_ratio=0,
		max_packet_length=0,
		average_packet_size=0,
		min_packet_length=0,
		packet_length_std=0,
		fwd_packets_s=0,
		packet_length_mean=0.0,
		flow_iat_std=0,
		urg_flag_count=0,
		fin_flag_count=0,
		fwd_packet_length_min=0,
		subflow_fwd_packets=0,
		bwd_iat_max=0,
		packet_length_variance=0,
		fwd_iat_mean=0,
		flow_duration=0,
		fwd_iat_total=0,
		bwd_iat_std=0,
		flow_iat_mean=0
	)

	print(anomaly_service.infer(input_request))
