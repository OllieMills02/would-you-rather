from fastapi import Request

from train import WyrModelTrainer


class ModelManager:
    def __init__(self):
        self.models = {}
        self.is_loaded = False

    def load_models(self):
        # The actual loading logic
        self.models["would_you_rather"] = WyrModelTrainer()
        # You could also add a line to retrain here
        self.is_loaded = True

    def get_model(self):
        if not self.is_loaded:
            raise RuntimeError("Models are not loaded.")
        return self.models["would_you_rather"]


model_manager = ModelManager()


def get_model():
    return model_manager.get_model()