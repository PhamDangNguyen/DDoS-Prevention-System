import pickle
import argparse
import pandas as pd
import numpy as np

class AnomalyDetection:
    def __init__(self, save_path):
        self.save_path = save_path
        self.model = None
        self.preprocessor = None
        self.label_encoder = None
        self.load_model()
    
    def load_model(self):
        
        with open(self.save_path, 'rb') as f:
            bundle = pickle.load(f)
            self.model = bundle["model"]
            self.preprocessor = bundle["preprocessor"]
            self.label_encoder = bundle["label_encoder"]

    def preprocess(self, df_test):
        FEATURE_ORDER = [
            "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
            "wrong_fragment", "hot", "logged_in", "num_compromised", "count", "srv_count",
            "serror_rate", "srv_serror_rate", "rerror_rate"
        ]
        df_test = df_test[FEATURE_ORDER]
        df_test = self.preprocessor.transform(df_test) 
        y_pred = self.model.predict(df_test)
        class_pred = self.label_encoder.inverse_transform(y_pred)
    
        return class_pred
    
    def infer(self, test_path):
        df_test = pd.read_csv(test_path)
        data_transformed = self.preprocess(df_test)
        pred = self.model.predict(data_transformed)
        pred = self.label_encoder.inverse_transform(pred)
        return pred[0]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_path", type = str, required=True, help="Path to csv file contain test data")
    parser.add_argument("--save_path", type=str, required=True, help="Path to trained model")
    args = parser.parse_args()

    anomaly_detector = AnomalyDetection(save_path=args.save_path)
    anomaly_detector.infer(args.test_path)
    