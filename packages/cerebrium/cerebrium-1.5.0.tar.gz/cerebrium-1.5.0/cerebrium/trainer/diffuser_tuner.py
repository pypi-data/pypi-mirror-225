import os
import json
import yaml
from cerebrium import __version__
from pathlib import Path
import sys
import tempfile
import zipfile
import requests
import warnings
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from prodict import Prodict

from cerebrium.requests import _cerebrium_request

# Required libraries:
# - xformers
# - datasets
# - diffusers
# - torch
# - bitsandbytes (8bit training and 8bit adam)


class DiffuserTuner:
    def __init__(
        self, name: str, config_path: str = None, config: dict = {}, log_level="INFO"
    ):
        self.training_type = "diffuser"
        self.name = name

        assert config_path or config, "Please provide a config file or config dict."
        # load in the config yaml
        if config_path:
            with open(config_path, "r") as f:
                if log_level.upper() == "DEBUG":
                    print(f"Loading config from {config_path}")
                yaml_config = yaml.safe_load(f)
                if log_level.upper() == "DEBUG":
                    print(f"Read in config and found {len(yaml_config)} keys.")
                if config:
                    yaml_config.update(config)
                config = yaml_config

        # overwrite the config with the user provided args
        config.update(
            {"name": name, "log_level": log_level, "training_type": self.training_type}
        )

        # Required args
        required_args = [
            "hf_model_path",  # Path to huggingface model
            "train_prompt",
            "train_image_dir",
        ]
        for arg in required_args:
            if arg not in config:
                raise ValueError(f"Config file must contain: {arg}.")

        # check the diffusers library has the model
        # assert self.model_name in ####List of supported models?####, f"Model {self.model_name} is not supported at present. Please contact the team to enable support for this model."

        # Check the dataset
        train_image_dir = config.get("train_image_dir")
        prior_class_image_dir = config.get("prior_class_image_dir", "")
        self.check_dataset(
            train_image_dir=train_image_dir, prior_class_image_dir=prior_class_image_dir
        )

        prior_class_prompt = config.get("prior_class_prompt", "")
        if bool(prior_class_prompt or prior_class_image_dir):
            config["with_prior_preservation"] = True
            assert (
                prior_class_prompt is not None
            ), "Please provide a class prompt with your prior_class_image_dir if you would like to use prior class images in training."
            print("🧱 Using prior class images in training.")
        else:
            config["with_prior_preservation"] = False

        # Set the logging log_level
        config["log_level"] = (
            log_level if log_level in ["", None] else config.get("log_level", "INFO")
        )
        self.log_level = config["log_level"]

        # Set the training args
        config["training_args"] = self.getTrainingArgs(config.get("training_args", {}))
        self.config = Prodict.from_dict(config)  # save the config to the object

    def check_dataset(self, train_image_dir: str, prior_class_image_dir: str):
        """Check the dataset path is valid and contains images for training."""
        if not Path(train_image_dir).exists():
            raise ValueError("Images root doesn't exists.")

        instance_images_path = []
        for p in list(Path(train_image_dir).iterdir()):
            if p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                instance_images_path.append(p)
        num_instance_images = len(instance_images_path)

        if num_instance_images == 0:
            raise ValueError("No images found in the training directory.")

        print(f"Found {num_instance_images} images in the training directory.")

        if prior_class_image_dir not in [None, ""]:
            if not Path(prior_class_image_dir).exists():
                raise ValueError("Class images root doesn't exists.")

            # Check there are images in the directory
            class_images_list = []
            for p in list(Path(prior_class_image_dir).iterdir()):
                if p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    class_images_list.append(p)
            num_class_images = len(class_images_list)

            # print info about number of images
            if num_class_images == 0:
                warnings.warn("No images found in the class directory.")
            else:
                print(f"Found {num_class_images} images in the class directory.")

        return True

    def getTrainingArgs(self, user_training_args) -> dict:
        """Create training args using combo of user_args and cerebrium defaults.
        Preference user training args and set defaults if not provided"""
        user_training_args = {
            "gradient_accumulation_steps": user_training_args.get(
                "gradient_accumulation_steps", 1
            ),
            "learning_rate": user_training_args.get("learning_rate", 5e-4),
            "lr_schedule": user_training_args.get("lr_schedule", "constant"),
            "max_train_steps": user_training_args.get("max_train_steps", ""),
            "num_train_epochs": user_training_args.get("num_train_epochs", 30),
            "per_device_train_batch_size": user_training_args.get(
                "per_device_train_batch_size", 1
            ),
            "train_batch_size": user_training_args.get("train_batch_size", 2),
            "train_in_8bit": user_training_args.get("train_in_8bit", True),
            "train_val_split": user_training_args.get("train_val_split", 0.8),
            "scale_lr": user_training_args.get("scale_lr", False),
            "warmup_steps": user_training_args.get("warmup_steps", 0),
            "use_xformers": user_training_args.get("use_xformers", True),
            "use_8bit_adam": user_training_args.get("use_8bit_adam", True),
            # "report_to": user_training_args.get("report_to", "wandb"), # For integration with wandb. Needs an API key and wandb project.
        }

        if self.log_level.upper() == "DEBUG":
            print("Set the training args to:")
            print(json.dumps(user_training_args, indent=4))

        return user_training_args

    def create_local_dataset(self, zip: zipfile.ZipFile = None):
        """Create a dataset from the images in the training directory."""
        # Check there are images in the directory
        assert (
            self.config.train_image_dir
        ), "Please provide a directory of images to train on."
        assert Path(
            self.config.train_image_dir
        ).exists(), "Training image directory doesn't exist."

        instance_images_list = []
        for p in list(Path(self.config.train_image_dir).iterdir()):
            if p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                instance_images_list.append(p)
        self.dataset_info = {
            "num_images": len(instance_images_list),
            "image_names": [
                str(img.relative_to(self.config.train_image_dir))
                for img in instance_images_list
            ],
        }

        if self.config.with_prior_preservation and self.config.prior_class_image_dir:
            assert Path(
                self.config.prior_class_image_dir
            ).exists(), "Please provide a directory of prior class images to train on."
            # append the class images to the dataset info
            class_images_list = []
            for p in list(Path(self.config.prior_class_image_dir).iterdir()):
                if p.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    class_images_list.append(p)

            self.dataset_info["class_image_names"] = [
                str(img.relative_to(self.config.prior_class_image_dir))
                for img in class_images_list
            ]

        if self.log_level.upper() == "DEBUG":
            print("Dataset info:")
            print(json.dumps(self.dataset_info, indent=4))

        # return a zipped dataset of images in the required format if supplied with a directory
        assert zip is not None, "Please provide a zip file to write the dataset to."

        # Write out the dataset info to a json file in the zip
        with zip.open("dataset.json", "w") as f:
            dataset_info_json = json.dumps(self.dataset_info, indent=2)
            # convertins string to bytes
            dataset_info_json = dataset_info_json.encode("utf-8")
            f.write(dataset_info_json)

        wrote = 0
        for img in tqdm(instance_images_list):
            if img.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                zip.write(
                    img,
                    arcname=os.path.join(
                        "dataset",
                        "trainingData",
                        img.relative_to(self.config.train_image_dir),
                    ),
                )
                wrote += 1
        if self.log_level.upper() == "DEBUG":
            print(f"Wrote {wrote} training images to the dataset zip file.")

        if (
            self.config.with_prior_preservation
            and self.config.prior_class_image_dir
            and Path(self.config.prior_class_image_dir).exists()
        ):
            for img in tqdm(class_images_list):
                if img.suffix.lower() in [".jpg", ".jpeg", ".png"]:
                    zip.write(
                        img,
                        arcname=os.path.join(
                            "dataset",
                            "classData",
                            img.relative_to(self.config.prior_class_image_dir),
                        ),
                    )
                    wrote += 1
            if self.log_level.upper() == "DEBUG":
                print(f"Wrote {wrote} prior class images to the dataset zip file.")

    def create_yaml_config(self, config_path):
        """Dump to yaml and write to the given file name."""
        safe_config = self.config.to_dict()
        for k, v in safe_config.items():
            if isinstance(v, Prodict):
                safe_config[k] = v.to_dict()

        with open(config_path, "w") as f:
            yaml.safe_dump(safe_config, f, sort_keys=False, version=(1, 2))

        if self.log_level.upper() == "DEBUG":
            print(f"Created config file at {config_path}!")

    def _zip_for_upload(self, zip_path, temp_dir=None):
        """Create a zip file containing the config files and upload them."""
        dir_name = os.path.dirname(zip_path)
        temp_dir = temp_dir if temp_dir else dir_name
        os.makedirs(dir_name, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w") as zip:
            config_path = os.path.join(temp_dir, f"{self.name}_finetune_config.yaml")
            self.create_yaml_config(config_path)
            zip.write(config_path, arcname="finetune_config.yaml")
            self.create_local_dataset(zip)

        if self.log_level.upper() == "DEBUG":
            print(f"Created zip file at {zip_path} and ready for upload!")

    def _upload(
        self,
        api_key,
        init_debug=False,
        pre_init_debug=False,
        log_level="INFO",
        hardware="AMPERE_A6000",
        cpu=2,
        memory=16.0,
    ):
        """Upload the config files to cerebrium for training."""
        dataset_hash = "DATASET_FILE_DOESNT_EXIST"
        # Calc MD5 hash of user's dataset
        assert os.path.exists(
            self.config.train_image_dir
        ), "Dataset file cannot be found. Please check the path you have entered!"

        # need some clever way to check if the contents of the folder have changed. If yes, reupload the dataset.
        # with open(self.config.train_image_dir, "rb") as f:
        #     dataset_hash = hashlib.md5(f.read()).hexdigest()

        # Hit the deploy endpoint to get the upload URL
        upload_url_response = _cerebrium_request(
            method="train",
            http_method="POST",
            api_key=api_key,
            payload={
                "name": self.name,
                "hf_model_path": self.config.hf_model_path,
                "hardware": hardware,
                "init_debug": init_debug,
                "pre_init_debug": pre_init_debug,
                "log_level": log_level,
                "cerebrium_version": __version__,
                "cpu": cpu,
                "memory": memory,
                # "dataset_hash": dataset_hash,
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
            zip_path = os.path.join(temp_dir, f"{self.name}.zip")
            self._zip_for_upload(zip_path, temp_dir=temp_dir)

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
                        "❌ API request failed with status code:",
                        upload_response.status_code,
                    )
                    print("Error uploading to Cerebrium:", upload_response.text)
                    raise Exception("Error uploading to Cerebrium")
                else:
                    print(f"✅ Resources uploaded successfully for {job_id}")
            print(
                f"You can query the training status with `cerebrium get-training-jobs --api-key {api_key}` \n",
                f"Your training logs can be found at `cerebrium get-training-logs {job_id} --api-key {api_key}` ",
            )

    def __iter__(self):
        yield from self.__dict__.items()

    def __str__(self):
        return json.dumps(dict(self), ensure_ascii=False)

    def __repr__(self):
        return self.__str__()
