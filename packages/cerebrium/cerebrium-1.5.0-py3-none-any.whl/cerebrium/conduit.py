import enum
import json
import os
import re
import tempfile
import zipfile
import requests
from copy import deepcopy
from inspect import getsource, signature
from types import FunctionType
from typing import Any, Dict, Literal, Union
from typing_extensions import Self
from cloudpickle import load as pickle_load
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from cerebrium import __version__
from cerebrium.flow import CerebriumFlow, _check_flow_type, _flow_string
from cerebrium.logging.base import LoggingPlatform
from cerebrium.models.base import ModelType
from cerebrium.requests import _cerebrium_request, _poll_deployment_status

from cerebrium.datatypes import PythonVersion, Hardware

REGEX_NAME_PATTERN = "^[a-z0-9-]*$"
API_KEY = None


def _set_api_key(api_key):
    global API_KEY
    API_KEY = api_key


class Conduit:
    """
    The Conduit class encompasses the logic required to create a computational graph from a given model flow, as well as the logic required to run the graph on a given input.

    Args:
        name (str): The name to deploy the flow under.
        api_key (str): The API key for the Cerebrium account. If not provided, the API key will be read from the CEREBRIUM_API_KEY environment variable.
        flow (CerebriumFlow): The flow to deploy. This is a list of ModelType, model path and postprocessor tuples, as such:
            [(model_type.TORCH, "model.pt", postprocess_f)]
        hardware (Hardware): The hardware to deploy the model on.
        cpu (int): The number of CPU cores to allocate to the model. Defaults to 2.
        memory (int): The amount of memory to allocate to the model, in GB. Defaults to 14.5GB.
        from_json (str): The path to a JSON file containing the Conduit configuration.
        requirements_file (str): The path to a requirements.txt file containing the dependencies for the Conduit.
        min_replicas (int): The minimum number of replicas to deploy. Defaults to 0.
        max_replicas (int): The maximum number of replicas to deploy. Defaults to 2. This is plan dependent. Please contact Cerebrium for more information.
    """

    def __init__(
        self,
        name: str = "",
        api_key: str = "",
        flow: CerebriumFlow = [],
        hardware: Union[Hardware, None] = None,
        cpu: Union[int, None] = None,
        memory: Union[int, None] = None,
        python_version: Union[PythonVersion, None] = None,
        from_json: str = "",
        requirements_file: str = "",
        min_replicas: Union[int, None] = None,
        max_replicas: Union[int, None] = None,
    ):
        if not from_json:
            self.api_key = api_key or os.environ.get("CEREBRIUM_API_KEY", "")
            assert name != "" and self.api_key != ""
            # Check that the flow name is valid
            if len(name) > 20:
                raise ValueError("Conduit name must be less than 20 characters")
            if not bool(re.match(REGEX_NAME_PATTERN, name)):
                raise ValueError(
                    "Conduit name can only contain lowercase alphanumeric characters and hyphens"
                )
            self.name = name
            if flow is not None:
                self.flow: CerebriumFlow = _check_flow_type(flow)
            self.logger_configs = {}
            self._processors = None
            self.min_replicas = min_replicas
            self.max_replicas = max_replicas
            self.requirements_file = requirements_file
            self.cpu = cpu
            self.memory = memory
        else:
            with open(from_json, "r") as f:
                config = json.load(f)
                self.name = config["name"]
                self.api_key = config["api_key"]
                self.flow: CerebriumFlow = config["flow"]
                self.logger_configs = config["logger_configs"]
                self._processors = config["processors"]
                self.requirements_file = config.get("requirements_file")
                self.min_replicas = config.get("min_replicas")
                self.max_replicas = config.get("max_replicas")
                self.hardware = (
                    Hardware(config["hardware"]) if config.get("hardware") else None
                )
                self.cpu = config.get("cpu")
                self.memory = config.get("memory")
                self.python_version = (
                    PythonVersion(config["python_version"])
                    if config.get("python_version")
                    else None
                )
                # Set correct ModelTypes in flow
                for i, (model_type, model_initialization, processors) in enumerate(  # type: ignore
                    self.flow
                ):
                    self.flow[i] = (
                        ModelType(model_type),
                        model_initialization,
                        processors,
                    )
        _set_api_key(self.api_key)
        self.graph = []
        self.ready = False
        self.loggers = {}
        self.hardware = hardware or self._determine_hardware()
        self.python_version = python_version or PythonVersion.PYTHON_3_10

        if self.requirements_file:
            assert os.path.exists(
                self.requirements_file
            ), f"Requirements file {self.requirements_file} does not exist"
            assert os.path.isfile(
                self.requirements_file
            ), f"Requirements file {self.requirements_file} is not a file"
            assert self.requirements_file.endswith(
                ".txt"
            ), f"Requirements file {self.requirements_file} is not a .txt file"
            ## Calc MD5 hash of ./requirements.txt
            # if os.path.exists("./requirements.txt"):
            #     with open("./requirements.txt", "rb") as f:
            #         self.requirements_hash = hashlib.md5(f.read()).hexdigest()

        try:
            from torch.cuda import is_available

            self.device = (
                "cuda" if self.hardware != Hardware.CPU and is_available() else "cpu"
            )
        except ImportError:
            self.device = "cpu"
        self.contains_torch_model = False

    def _determine_hardware(self):
        # Set the default hardware to GPU if the flow contains a Torch, ONNX or HuggingFace model
        if any(
            model_type
            in [ModelType.TORCH, ModelType.ONNX, ModelType.HUGGINGFACE_PIPELINE]
            for model_type, _, _ in self.flow
        ):
            return Hardware.AMPERE_A5000
        else:
            return Hardware.CPU

    def load(self, directory: str = "/cache/", direct_from_flow: bool = False):
        """
        Load the Conduit components from the stored Model Flow into the computation graph.

        Args:
            directory (str): The directory to load the Conduit components from.
        """
        if self.flow == []:
            raise ValueError("Conduit is empty. Please add models to the Conduit flow.")
        if not self.ready:
            for model_type, model_initialization, _ in self.flow:  # type: ignore
                # run correct path
                if direct_from_flow:
                    model_initialization: str = os.path.abspath(model_initialization)
                elif model_type not in [
                    ModelType.PREBUILT,
                    ModelType.HUGGINGFACE_PIPELINE,
                ]:
                    model_initialization: str = (
                        directory + model_initialization.split("/")[-1]
                    )
                # Torch
                if model_type == ModelType.TORCH:
                    from cerebrium.models.torch import TorchModel

                    try:
                        from torch.nn import Module as TorchModule
                        from torch.jit import load as torchscript_load
                    except ImportError as e:
                        raise ImportError(
                            "PyTorch not installed. Please install `torch` with pip or conda to run this model type."
                        ) from e
                    self.contains_torch_model = True

                    if model_initialization.endswith(".pt"):
                        torch_model: TorchModule = torchscript_load(
                            model_initialization
                        )
                    else:
                        with open(model_initialization, "rb") as f:
                            torch_model: TorchModule = pickle_load(f)
                    torch_model.to(self.device)
                    self.graph.append(TorchModel(torch_model))

                # ONNX
                elif model_type == ModelType.ONNX:
                    from cerebrium.models.onnx import OnnxModel

                    try:
                        from onnxruntime import InferenceSession
                    except ImportError as e:
                        raise ImportError(
                            "ONNX not installed. Please install `onnxruntime` with pip or conda to run this model type."
                        ) from e

                    providers = (
                        ["CUDAExecutionProvider", "CPUExecutionProvider"]
                        if self.device == "cuda"
                        else ["CPUExecutionProvider"]
                    )
                    onnx_model = InferenceSession(
                        model_initialization,
                        providers=providers,
                    )
                    self.graph.append(OnnxModel(onnx_model))

                # Spacy
                elif model_type == ModelType.SPACY:
                    from cerebrium.models.spacy import SpacyModel
                    from spacy import load as spacy_load

                    try:
                        from spacy import load as spacy_load
                    except ImportError as e:
                        raise ImportError(
                            "SpaCy not installed. Please install `spacy` with pip or conda to run this model type."
                        ) from e

                    spacy_model = spacy_load(model_initialization)
                    self.graph.append(SpacyModel(spacy_model))

                # XGBoost
                elif model_type == ModelType.XGBOOST_CLASSIFIER:
                    from cerebrium.models.sklearn import SKClassifierModel

                    try:
                        from xgboost import XGBClassifier
                    except ImportError as e:
                        raise ImportError(
                            "XGBoost not installed. Please install `xgboost` with pip or conda to run this model type."
                        ) from e

                    if model_initialization.endswith("json"):
                        xgb_classifier = XGBClassifier()
                        xgb_classifier.load_model(model_initialization)
                    else:
                        with open(model_initialization, "rb") as f:
                            xgb_classifier: XGBClassifier = pickle_load(f)
                    self.graph.append(SKClassifierModel(xgb_classifier))

                elif model_type == ModelType.XGBOOST_REGRESSOR:
                    from cerebrium.models.sklearn import SKRegressorModel

                    try:
                        from xgboost import XGBRegressor
                    except ImportError as e:
                        raise ImportError(
                            "XGBoost not installed. Please install `xgboost` with pip or conda to run this model type."
                        ) from e

                    if model_initialization.endswith("json"):
                        xgb_regressor = XGBRegressor()
                        xgb_regressor.load_model(model_initialization)
                    else:
                        with open(model_initialization, "rb") as f:
                            xgb_regressor: XGBRegressor = pickle_load(f)
                    self.graph.append(SKRegressorModel(xgb_regressor))

                # Scikit-Learn Interface
                elif model_type == ModelType.SKLEARN_CLASSIFIER:
                    from cerebrium.models.sklearn import SKClassifierModel

                    try:
                        from sklearn.base import ClassifierMixin
                    except ImportError as e:
                        raise ImportError(
                            "SciKit-Learn not installed. Please install `scikit-learn` with pip or conda to run this model type."
                        ) from e

                    with open(model_initialization, "rb") as f:
                        sk_classifier: ClassifierMixin = pickle_load(f)
                    self.graph.append(SKClassifierModel(sk_classifier))

                elif model_type == ModelType.SKLEARN:
                    from cerebrium.models.sklearn import SKRegressorModel

                    try:
                        from sklearn.base import RegressorMixin
                    except ImportError as e:
                        raise ImportError(
                            "SciKit-Learn not installed. Please install `scikit-learn` with pip or conda to run this model type."
                        ) from e

                    with open(model_initialization, "rb") as f:
                        sk_regressor: RegressorMixin = pickle_load(f)
                    self.graph.append(SKRegressorModel(sk_regressor))

                elif model_type == ModelType.SKLEARN_PREPROCESSOR:
                    from cerebrium.models.sklearn import SKPreprocessorModel

                    try:
                        from sklearn.base import BaseEstimator
                    except ImportError as e:
                        raise ImportError(
                            "SciKit-Learn not installed. Please install `scikit-learn` with pip or conda to run this model type."
                        ) from e

                    with open(model_initialization, "rb") as f:
                        sk_preprocessor: BaseEstimator = pickle_load(f)
                    self.graph.append(SKPreprocessorModel(sk_preprocessor))

                # HuggingFace Pipeline
                elif model_type == ModelType.HUGGINGFACE_PIPELINE:
                    from cerebrium.models.hf_pipeline import HFPipeline

                    try:
                        from transformers.pipelines import pipeline
                    except ImportError as e:
                        raise ImportError(
                            "Transformers not installed. Please install `transformers` with pip or conda to run this model type."
                        ) from e

                    hf_pipeline: pipeline = HFPipeline(pipeline(**model_initialization))  # type: ignore
                    self.graph.append(hf_pipeline)

            # If there are processors, create a processors.py file with the respective processors
            # Save the processors.py file in the /usr/local/lib/python3.10/dist-packages/conduit_processors directory

            self.write_processors()
            self.ready = True

    def write_processors(self):
        if not self._processors:
            return
        app_name = os.getenv("APP_NAME", "")
        assert app_name != "", "APP_NAME environment variable not set"
        # get python version from the runtime
        python_version = os.getenv("PYTHON_VERSION", "3.10")
        processor_path = (
            f"/miniconda/envs/{app_name}/lib/python{python_version}/conduit_processors"
        )
        os.makedirs(processor_path, exist_ok=True)
        # Create the processors.py file
        with open(
            f"{processor_path}/processors.py",
            "w",
        ) as f:
            f.write(
                "from cerebrium import save, get, delete, upload\n"
                "import numpy as np\n"
                "import pandas as pd\n"
                "import torch\n"
            )
            for processors in self._processors:
                if processors["pre"]:
                    source = processors["pre"]
                    f.write(source)
                if processors["post"]:
                    source = processors["post"]
                    f.write(source)
        # Create the __init__.py file
        with open(
            f"{processor_path}/__init__.py",
            "w",
        ) as f:
            f.write("from .processors import *\n")

    def run(self, data: Any, files: list = []):
        # sourcery skip: default-mutable-arg
        """
        Run the Conduit on the given input with the stored computational graph.

        Args:
            data (list): The input data to run the Conduit on.
        """
        self.load()
        try:
            from numpy import atleast_2d, ndarray
        except ImportError as e:
            raise ImportError(
                "NumPy not installed. Please install `numpy` with pip or conda to run Conduit."
            ) from e
        if self.contains_torch_model:
            try:
                from torch import Tensor
            except ImportError as e:
                raise ImportError(
                    "PyTorch not installed. Please install `torch` with pip or conda to run Conduit."
                ) from e

        if self._processors:
            # List files in working directory
            files = os.listdir()
            import conduit_processors  # type: ignore

        if not self.ready:
            return "Conduit not ready. Conduit components have not been loaded."
            # If there is no initial pre-processor, convert the data accordingly
        if not self.flow[0][2].get("pre", False):
            if self.flow[0][0] == ModelType.TORCH:
                # attempt to import Tensor from Torch if it exists
                data = Tensor(atleast_2d(data)).to(self.device)  # type: ignore
            elif self.flow[0][0] == ModelType.ONNX:
                if isinstance(data, list):
                    data = data[0]
            elif self.flow[0][0] == ModelType.HUGGINGFACE_PIPELINE:
                pass
            elif self.flow[0][0] == ModelType.SPACY:
                data = data[0]
            elif not any(isinstance(d, bytes) for d in data):
                data = atleast_2d(data)

        # Set input data
        input_data = data

        for (model_type, _, processors), (model) in zip(self.flow, self.graph):
            # Run the preprocessor
            preprocessor: Union[FunctionType, str] = processors.get("pre", "")
            postprocessor: Union[FunctionType, str] = processors.get("post", "")
            if preprocessor:
                if self._processors:
                    assert isinstance(preprocessor, str)
                    preprocessor_function: FunctionType = getattr(conduit_processors, preprocessor)  # type: ignore
                else:
                    assert isinstance(preprocessor, FunctionType)
                    preprocessor_function: FunctionType = preprocessor
                sig = signature(preprocessor_function)
                if len(sig.parameters) == 1:
                    data = preprocessor_function(data)
                elif len(sig.parameters) == 2:
                    data = preprocessor_function(data, files)

            # Ensure that the input data is the correct type
            if self.contains_torch_model:
                if model_type == ModelType.TORCH and not isinstance(data, Tensor):  # type: ignore
                    data = Tensor(data).to(self.device)  # type: ignore
                elif model_type != ModelType.TORCH and isinstance(data, Tensor):  # type: ignore
                    data = data.detach().to("cpu").numpy()

            # Run the model
            data = model.predict(data)

            # Run the postprocessor
            if postprocessor:
                if self._processors:
                    assert isinstance(postprocessor, str)
                    postprocessor_function = getattr(conduit_processors, postprocessor)  # type: ignore
                else:
                    assert isinstance(postprocessor, FunctionType)
                    postprocessor_function: FunctionType = postprocessor
                sig = signature(postprocessor_function)
                if len(sig.parameters) == 1:
                    data = postprocessor_function(data)
                elif len(sig.parameters) == 2:
                    data = postprocessor_function(data, input_data)
                else:
                    data = postprocessor_function(data, input_data, files)

        # Ensure that final output is a list
        if self.contains_torch_model:
            if isinstance(data, Tensor):  # type: ignore
                data = data.detach().to("cpu").numpy().tolist()
        elif isinstance(data, ndarray):
            data = data.tolist()
        elif not isinstance(data, list) and not isinstance(data, dict):
            data = [data]
        return data

    def add_model(
        self,
        model_type: ModelType,
        model_initialization: Union[str, dict],
        postprocessor: Union[
            Dict[Union[Literal["pre"], Literal["post"]], FunctionType], None
        ] = None,
    ):
        """
        Add a model to the Conduit's computational flow.
        """
        temp_flow = self.flow
        model = (model_type, model_initialization, postprocessor or {})
        temp_flow.append(model)  # type: ignore
        self.flow = _check_flow_type(temp_flow)
        self._determine_hardware()

    def add_logger(
        self,
        platform: LoggingPlatform,
        platform_authentication: dict,
        features: list,
        targets: list,
        platform_args: dict = {},
        log_ms: bool = False,
    ):  # sourcery skip: default-mutable-arg
        """
        Add a logger to the Conduit's computational flow.

        Args:
            platform (LoggingPlatform): The logging platform to use.
            platform_authentication (dict): The authentication credentials for the logging platform.
            features (list): The features to log.
            targets (list): The targets to log.
            platform_args (dict, optional): Any additional arguments to pass to the logger. Defaults to {}.
            log_ms (bool, optional): Whether to log the milliseconds of the input data. Defaults to False.
        """
        self.logger_configs[platform.value] = {
            "platform_authentication": platform_authentication,
            "features": features,
            "targets": targets,
            "platform_args": platform_args,
            "log_ms": log_ms,
        }

    def setup_loggers(self):
        """
        Setup the loggers for the Conduit.
        """
        for platform, config in self.logger_configs.items():
            if platform == "Censius":
                from cerebrium.logging.censius import CensiusLogger

                # If there are processors, set the model type to the last model in the flow
                if self._processors:
                    self.logger_configs[platform]["platform_args"]["model_type"] = eval(
                        config[platform]["platform_args"]["model_type"]
                    )
                self.loggers["Censius"] = CensiusLogger(
                    config["platform_authentication"],
                    self.name,
                    config["features"],
                    config["targets"],
                    config["platform_args"],
                    config["log_ms"],
                )
            elif platform == "Arize":
                from cerebrium.logging.arize import ArizeLogger
                from arize.utils.types import (
                    Schema,
                    Embedding,
                )

                # If there are processors, recreate the model type, metrics, schema, and embedding objects
                if self._processors:
                    from pandas import Series

                    self.logger_configs[platform]["platform_args"]["model_type"] = eval(
                        config[platform]["platform_args"]["model_type"]
                    )
                    self.logger_configs[platform]["platform_args"]["metrics"] = [
                        eval(x) for x in config[platform]["platform_args"]["metrics"]
                    ]
                    self.logger_configs[platform]["platform_args"]["schema"] = Schema(
                        **config[platform]["platform_args"]["schema"]
                    )
                    if config[platform]["platform_args"].get("embedding", None):
                        for feature in config[platform]["platform_args"]["embedding"]:
                            self.logger_configs[platform]["platform_args"]["embedding"][
                                feature
                            ] = Embedding(
                                data=config[platform]["platform_args"]["embedding"][
                                    feature
                                ]["data"],
                                vector=Series(
                                    config[platform]["platform_args"]["embedding"][
                                        feature
                                    ]["vector"]
                                ).to_list(),
                            )
                self.loggers["Arize"] = ArizeLogger(
                    config["platform_authentication"],
                    self.name,
                    config["features"],
                    config["targets"],
                    config["platform_args"],
                    config["log_ms"],
                )

    def _jsonify_loggers(self):
        """
        Serialize the loggers to JSON for the Conduit.
        """
        logger_configs = {}
        for platform, config in self.logger_configs.items():
            if platform == "Arize":
                logger_configs[platform] = deepcopy(config)
                logger_configs[platform]["platform_args"]["model_type"] = str(
                    config["platform_args"]["model_type"]
                )
                logger_configs[platform]["platform_args"]["metric"] = [
                    str(x) for x in config["platform_args"]["metric"]
                ]
                logger_configs[platform]["platform_args"]["schema"] = {
                    "prediction_id_column_name": config["platform_args"]["schema"][
                        "prediction_id_column_name"
                    ],
                    "prediction_label_column_name": config["platform_args"]["schema"][
                        "prediction_label_column_name"
                    ],
                    "feature_column_names": config["platform_args"]["schema"][
                        "feature_column_names"
                    ],
                    "tags_column_names": config["platform_args"]["schema"][
                        "tags_column_names"
                    ],
                }
                if config["platform_args"].get("embedding_features", None):
                    logger_configs[platform]["platform_args"][
                        "embedding_features"
                    ] = config["platform_args"]["embedding_features"]
                    for feature in logger_configs[platform]["platform_args"][
                        "embedding_features"
                    ]:
                        logger_configs[platform]["platform_args"]["embedding_features"][
                            feature
                        ] = {
                            "data": logger_configs[platform]["platform_args"][
                                "embedding_features"
                            ][feature]["data"],
                            "vector": logger_configs[platform]["platform_args"][
                                "embedding_features"
                            ][feature]["vector"].tolist(),
                        }

            elif platform == "Censius":
                from censius import ModelType

                logger_configs[platform] = deepcopy(config)
                logger_configs[platform]["platform_args"]["model_type"] = (
                    "ModelType.BINARY_CLASSIFICATION"
                    if (
                        config["platform_args"]["model_type"]
                        == ModelType.BINARY_CLASSIFICATION
                    )
                    else "ModelType.REGRESSION"
                )
        return logger_configs

    def create_json_config(self, filename: str):
        """
        Return the Conduit's configuration as a JSON string.

        Returns:
            str: The Conduit's configuration as a JSON string.
        """

        def get_function_names(
            processors: Dict[Union[Literal["pre"], Literal["post"]], FunctionType]
        ):
            names = {}
            names["pre"] = processors["pre"].__name__ if "pre" in processors else None
            names["post"] = (
                processors["post"].__name__ if "post" in processors else None
            )
            return names

        json_flow = [
            (model_type.value, model_initialization, get_function_names(processors))  # type: ignore
            for model_type, model_initialization, processors in self.flow
        ]
        with open(filename, "w") as f:
            json.dump(
                {
                    "name": self.name,
                    "flow": json_flow,
                    "api_key": self.api_key,
                    "logger_configs": self._jsonify_loggers(),
                    "version": __version__,
                    "processors": [
                        {
                            "pre": None
                            if p[2].get("pre", None) is None
                            else getsource(p[2]["pre"]),  # type: ignore
                            "post": None
                            if p[2].get("post", None) is None
                            else getsource(p[2]["post"]),  # type: ignore
                        }
                        for p in self.flow
                    ],
                    "hardware": self.hardware.value,
                    "python_version": self.python_version.value,
                    "cpu": self.cpu,
                    "memory": self.memory,
                },
                f,
                indent=2,
            )

    def _upload(self, url):
        """
        Upload the Conduit to Cerebrium.

        Args:
            url (str): The upload URL.

        Returns:
            dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the flow token if successful.
        """
        if self.flow == []:
            raise ValueError("Conduit is empty. Please add models to the Conduit.")
        # Clear the graph
        if self.ready:
            print("Clearing the Conduit graph...")
            self.graph = []
            self.ready = False
        # Clear the loggers
        if self.loggers:
            print("Clearing the Conduit loggers...")
            self.loggers = {}
        self.graph = []
        self.ready = False
        # Create a temporary directory to store the Conduit zip
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a zip file of the Conduit, writing the model files and Conduit object to the zip
            with zipfile.ZipFile(f"{tmpdir}/{self.name}.zip", "w") as zip:
                for model_type, model_initialization, _ in self.flow:
                    if model_type != ModelType.HUGGINGFACE_PIPELINE:
                        assert isinstance(model_initialization, str)
                        true_path: str = os.path.abspath(model_initialization)
                        zip.write(true_path, os.path.basename(true_path))

                        ## If the user has provided a requirements file, write it to the zip
                        if self.requirements_file:
                            zip.write(
                                self.requirements_file, arcname="requirements.txt"
                            )

                        ## If the model is a spaCy model, write all the folder contents to the zip
                        ## This is necessary because spaCy models are directories
                        if model_type == ModelType.SPACY:
                            for root, _, files in os.walk(true_path):
                                for file in files:
                                    directory = os.path.basename(root)
                                    directory = (
                                        ""
                                        if root == true_path
                                        else f"/{os.path.basename(root)}"
                                    )
                                    zip.write(
                                        os.path.join(root, file),
                                        os.path.join(
                                            f"{os.path.basename(true_path)}{directory}",
                                            file,
                                        ),
                                    )
                self.create_json_config("conduit.json")
                zip.write("conduit.json")
                # Upload the Conduit zip, chunking with tqdm for progress bar
            with open(f"{tmpdir}/{self.name}.zip", "rb") as f:
                headers = {
                    "Content-Type": "application/zip",
                }
                with tqdm(
                    total=os.path.getsize(f"{tmpdir}/{self.name}.zip"),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:
                    wrapped_f = CallbackIOWrapper(pbar.update, f, "read")
                    response = requests.put(
                        url,
                        headers=headers,
                        data=wrapped_f,  # type: ignore
                        timeout=60,
                        stream=True,
                    )
                data = json.loads(response.text) if response.text else {}
                return {"status_code": response.status_code, "data": data}

    def deploy(self, dry_run=False) -> Union[str, Self]:
        """
        Deploy the Conduit to Cerebrium.

        Returns:
            dict ('status_code': int, 'data': dict): The response code and data. 'data' contains the flow token if successful.
        """
        if not dry_run:
            return self.register()
        if self.flow[0][0] == ModelType.PREBUILT:
            raise NotImplementedError("Dry run not supported for prebuilt models")
        self.load(direct_from_flow=True)
        return self

    def register(self):
        # Check that the user is authenticated
        env = os.getenv("DEVELOPMENT_ENV", "prod")
        upload_url_response = _cerebrium_request(
            "deploy",
            "POST",
            self.api_key,
            payload={
                "name": self.name,
                "cerebrium_version": __version__ if env == "prod" else "0.1.1_dev",
                "hardware": self.hardware.value.upper(),
                "source": "conduit",
                "min_replicas": self.min_replicas,
                "max_replicas": self.max_replicas,
                "python_version": self.python_version.value,
                "cpu": self.cpu,
                "memory": self.memory,
            },
            enable_spinner=(
                True,
                ("Authenticating...", "Authenticated with Cerebrium!"),
            ),
        )
        upload_url = upload_url_response["data"]["uploadUrl"]
        project_id = upload_url_response["data"]["projectId"]
        build_id = upload_url_response["data"]["buildId"]
        endpoint = upload_url_response["data"]["internalEndpoint"]

        print(f"🚀 Deploying {self.name}:{build_id} to Cerebrium...")

        # If Prebuilt model, register with modal
        if self.flow[0][0] == ModelType.PREBUILT:
            print("Registering with Cerebrium...")
            prebuilt_model_response = _cerebrium_request(
                "pre-built-model",
                "POST",
                self.api_key,
                payload={
                    "arguments": {
                        "name": self.name,
                        "externalId": self.flow[0][1],
                        "modelType": _flow_string(self.flow),
                    }
                },
                enable_spinner=(
                    True,
                    ("Registering with Cerebrium...", "Registered with Cerebrium!"),
                ),
            )
            endpoint = prebuilt_model_response["data"]["internalEndpoint"]
            print("🌍 Endpoint:", endpoint)
        else:
            # Upload the conduit artefacts to Cerebrium
            print("⬆️  Uploading conduit resources...")
            self._upload(upload_url)
            print("✅ Conduit resources uploaded successfully.")
            _poll_deployment_status(
                self.api_key, build_id, self.name, project_id, endpoint
            )
        return endpoint
