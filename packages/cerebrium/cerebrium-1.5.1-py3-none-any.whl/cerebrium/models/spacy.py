from cerebrium.models.base import BaseModel, ModelType


class SpacyModel(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.model_type = ModelType.SPACY

    def predict(self, input_data: str):
        return self.model(input_data)
