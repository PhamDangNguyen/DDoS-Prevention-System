from abc import ABC

class IAnomalyService:
    def __init__(self) -> None:
        pass

    def load_model(self, model_path):
        pass

    def preprocess(self):
        pass

    def infer(self):
        pass