import hashlib
import os
import sys
import tempfile
import yaml
import zipfile
from copy import copy
from typing import Optional
import requests
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from cerebrium import __version__
from cerebrium.requests import _cerebrium_request
from cerebrium.trainer.finetune_LLM.finetuning_model import FineTuningModel
from cerebrium.trainer.finetune_LLM.userDataset.base_dataset import FineTuningDataset


class FineTuner:
    def __init__(
        self,
        name: str,
        config: dict = {},
        config_yaml_path: Optional[str] = None,
        log_level: str = "INFO",
    ):
        """An object for finetuning transformers on Cerebrium to improve the perfromance of Large Language Models towards your task."""
        # check either config or config_yaml_path is provided
        assert (
            config or config_yaml_path
        ), "Either config or config_yaml_path must be provided."
        # load config
        if config_yaml_path:
            with open(config_yaml_path, "r") as f:
                self.config = yaml.safe_load(f).update(config)
        else:
            self.config = config

        self.config["training_type"] = "transformer"
        self.config["name"] = name

        # override with log_level from params
        self.config["log_level"] = log_level or self.config["log_level"]

        # backup for user to see what they sent
        self.config["user_base_model_kwargs"] = copy(self.config["base_model_args"])
        self.config["user_peft_kwargs"] = copy(self.config["peft_lora_args"])

        # will set to our defaults. Easier for beginners.
        # Calling here so that a user can access the defaults and check them before training.

        if self.config["log_level"].upper() == "DEBUG":
            print("Training args set to:")
            args = self.get_training_arguments(self.config["training_args"])
            print(args.to_json_string())

        self.config["finetuning_model"] = FineTuningModel(
            hf_base_model_path=self.config["hf_model_path"],
            model_type=self.config["model_type"],
            base_model_kwargs=self.config["base_model_args"],
            lora_kwargs=self.config["peft_lora_args"],
        )

        self.config["dataset"] = FineTuningDataset(
            dataset_path=self.config["dataset_path"],
            verbose=self.config["log_level"],
            **self.config["dataset_args"],
        )

    def get_training_arguments(self, training_kwargs: dict = {}):
        """A utility function to create training arguments for user inspection.
        A set of default training arguments is used if none are provided

        Args:
            logging_steps (int, optional): Steps between logging. Defaults to 10.
            per_device_batch_size (int, optional): Batch size. Defaults to 15.
            warmup_steps (int, optional): Warmup before beginning training. Defaults to 50.
            micro_batch_size (int, optional): Defaults to 4.
            num_epochs (int, optional): Number of epochs to train for. Defaults to 3.
            learning_rate (float, optional): Initial learning rate. Defaults to 3e-4.
            group_by_length (bool, optional): Defaults to False.


        Returns:
            TrainingArguments: _description_
        """
        try:
            from transformers import (
                TrainingArguments,
            )
        except ImportError as e:
            raise ImportError(
                "Transformers not installed. Please install `transformers` with pip or conda to run this model type."
            ) from e
        defaults = {
            "logging_steps": 10,
            "per_device_train_batch_size": 15,
            "per_device_eval_batch_size": 15,
            "warmup_steps": 0,
            "gradient_accumulation_steps": 4,
            "num_train_epochs": 3,
            "learning_rate": 1e-4,
            "group_by_length": False,
            "output_dir": "./",
        }

        for k, v in defaults.items():
            if k not in training_kwargs:
                training_kwargs[k] = v

        return TrainingArguments(
            **training_kwargs,
        )

    def create_yaml_config(self, filename="finetune.yaml"):
        # Quick json serialiser. Dumps all the variables as a config
        config_dict = self.config.copy()
        config_dict["finetuning_model"] = config_dict["finetuning_model"].to_dict()
        config_dict["dataset"] = config_dict["dataset"].to_dict()

        with open(filename, "w") as f:
            # json.dump(config_dict, fp=f, indent=2, sort_keys=True)
            yaml.dump(config_dict, f, sort_keys=False, version=(1, 2))

    def _upload(
        self,
        api_key,
        init_debug=False,
        pre_init_debug=False,
        log_level="INFO",
        hardware="AMPERE_A6000",
        cpu=2,
        memory=16.0
    ):  # sourcery skip: extract-method
        dataset_hash = "DATASET_FILE_DOESNT_EXIST"

        # Calc MD5 hash of user's dataset
        assert os.path.exists(
            self.config["dataset_path"]
        ), "Dataset file cannot be found. Please check the path you have entered!"
        with open(self.config["dataset_path"], "rb") as f:
            dataset_hash = hashlib.md5(f.read()).hexdigest()
        # Hit the deploy endpoint to get the upload URL
        upload_url_response = _cerebrium_request(
            method="train",
            http_method="POST",
            api_key=api_key,
            payload={
                "name": self.config["name"],
                "hf_model_path": self.config["hf_model_path"],
                "hardware": hardware,
                "init_debug": init_debug,
                "pre_init_debug": pre_init_debug,
                "log_level": log_level,
                "cerebrium_version": __version__,
                "dataset_hash": dataset_hash,
                "cpu": cpu,
                "memory": memory
            },
        )
        if upload_url_response["status_code"] != 200 or (
            upload_url_response["data"].get("uploadUrl", None) is None
        ):
            print(
                "❌ API request failed with status code:",
                upload_url_response["status_code"],
            )
            print("Error getting upload URL:", upload_url_response["data"]["message"])
            sys.exit(1)
        upload_url = upload_url_response["data"]["uploadUrl"]
        job_id = upload_url_response["data"]["jobId"]

        print(f"⚙️ Job ID: {job_id}")
        # Zip all files in the current directory and upload to S3
        print("📦 Zipping files...")
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, f"{self.config['name']}.zip")
            dir_name = os.path.dirname(zip_path)
            os.makedirs(dir_name, exist_ok=True)
            # Create a zip file containing the config files and upload them.
            with zipfile.ZipFile(
                os.path.join(temp_dir, f"{self.config['name']}.zip"), "w"
            ) as zip:
                config_file = os.path.join(
                    temp_dir, f"{self.config['name']}_finetune_config.yaml"
                )
                self.create_yaml_config(filename=config_file)
                zip.write(config_file, arcname="finetune_config.yaml")
                zip.write(self.config["dataset_path"], arcname="dataset.json")

            print("⬆️  Uploading to Cerebrium...")
            with open(zip_path, "rb") as f:
                headers = {
                    "Content-Type": "application/zip",
                }
                with tqdm(
                    total=os.path.getsize(zip_path),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:  # type: ignore
                    wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                    upload_response = requests.put(
                        upload_url,
                        headers=headers,
                        data=wrapped_f,  # type: ignore
                        timeout=60,
                        stream=True,
                    )
                if upload_response.status_code != 200:
                    print(
                        "API request failed with status code:",
                        upload_response.status_code,
                    )
                    print("❌ Error uploading to Cerebrium:", upload_response.text)
                    raise Exception("Error uploading to Cerebrium")
                else:
                    print(f"✅ Resources uploaded successfully for {job_id}")
            print(
                f"You can query the training status with `cerebrium get-training-jobs --api-key {api_key}` \n",
                f"Your training logs can be found at `cerebrium get-training-logs {job_id} --api-key {api_key}` ",
            )
