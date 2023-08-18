from cerebrium.models.base import BaseModel, ModelType


class TorchModel(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.model_type = ModelType.TORCH

    def predict(self, input_data) -> list:
        return self.model(input_data)
