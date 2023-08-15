import os
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Union
from jsonschema import Draft202012Validator, validate


# class to perform validation
class Dataset_Validator:
    """
    Class to check JSON dataset and ensure the data is labeled for training.
    """

    def __init__(
        self,
        prompt_column: str = "prompt",
        context_column: str = "context",
        label_column: str = "completion",
        custom_schema: Union[dict, None] = None,
        verbose: bool = False,
        pd_json_kwargs: Union[dict, None] = None,
    ) -> None:
        """Init for dataset validator class

        Args:
            prompt_column (str, optional): Dataset prompt column name. Defaults to "prompt".
            context_column (str, optional): Dataset context column name. Defaults to "context".
            label_column (str, optional): Dataset label column name. Defaults to "completion".
            custom_schema (dict, optional): Your very own custom jsonschema to use instead. Defaults to None.
            verbose (bool, optional): Verbose or quiet. Defaults to False.
            pd_json_kwargs, (dict, optional): kwargs for pandas when loading dataset from JSON. Defaults to None.
        """
        self.verbose = verbose

        if pd_json_kwargs is None:
            pd_json_kwargs = {"lines": False, "orient": None}
        self.pd_json_kwargs = pd_json_kwargs

        # Init data validation object
        if not custom_schema:
            self.schema = {
                "type": "object",
                "properties": {
                    prompt_column: {"type": "string"},
                    label_column: {"type": "string"},
                    "source": {"type": ["string", "null"]},
                },
                "required": [prompt_column, label_column],
                "additionalProperties": False,
            }
            if context_column:  # if context column is provided, add it to the schema
                self.schema["properties"][context_column] = {"type": "string"}
        else:
            self.schema = custom_schema

        Draft202012Validator.check_schema(self.schema)

    def __call__(self, filename: Path, return_dataframe: bool = False):
        # Check if the file exists
        assert os.path.exists(filename), f"The file '{filename}' could not be found"
        if self.verbose:
            print("Found dataset file.")

        # Check the json is valid for training.
        df_data = self.load_json_file(filename=filename)
        result = self.is_valid_for_training(df=df_data)

        return result

    def is_valid_for_training(self, df) -> bool:
        if self.verbose:
            print(f"Found {len(df)} data entries")
        for _, row in df.iterrows():
            row = row.dropna()
            pt = row.to_dict()
            result = validate(instance=pt, schema=self.schema)
            if result is not None:
                if self.verbose:
                    print(f"Found invalid entry: {pt}")
                return False

        if self.verbose:
            print("All entries in the dataset passed validation ✅")
        return True

    def load_json_file(self, filename):
        try:
            import pandas as pd
        except ImportError as error:
            print(
                "Pandas is required for validating JSON datasets for the cerebrium trainer. Please install 'pandas' with pip or conda."
            )
            raise error

        extension = os.path.splitext(filename)[1]

        if extension in {".json", ".jsonl"}:
            if extension == ".jsonl":
                self.pd_json_kwargs["orient"] = "records"
                self.pd_json_kwargs["lines"] = True
            if self.verbose:
                print(f"Reading in JSON file at {filename}")
            df = pd.read_json(filename, **self.pd_json_kwargs)
        else:
            try:
                df = pd.read_json(filename, **self.pd_json_kwargs)
            except JSONDecodeError as error:
                print("Cannot decode your file. Ensure it is valid json or jsonl")
                raise error

        return df
