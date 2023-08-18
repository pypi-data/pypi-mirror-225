from typing import Dict, List, Union

from cerebrium.models.base import BaseModel, ModelType


class HFPipeline(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.model_type = ModelType.HUGGINGFACE_PIPELINE

    def predict(self, input_data: Union[Dict, List]) -> list:
        if isinstance(input_data, dict):
            data = input_data["data"]
            params = input_data.get("parameters", {})
        else:
            data = input_data
            params = {}
        return self.model(data, **params)
