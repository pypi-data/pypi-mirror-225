from cerebrium.models.base import BaseModel, ModelType


class SKClassifierModel(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.model_type = ModelType.SKLEARN_CLASSIFIER

    def predict(self, input_data) -> list:
        return self.model.predict_proba(input_data)


class SKRegressorModel(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.model_type = ModelType.SKLEARN

    def predict(self, input_data) -> list:
        return self.model.predict(input_data)


class SKPreprocessorModel(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.model_type = ModelType.SKLEARN_PREPROCESSOR

    def predict(self, input_data) -> list:
        return self.model.transform(input_data)
