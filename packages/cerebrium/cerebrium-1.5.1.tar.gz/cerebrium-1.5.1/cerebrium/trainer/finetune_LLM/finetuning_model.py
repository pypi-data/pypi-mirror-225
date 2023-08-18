from typing import Union


class FineTuningModel:
    def __init__(
        self,
        hf_base_model_path: str,
        model_type: str = "AutoModelForCausalLM",
        lora_kwargs: Union[dict, None] = None,
        base_model_kwargs: Union[dict, None] = None,
    ):
        if lora_kwargs is None:
            lora_kwargs = {}
        if base_model_kwargs is None:
            base_model_kwargs = {}

        self.model_type = model_type
        try:
            import transformers
        except ImportError as e:
            raise ImportError(
                "Transformers not installed. Please install `transformers` with pip or conda to run this model type."
            ) from e
        assert hasattr(
            transformers, model_type
        ), f"Model type {model_type} not found in transformers library. Please check your spelling and try again."
        self.hf_base_model_path = hf_base_model_path
        self.lora_kwargs = lora_kwargs
        self.base_model_kwargs = base_model_kwargs
        self.init_kwargs()

    def init_kwargs(self):
        lora_defaults = {
            "r": 8,
            "lora_alpha": 32,
            "lora_dropout": 0.05,
            "target_modules": ["q_proj", "v_proj"],
            "bias": "none",
            "task_type": "CAUSAL_LM",
        }

        for k, v in lora_defaults.items():
            if k not in self.lora_kwargs:
                self.lora_kwargs[k] = v

        defaults = {
            "load_in_8bit": True,
            "device_map": "auto",
        }

        for k, v in defaults.items():
            if k not in self.base_model_kwargs:
                self.base_model_kwargs[k] = v

    def to_dict(self):
        return self.__dict__
