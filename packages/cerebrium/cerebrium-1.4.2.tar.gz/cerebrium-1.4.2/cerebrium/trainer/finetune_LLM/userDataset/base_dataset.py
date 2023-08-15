from .data_validator import Dataset_Validator


class FineTuningDataset:
    # TODO Docstrings
    def __init__(self, dataset_path, verbose: bool = False, **kwargs):
        """Base dataset class for fine-tuning using the Cerebrium package.
        Your dataset is loaded and run through a sanity check to ensure that it is ready for training.

        Args:
            dataset_path (str): path to the JSON/JSONL file on your system that contains your fine-tuning data.
            instruction_column (str, optional): Name of the input column in your dataset. Defaults to "prompt".
            label_column (str, optional): Name of the label column in your dataset. Defaults to "completion".
            context_column (str, optional): Name of the context column in your dataset . Defaults to "context".
            prompt_template (str): The template to be used for finetuning. Can be {"short", "long"} or a string to format. E.g f"###My Question\n{input}\n\n###Models Answer\n" which will be formatted with your input data.
            cutoff_len (int, optional): Maximum length to cut inputs to. Defaults to 512.
            train_val_ratio (float, optional): Ratio between train and validation data for splits. Defaults to 0.9.
            custom_schema (dict, optional): Custom jsonschema for validating your dataset. Defaults to None
            verbose (bool, optional): Verbose prints. Defaults to False
        """
        self.dataset_path = dataset_path

        # validator
        self.verbose = kwargs.get("verbose", False)

        self.prompt_template = kwargs.get("prompt_template", "")
        self.instruction_column = kwargs.get("instruction_column", "prompt")
        self.label_column = kwargs.get("label_column", "completion")
        self.context_column = kwargs.get("context_column", "context")
        self.cutoff_len = kwargs.get("cutoff_len", 512)
        self.train_val_ratio = kwargs.get("train_val_ratio", 0.9)
        self.verbose = verbose  # override with verbose from params

        self.custom_schema = kwargs.get("custom_schema", None)
        # validate file before training
        validator = Dataset_Validator(
            prompt_column=self.instruction_column,
            context_column=self.context_column,
            label_column=self.label_column,
            custom_schema=self.custom_schema,
            verbose=self.verbose,
        )

        assert validator(
            filename=self.dataset_path
        ), "Failed check. Please ensure your input dataset is valid json and that the column names you have provided match the data"

    def to_dict(self) -> dict:
        return self.__dict__
