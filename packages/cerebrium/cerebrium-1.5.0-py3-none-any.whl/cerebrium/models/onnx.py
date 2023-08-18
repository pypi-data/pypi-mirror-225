from cerebrium.models.base import BaseModel, ModelType


class OnnxModel(BaseModel):
    def __init__(self, model):
        super().__init__(model)
        self.output_names = [output.name for output in self.model.get_outputs()]
        self.model_type = ModelType.ONNX

    def predict(self, onnx_input: dict) -> list:
        res = self.model.run(self.output_names, onnx_input)
        return [result.tolist() for result in res]
