from abc import ABC, abstractmethod
from enum import Enum


class ModelType(Enum):
    XGBOOST_CLASSIFIER = "xgboost_classifier"
    XGBOOST_REGRESSOR = "xgboost_regressor"
    TORCH = "torch"
    SKLEARN = "sklearn"
    SKLEARN_CLASSIFIER = "sklearn_classifier"
    ONNX = "onnx"
    SKLEARN_PREPROCESSOR = "sklearn_preprocessor"
    PREBUILT = "prebuilt"
    SPACY = "spacy"
    HUGGINGFACE_PIPELINE = "hf_pipeline"


class BaseModel(ABC):
    def __init__(
        self,
        model,
    ):
        self.model = model

    @abstractmethod
    def predict(self, input_data) -> list:
        pass
