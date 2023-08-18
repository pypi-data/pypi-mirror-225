import fnmatch
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import zipfile
from typing import Union

import requests
import typer
from typing_extensions import Annotated
import yaml
import yaspin
from termcolor import colored
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from cerebrium import trainer
from cerebrium.datatypes import PythonVersion, Hardware
from cerebrium import __version__ as cerebrium_version

app = typer.Typer()
env = os.getenv("ENV", "prod")

dashboard_url = (
    "https://dashboard.cerebrium.ai"
    if env == "prod"
    else "https://dev-dashboard.cerebrium.ai"
)
api_url = (
    "https://dev-rest-api.cerebrium.ai"
    if env == "dev"
    else "https://rest-api.cerebrium.ai"
)


@app.command()
def version():
    """
    Print the version of the Cerebrium CLI
    """
    print(cerebrium_version)


@app.command()
def login(
    private_api_key: str = typer.Argument(
        ...,
        help="Private API key for the user. Sets the environment variable CEREBRIUM_API_KEY.",
    )
):
    """
    Set private API key for the user in ~/.cerebrium/config.yaml
    """
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = None

    if config is None:
        config = {"api_key": private_api_key}
    else:
        config["api_key"] = private_api_key
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    print("✅  Logged in successfully.")


def get_api_key():
    config_path = os.path.expanduser("~/.cerebrium/config.yaml")
    if not os.path.exists(config_path):
        print(
            "Please login using 'cerebrium login <private_api_key>' or specify the API key using the --api-key flag."
        )
        sys.exit(1)
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    if config is None or "api_key" not in config:
        print(
            "Please login using 'cerebrium login <private_api_key>' or specify the API key using the --api-key flag."
        )
        sys.exit(1)
    return config["api_key"]


@app.command()
def init_trainer(
    training_type: str = typer.Argument(
        "",
        help="Type of training to run. Can be either 'diffuser' or 'transformer'. Optionally you can choose a specific model. Can be any in {'falcon-7b', 'llama-7b/13b', 'llama2-7b/13b'}",
    ),
    config_path: str = typer.Argument(
        "",
        help="Path to directory where you would like to init a Cerebrium cortex project.",
    ),
    api_key: str = typer.Option(
        "", help="Private API key for the user. Not included in config by default."
    ),
    training_name: str = typer.Option(
        "", help="Name for your training job. Will be stored in a config file."
    ),
    overwrite: bool = typer.Option(
        False, help="Whether to overwrite contents of the init_dir."
    ),
):
    """
    Initialises an empty Cerebrium trainer project.
    """
    # check the config file does not exist
    if os.path.exists(config_path) and not overwrite:
        print(
            "Found a config file at {config_path}. Please specify a new name or use the --overwrite flag if you want to overwrite."
        )
        sys.exit(1)

    # if the config file extention is not yaml, add it
    if os.path.splitext(config_path)[1] != ".yaml":
        config_path = os.path.splitext(config_path)[0] + ".yaml"

    # Load in the config for the training_type
    base_path = os.path.join(os.path.dirname(trainer.__file__), "config")
    base_config_path = os.path.join(base_path, f"{training_type}.yaml")
    if not os.path.exists(base_config_path):
        print(
            f"Your training type {training_type} is not supported yet. Please contact Cerebrium support on Slack or Discord if you would like it added."
        )
        sys.exit(1)

    if training_type not in ["diffuser", "transformer"]:
        transformer_models = ["falcon", "llama", "llama2"]
        if training_type.split("-")[0] in transformer_models:
            training_type = "transformer"

    # modify the base config by matching the yaml params.
    # cannot load the yaml file as we want to preserve comments.
    with open(base_config_path, "r") as f:
        config = f.readlines()

    defaults = {
        "training_type": training_type,
        "name": training_name,
        "api_key": api_key,
    }
    for i, line in enumerate(config):
        for k, v in defaults.items():
            if not v:  # skip if val is None or empty string
                continue
            l = line.lstrip()
            indent_level = len(line) - len(l)  # strip the leading whitespaces
            if l.startswith(f"{k}:"):
                config[i] = f"{' '*indent_level}{k}: {v}\n"

    # write config.yaml
    with open(config_path, "w") as f:
        f.writelines(config)

    print(f"✅  Config file written to {config_path}.")


@app.command()
def init_cortex(
    init_dir: str = typer.Argument(
        "",
        help="Path to directory where you would like to init a Cerebrium cortex project.",
    ),
    overwrite: bool = typer.Option(
        False, help="Whether to overwrite contents of the init_dir."
    ),
    requirements_list: str = typer.Option(
        "",
        help="Optional list of requirements you would like to add. For example \"['transformers', 'datasets', 'sentencepiece==0.1.97']\"",
    ),
    pkg_list: str = typer.Option(
        "",
        help="Optional list of packages you would like to add. For example \"['git', 'ffmpeg' ]\"",
    ),
    conda_pkglist: str = typer.Option(
        "", help="Optional list of conda packages you would like to add."
    ),
    api_key: str = typer.Option(
        "", help="Private API key for the user. Not included in config by default."
    ),
    hardware: str = typer.Option(
        "AMPERE_A5000",
        help="Hardware to use for the Cortex deployment. Defaults to 'GPU'. Can be one of 'CPU', 'GPU', 'A10', 'TURING_4000', 'TURING_5000', 'AMPERE_A4000', 'AMPERE_A5000', 'AMPERE_A6000', 'AMPERE_A100'",
    ),
    cpu: int = typer.Option(
        2,
        help="Number of CPUs to use for the Cortex deployment. Defaults to 2. Can be an integer between 1 and 48",
    ),
    memory: float = typer.Option(
        14.5,
        help="Amount of memory (in GB) to use for the Cortex deployment. Defaults to 14.5GB . Can be a float between 2.0 and 256.0 depending on hardware selection.",
    ),
    include: str = typer.Option(
        "[./*, main.py, requirements.txt, pkglist.txt, conda_pkglist.txt]",
        help="Comma delimited string list of relative paths to files/folder to include. Defaults to all visible files/folders in project root.",
    ),
    exclude: str = typer.Option(
        "[./.*, ./__*]",  # ignore .git etc. by default
        help="Comma delimited string list of relative paths to files/folder to exclude. Defaults to all hidden files/folders in project root.",
    ),
    log_level: str = typer.Option(
        "INFO",
        help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
    disable_animation: bool = typer.Option(
        bool(os.getenv("CI", False)),
        help="Whether to use TQDM and yaspin animations.",
    ),
):
    """
    Initialize an empty Cerebrium Cortex project.
    """
    # Check the hardware val is valid
    if hardware:
        vals = [v.value for v in Hardware]
        assert hardware in vals, f"Hardware must be one of {vals}"
        hardware = Hardware(hardware).value

    # check if init_dir exists, if not create it
    if not os.path.exists(init_dir):
        os.makedirs(init_dir)
    else:
        # check the init_dir is empty, if not throw error and exit
        if os.listdir(init_dir) and not overwrite:
            print("Directory is not empty. Please specify an empty directory.")
            sys.exit(1)

    # write a main.py with the imports and predict function.
    main_file = """from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    # Add your input parameters here
    prompt: str
    your_param: Optional[str] = None # an example optional parameter


def predict(item, run_id, logger):
    item = Item(**item)
    
    ### ADD YOUR CODE HERE

    return {"your_results_variable": results, "your_other_return": "success"} # return your results 

"""
    with open(os.path.join(init_dir, "main.py"), "w") as f:
        f.write(main_file)

    # requirements.txt
    # split the requirements string list into a list
    requirements_list = requirements_list.strip("[]").split(",")
    # if torch, numpy and pydantic are not in requirements_list, add them by default
    if not any(r.find("torch") >= 0 for r in requirements_list):
        requirements_list.append("torch")
    if not any(r.find("numpy") >= 0 for r in requirements_list):
        requirements_list.append("numpy")
    if not any(r.find("pydantic") >= 0 for r in requirements_list):
        requirements_list.append("pydantic")

    with open(os.path.join(init_dir, "requirements.txt"), "w") as f:
        for r in requirements_list:
            f.write(f"{r}\n")

    # pgklist.txt
    pkg_list = pkg_list.strip("[]").replace(",", "\n")
    with open(os.path.join(init_dir, "pkglist.txt"), "w") as f:
        for p in pkg_list:
            f.write(p)

    # conda_pkglist.txt
    conda_pkglist = conda_pkglist.strip("[]").replace(",", "\n")
    with open(os.path.join(init_dir, "conda_pkglist.txt"), "w") as f:
        for c in conda_pkglist:
            f.write(c)

    # config_file with some sensible defaults
    config = {
        "hardware": hardware,
        "log_level": log_level,
        "include": include,
        "exclude": exclude,
        "disable_animation": disable_animation,
        "cpu": cpu,
        "memory": memory,
    }
    if api_key:
        config["api_key"] = api_key
    with open(os.path.join(init_dir, "config.yaml"), "w") as f:
        yaml.dump(config, f, version=(1, 2), sort_keys=True)


@app.command()
def deploy(
    name: str = typer.Argument(..., help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    hardware: str = typer.Option(
        "",
        help="Hardware to use for the Cortex deployment. Defaults to 'GPU'. Can be one of 'CPU', 'GPU', 'A10', 'TURING_4000', 'TURING_5000', 'AMPERE_A4000', 'AMPERE_A5000', 'AMPERE_A6000', 'AMPERE_A100'",
    ),
    cpu: int = typer.Option(
        0,
        help="Number of CPUs to use for the Cortex deployment. Defaults to 2. Can be an integer between 1 and 48 on the new hardware. GPU and A10 have a max of 4.",
    ),
    memory: float = typer.Option(
        0.0,
        help="Amount of memory (in GB) to use for the Cortex deployment. Defaults to 14.5. Can be a float between 2.0 and 256.0 depending on hardware selection.",
    ),
    min_replicas: Union[int, None] = typer.Option(
        None,
        help="Initial minimum number of replicas to create on the Cortex deployment. Defaults to 0",
    ),
    max_replicas: Union[int, None] = typer.Option(
        None,
        help="A hard limit on the maximum number of replicas allow. Defaults to 2 for free users, enterprise and standard users are set to maximum specified in their plan",
    ),
    python_version: str = typer.Option(
        "",
        help="Python version to use. Currently, we support '3.8' to '3.11'. Defaults to '3.10'",
    ),
    include: str = typer.Option(
        "",
        help="Comma delimited string list of relative paths to files/folder to include. Defaults to all visible files/folders in project root.",
    ),
    exclude: str = typer.Option(
        "",
        help="Comma delimited string list of relative paths to files/folder to exclude. Defaults to all hidden files/folders in project root.",
    ),
    init_debug: Union[bool, None] = typer.Option(
        None,
        help="Stops the container after initialization.",
    ),
    pre_init_debug: Union[bool, None] = typer.Option(
        None,
        help="Stops the container before initialization.",
    ),
    log_level: str = typer.Option(
        "",
        help="Log level for the Cortex deployment. Can be one of 'DEBUG' or 'INFO'",
    ),
    config_file: str = typer.Option(
        "",
        help="Path to config.yaml file. You can generate a config using `cerebrium init-cortex`. The contents of the deployment config file are overridden by the command line arguments.",
    ),
    disable_animation: Union[bool, None] = typer.Option(
        None,
        help="Whether to use TQDM and yaspin animations.",
    ),
):
    """
    Deploy a Cortex deployment to Cerebrium
    """

    # Set default params
    params = {
        "hardware": "AMPERE_A5000",
        "cpu": 2,
        "memory": 14.5,
        "python_version": "3.10",
        "include": "[./*, ./main.py, ./requirements.txt, ./pkglist.txt, ./conda_pkglist.txt]",
        "exclude": "[./.*, ./__*]",  # ignore .git etc. by default
        "log_level": "INFO",
        "init_debug": False,
        "pre_init_debug": False,
        "disable_animation": bool(os.getenv("CI", False)),
        "min_replicas": None,  # This is set on the backend.
        "max_replicas": None,
    }

    # If a config file is provided, load it in.
    if config_file:
        if not os.path.exists(config_file):
            print(f"Config file {config_file} not found.")
            sys.exit(1)
        else:
            with open(config_file, "r") as f:
                config = yaml.safe_load(f)

            # remove any params that are none or empty strings
            for k, v in config.copy().items():
                if (v is None) or (isinstance(v, str) and len(v) == 0):
                    _ = config.pop(k)
    else:
        config = {}

    # Override the default params with the config file params
    params.update(config)

    # Override the default params and config with the command line params
    name = name if name else params.get("name", None)
    python_version = (
        python_version if python_version else params.get("python_version", None)
    )
    api_key = api_key if api_key else params.get("api_key", None)
    hardware = hardware if hardware else params.get("hardware", None)
    include = include if include else params.get("include", None)
    exclude = exclude if exclude else params.get("exclude", None)
    log_level = log_level if log_level else params.get("log_level", None)
    init_debug = (
        init_debug if init_debug is not None else params.get("init_debug", None)
    )
    pre_init_debug = (
        pre_init_debug
        if pre_init_debug is not None
        else params.get("pre_init_debug", None)
    )
    disable_animation = (
        disable_animation
        if disable_animation is not None
        else params.get("disable_animation", None)
    )
    min_replicas = (
        min_replicas if min_replicas is not None else params.get("min_replicas", None)
    )
    max_replicas = (
        max_replicas if max_replicas is not None else params.get("max_replicas", None)
    )
    cpu = cpu if cpu else params.get("cpu", None)
    memory = memory if memory else params.get("memory", None)

    # assert name is provided
    if not name:
        print("Please provide a name for your deployment using the --name flag.")
        sys.exit(1)

    # set api_key if not provided
    if not api_key:
        print("No API key provided. Using your login API Key. 🗝️")
        api_key = get_api_key()

    if python_version:
        # Assert that the python version is valid
        vals = [v.value for v in PythonVersion]
        assert python_version in vals, f"Python version must be one of {vals}"

    # Check that hardware is valid and assign to enum
    if hardware:
        vals = [v.value for v in Hardware]
        assert hardware in vals, f"Hardware must be one of {vals}"
        hardware = Hardware(hardware).value
        if hardware == "A10" or hardware == "GPU":
            print(
                "Using V2 hardware. Defaulting to 2 CPU and 14.5 GB memory. Please consider using V3 hardware for better performance."
            )
            cpu = 2
            memory = 14.5

    # Check that CPU is valid
    if cpu:
        assert isinstance(cpu, int), "CPU must be an integer."
        assert cpu >= 1, "CPU must be at least 1."
        if (
            hardware == "AMPERE_A6000"
            or hardware == "AMPERE_A40"
            or hardware == "AMPERE_A100"
        ):
            assert cpu <= 48, f"CPU must be at most 48 for {hardware}."
        else:
            assert cpu <= 36, f"CPU must be at most 36 for {hardware}."

    # Check that memory is valid
    if memory:
        assert isinstance(memory, float) or isinstance(
            memory, int
        ), "Memory must be a number."
        assert memory >= 2.0, "Memory must be at least 2.0 GB."
        assert memory <= 256.0, "Memory must be at most 256.0 GB."
        # if a CPU deployment assert memory is at most 4 times the number of CPUs
        if hardware == "CPU":
            assert (
                memory <= 4 * cpu
            ), "Memory must be at most 4 times the number of CPUs for CPU deployments."
        elif (
            hardware == "AMPERE_A6000"
            or hardware == "AMPERE_A40"
            or hardware == "AMPERE_A100"
        ):
            assert memory <= 256.0, f"Memory must be at most 256.0 GB for {hardware}."
        else:
            assert memory <= 128.0, f"Memory must be at most 128.0 GB for {hardware}."

    # Safety check to ensure no parameter is None
    if any(
        True
        for elem in [
            name,
            api_key,
            python_version,
            hardware,
            include,
            exclude,
            log_level,
            init_debug,
            pre_init_debug,
            disable_animation,
        ]
        if elem is None
    ):
        f"All parameters must be provided. Please check your config file and command line arguments, found the following parameters to be None:"
        params = {
            "name": name,
            "api_key": api_key,
            "python_version": python_version,
            "hardware": hardware,
            "include": include,
            "exclude": exclude,
            "log_level": log_level,
            "init_debug": init_debug,
            "pre_init_debug": pre_init_debug,
            "disable_animation": disable_animation,
        }
        for k, v in params.items():
            if v is None:
                print(f"{k} is None.")

        sys.exit(1)

    print(f"🌍 Deploying {name} with {hardware} hardware to Cerebrium...")

    requirements_hash = "REQUIREMENTS_FILE_DOESNT_EXIST"
    pkglist_hash = "PKGLIST_FILE_DOESNT_EXIST"

    # Check if main.py exists
    if not os.path.exists("./main.py"):
        print("main.py not found in current directory. This file is required.")
        sys.exit(1)

    # Check main.py for a predict function
    with open("./main.py", "r") as f:
        main_py = f.read()
        if "def predict(" not in main_py:
            print(
                "main.py does not contain a predict function. This function is required."
            )
            sys.exit(1)

    # Calc MD5 hash of ./requirements.txt
    if os.path.exists("./requirements.txt"):
        with open("./requirements.txt", "rb") as f:
            requirements_hash = hashlib.md5(f.read()).hexdigest()

    # Calc MD5 hash of ./pkglist.txt if it exists
    if os.path.exists("./pkglist.txt"):
        with open("./pkglist.txt", "rb") as f:
            pkglist_hash = hashlib.md5(f.read()).hexdigest()

    # Hit the deploy endpoint to get the upload URL
    upload_url_response = requests.post(
        f"{api_url}/deploy",
        headers={"Authorization": api_key},
        json={
            "name": name,
            "python_version": python_version,
            "hardware": hardware.upper(),
            "init_debug": init_debug,
            "pre_init_debug": pre_init_debug,
            "log_level": log_level.upper(),
            "cerebrium_version": cerebrium_version,
            "requirements_hash": requirements_hash,
            "pkglist_hash": pkglist_hash,
            "min_replicas": min_replicas,
            "max_replicas": max_replicas,
            "cpu": cpu,
            "memory": memory,
        },
    )

    if upload_url_response.status_code != 200 or (
        upload_url_response.json().get("uploadUrl", None) is None
    ):
        print("API request failed with status code:", upload_url_response.status_code)
        print("Error getting upload URL:", upload_url_response.text)
        upload_url_response.raise_for_status()

    upload_url = upload_url_response.json()["uploadUrl"]
    project_id = upload_url_response.json()["projectId"]
    zip_file_name = upload_url_response.json()["keyName"]
    endpoint = upload_url_response.json()["internalEndpoint"]
    build_id = upload_url_response.json()["buildId"]

    print(f"🆔 Build ID: {build_id}")

    def ensure_pattern_format(pattern):
        if not pattern.startswith("./"):
            pattern = f"./{pattern}"
        elif pattern.startswith("/"):
            raise ValueError(
                "Pattern cannot start with a forward slash. Please use a relative path."
            )
        if pattern.endswith("/"):
            pattern = f"{pattern}*"
        elif os.path.isdir(pattern) and not pattern.endswith("/"):
            pattern = f"{pattern}/*"
        return pattern

    # Zip all files in the current directory and upload to S3
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, zip_file_name)
        dir_name = os.path.dirname(zip_path)
        os.makedirs(dir_name, exist_ok=True)
        with zipfile.ZipFile(zip_path, "w") as zip_file:
            # include files
            include_set = include.strip("[]").split(",")
            # Force include main.py, requirements.txt, pkglist.txt and conda_pkglist.txt
            include_set.extend(
                [
                    "./main.py",
                    "./requirements.txt",
                    "./pkglist.txt",
                    "./conda_pkglist.txt",
                ]
            )
            include_set = set(ensure_pattern_format(pattern) for pattern in include_set)
            exclude_set = exclude.strip("[]").split(",")
            exclude_set = set(ensure_pattern_format(pattern) for pattern in exclude_set)
            file_list = []
            for root, _, files in os.walk("./"):
                for file in files:
                    full_path = os.path.join(root, file)
                    if any(
                        fnmatch.fnmatch(full_path, pattern) for pattern in include_set
                    ) and not any(
                        fnmatch.fnmatch(full_path, pattern) for pattern in exclude_set
                    ):
                        print(f"➕ Adding {full_path}")
                        file_list.append(full_path)

            print("🗂️  Zipping files...")
            for f in file_list:
                if os.path.isfile(f):
                    zip_file.write(f)

        print("⬆️  Uploading to Cerebrium...")
        with open(zip_path, "rb") as f:
            headers = {
                "Content-Type": "application/zip",
            }
            if not disable_animation:
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
            else:
                upload_response = requests.put(
                    upload_url,
                    headers=headers,
                    data=f,
                    timeout=60,
                    stream=True,
                )
            if upload_response.status_code != 200:
                print(
                    "API request failed with status code:", upload_response.status_code
                )
                print("Error uploading to Cerebrium:", upload_response.text)
                sys.exit(1)
            else:
                print("✅ Resources uploaded successfully.")

    # Poll the streamBuildLogs endpoint with yaspin for max of 10 minutes to get the build status
    t1 = time.time()
    seen_index = 0
    build_status = "IN_PROGRESS"
    if not disable_animation:
        spinner = yaspin.yaspin(text="🔨 Building...", color="yellow")
        spinner.start()
    else:
        spinner = None
        print("🔨 Building...")
    while build_status != "success":
        build_status_response = requests.get(
            f"{api_url}/streamBuildLogs",
            params={"buildId": build_id},
            headers={"Authorization": api_key},
        )
        if build_status_response.status_code != 200:
            print(
                "API request failed with status code:",
                build_status_response.status_code,
            )
            print("Error getting build status:", build_status_response.text)
            sys.exit(1)
        else:
            build_status = build_status_response.json()["status"]
            if not (response_logs := build_status_response.json()["logs"]):
                continue

            concat_logs = "".join(response_logs)
            logs = concat_logs.split("\n")[:-1]
            for message in logs[seen_index:]:
                if message:
                    match = re.match(
                        r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{9})Z ", message
                    )
                    if (
                        match is not None
                    ):  # If the regex matches the beginning of the string
                        created = match[1]
                        message = message[len(created) + 2 :]
                    if spinner:
                        spinner.write(f"{message}")
                    else:
                        print(message)
                elif spinner:
                    spinner.write("\n")
                else:
                    print()
            seen_index = len(logs)
            if spinner:
                spinner.text = f"🔨 Building... Status: {build_status}"
            time.sleep(1)
        if time.time() - t1 > 600:
            msg = "⏲️ Build timed out."
            if spinner:
                spinner.fail(msg)
                spinner.stop()
            else:
                print(msg)
            sys.exit(1)
        elif build_status in ["build_failure", "init_failure"]:
            msg = f"🚨 Build failed with status: {build_status}"
            if spinner:
                spinner.fail(msg)
                spinner.stop()
            else:
                print(msg)
            sys.exit(1)
        elif build_status == "success":
            msg = "🚀 Build complete!"
            if spinner:
                spinner.ok(msg)
                spinner.stop()
            else:
                print(msg)
    print("\n🌍 Endpoint:", endpoint, "\n")
    print("💡 You can call the endpoint with the following curl command:")
    print(
        colored(
            f"curl -X POST {endpoint} \\\n"
            "     -H 'Content-Type: application/json' \\\n"
            "     -H 'Authorization: <public_api_key>' \\\n"
            "     --data '{}'",
            "green",
        )
    )
    print("----------------------------------------")
    print(
        f"🔗 View builds: {dashboard_url}/projects/{project_id}/models/{project_id}-{name}?tab=builds"
    )
    print(
        f"🔗 View runs: {dashboard_url}/projects/{project_id}/models/{project_id}-{name}?tab=runs"
    )


@app.command()
def delete_model(
    name: str = typer.Argument(..., help="Name of the Cortex deployment."),
    api_key: str = typer.Option("", help="Private API key for the user."),
):
    """
    Delete a model or training job from Cerebrium
    """
    if not api_key:
        api_key = get_api_key()
    print(f'Deleting model "{name}" from Cerebrium...')
    delete_response = requests.delete(
        f"{api_url}/delete-model",
        headers={"Authorization": api_key},
        json={
            "name": name,
        },
    )
    if delete_response.status_code != 200:
        print("API request failed with status code:", delete_response.status_code)
        print("Error deleting model:", delete_response.text)
        delete_response.raise_for_status()

    if delete_response.json()["success"]:
        print("✅ Model deleted successfully.")
    else:
        print("❌ Model deletion failed.")


@app.command()
def get_training_logs(
    job_id: str = typer.Argument(
        ..., help="Job ID returned for your training instance."
    ),
    api_key: str = typer.Option("", help="Private API key for the user."),
    max_polling_duration: int = typer.Option(
        6000, help="Number of seconds to poll the training. Maximum of 60min."
    ),
):
    """
    Get the training logs for a training job.
    """
    print(f"Retrieving training logs for {job_id}...")
    if not api_key:
        api_key = get_api_key()

    interval = 1  # seconds between polling.
    max_polling_duration = min(max_polling_duration, 60 * 60)

    # Poll the trainingLogs and make the output pretty
    seen_index = 0
    t_start = time.time()
    with yaspin.yaspin(text="Fetching...", color="green") as spinner:
        train_status = "Fetching..."
        while train_status != "succeeded":
            train_status_response = requests.post(
                f"{api_url}/job-logs",
                headers={"Authorization": api_key},
                json={"jobId": job_id},
            )

            if train_status_response.status_code != 200:
                print(
                    "API request failed with status code:",
                    train_status_response.status_code,
                )
                spinner.fail(
                    f"❌ Error fetching training job logs: {train_status_response.text}"
                )
                train_status_response.raise_for_status()
                sys.exit(1)
            else:
                training_response = train_status_response.json()
                train_status = training_response["status"]
                if (
                    train_status == "pending"
                ):  # pending containers have no logs. Update status and continue.
                    spinner.text = f"🏋️ Training... Status: {train_status}"
                    time.sleep(interval)
                    continue

                if not (  # If no logs, continue
                    response_logs := training_response.get("trainingLogs", None)
                ):
                    continue

                concat_logs = "".join(response_logs)
                logs = concat_logs.split("\n")[:-1]

                # If the logs are unavailible and the training has succeeded, the instance has been recycled.
                # Notify the user.
                fail_phrase = "Unfortunately live logs are not available for this job at the moment."  # hardcoded but corresponds to dashboard backend.
                if (
                    train_status == "succeeded"
                    and response_logs[0].find(fail_phrase) != -1
                ):
                    spinner.write(f"🏋️ Training... Status: {train_status}")
                    spinner.write(
                        f"❌ Could not retrieve logs for job: `{job_id}`. Logs are deleted 12hrs after a job has ended."
                    )
                    spinner.text = ""
                    time.sleep(0.2)  # to allow the spinner text time to update
                    break

                for message in logs[seen_index:]:
                    if message:
                        match = re.match(
                            r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{9})Z ", message
                        )
                        if (
                            match is not None
                        ):  # If the regex matches the beginning of the string
                            created = match[1]
                            message = message[len(created) + 2 :]
                        spinner.write(f"{message}")
                    else:
                        spinner.write("\n")

                seen_index = len(logs)

                spinner.text = f"🏋️ Training... Status: {train_status}"
                if train_status == "succeeded":
                    break
                time.sleep(interval)
            if time.time() - t_start > max_polling_duration:
                spinner.fail("⏲️ Training polling timed out.")
                sys.exit(1)
            elif train_status == "failed":
                spinner.fail("❌ Training failed.")
                sys.exit(1)
        spinner.ok("🚀 Training complete!")


@app.command()
def get_training_jobs(
    api_key: str = typer.Option("", help="Private API key for the user."),
    last_n: int = typer.Option(
        10, help="Number of last training jobs to fetch. Defaults to all"
    ),
):
    """
    Get a list of your most recent training jobs.
    """
    print("Getting status of recent training jobs...")
    if not api_key:
        api_key = get_api_key()
    status_response = requests.post(
        f"{api_url}/jobs",
        # f"{api_url}/training-jobs",
        headers={"Authorization": api_key},
        json={},
    )

    if status_response.status_code != 200:
        print("❌ API request failed with status code:", status_response.status_code)
        print("Error: ", status_response.text)
        status_response.raise_for_status()

    trainingJobArr = status_response.json()["trainingJobArr"]

    if last_n > 0:
        trainingJobArr = trainingJobArr[-last_n:]  # get the last n jobs

    # make the printing pretty using panels and boxes using rich. Not for MVP
    if len(trainingJobArr):
        print(
            f"\n{'-' * 60}\n✅Found the following training jobs:\n{'-' * 60}\n{'=' * 60}"
        )
        for trainingJob in trainingJobArr:
            print(
                f"🏋️ Training ID : {trainingJob['id']} 🏋️",
                f"*Job Name*: {trainingJob['name']}",
                f"*Project ID*: {trainingJob['projectId']}",
                f"*Created at*: {trainingJob['createdAt']}",
                f"*Status*: {trainingJob['status']}",
                f"{'=' * 60}",
                sep="\n",
            )
    else:
        print("❌ Found no training jobs")  # redundant catch in case.


@app.command()
def train(
    # Command line takes priority. All can be set in config.
    config_file: str = typer.Option(
        None,
        help="Path to your config YAML file containing your args for training. Will be overridden by command line args.",
    ),
    training_type: Union[str, None] = typer.Option(
        None,
        help='Type of training to run if not provided in the config. Can be either "diffuser" or "transformer".',
    ),
    name: str = typer.Option(
        None, help="Name for your training instance. Overrides config file."
    ),
    api_key: Union[str, None] = typer.Option(
        None, help="Private API key for the user. Overrides the config file"
    ),
    hardware: Union[str, None] = typer.Option(
        None, help="Hardware to use for training. Defaults to AMPERE_A6000."
    ),
    cpu: Union[int, None] = typer.Option(
        None,
        help="Number of CPUs to use for training. Overrides the config file. Defaults to 2.",
    ),
    memory: Union[float, None] = typer.Option(
        None,
        help="Amount of memory (in GB) to use for training. Overrides the config file. Defaults to 16. Can be a number between 2 and 256 depending on the hardware.",
    ),
    config_string: str = typer.Option(
        None,
        help="Config JSON string to use for training. Overrides the config file if the file is provided.",
    ),
    init_debug: bool = typer.Option(
        False,
        help="Stops the container after initialization.",
    ),
    pre_init_debug: bool = typer.Option(
        False,
        help="Stops the container before initialization.",
    ),
    log_level: Union[str, None] = typer.Option(
        None,
        help="Log level for the Trainer Job. Can be one of 'DEBUG', 'INFO', 'WARNING' or 'ERROR'. Overrides the config file.",
    ),
):
    """
    Deploy a fine tuning to Cerebrium
    """
    # check only a config file or a config string is specified
    assert (
        config_file or config_string
    ), "At least one of --config-file or --config-string must be specified."

    # if config file or json, load in
    if config_file:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
    else:
        config = {}

    if config_string:
        config_json = json.loads(config_string)
        config.update(config_json)

    # check if training type is specified in config
    training_type = training_type or config.get("training_type")
    assert (
        training_type is not None
    ), "Training type must be specified in config or command line args."

    # overwrite with command line args if present
    name = name or config["name"]
    if not api_key:
        api_key = config.get(
            "api_key"
        )  # default to config from either the file or the string

    # Validate hardware
    hardware = hardware if hardware else config.get("hardware", "AMPERE_A6000")
    if hardware:
        assert (
            hardware != "A10" or hardware != "GPU"
        ), "A10 and GPU are not supported for training."
        vals = [v.value for v in Hardware]
        assert hardware in vals, f"Hardware must be one of {vals}"
        hardware = Hardware(hardware).value
    else:
        hardware = Hardware.AMPERE_A6000.value

    # Check that CPU is valid
    cpu = cpu if cpu else config.get("cpu", 2)
    if cpu:
        assert isinstance(cpu, int), "CPU must be an integer."
        assert cpu >= 1, "CPU must be at least 1."
        if (
            hardware == "AMPERE_A6000"
            or hardware == "AMPERE_A40"
            or hardware == "AMPERE_A100"
        ):
            assert cpu <= 48, f"CPU must be at most 48 for {hardware}."
        else:
            assert cpu <= 36, f"CPU must be at most 36 for {hardware}."

    # Check that memory is valid
    memory = memory if memory else config.get("memory", 16.0)
    if memory:
        assert isinstance(memory, float) or isinstance(
            memory, int
        ), "Memory must be a number."
        assert memory >= 2.0, "Memory must be at least 2.0 GB."
        assert memory <= 256.0, "Memory must be at most 256.0 GB."
        # if a CPU deployment assert memory is at most 4 times the number of CPUs
        if hardware == "CPU":
            assert (
                memory <= 4 * cpu
            ), "Memory must be at most 4 times the number of CPUs for CPU deployments."
        elif (
            hardware == "AMPERE_A6000"
            or hardware == "AMPERE_A40"
            or hardware == "AMPERE_A100"
        ):
            assert memory <= 256.0, f"Memory must be at most 256.0 GB for {hardware}."
        else:
            assert memory <= 128.0, f"Memory must be at most 128.0 GB for {hardware}."

    # If api key is not provided in any parameter or config, check if it is in the login config file
    if not api_key:
        api_key = get_api_key()

    # get log level
    log_level = log_level or config.get("log_level", "INFO")

    print(f"🌍 Deploying training job {name} with {hardware} hardware to Cerebrium...")

    # check which training
    if training_type == "diffuser":
        diffuser_tuning = trainer.DiffuserTuner(
            name=name, config=config, log_level=log_level
        )
        # upload
        diffuser_tuning._upload(
            api_key=api_key,
            hardware=hardware,
            init_debug=init_debug,
            pre_init_debug=pre_init_debug,
            log_level=log_level,
            cpu=cpu,
            memory=memory,
        )
    elif training_type == "transformer":
        finetuning = trainer.FineTuner(
            name=name,
            config=config,
            log_level=log_level,
        )
        finetuning._upload(
            api_key=api_key,
            hardware=hardware,
            init_debug=init_debug,
            pre_init_debug=pre_init_debug,
            log_level=log_level,
            cpu=cpu,
            memory=memory,
        )


@app.command()
def download_model(
    job_id: str = typer.Argument(..., help="Job ID of your trained model."),
    api_key: str = typer.Option("", help="Private API key for the user."),
    download_path: str = typer.Option(
        "",
        help="Path to download the model to. If not specified, the URL to model will be returned.",
    ),
):
    """
    Return a download link for the model.
    """
    print(f"Downloading model {job_id} from Cerebrium...")
    if not api_key:
        api_key = get_api_key()

    url_response = requests.post(
        f"{api_url}/download-model",
        json={"jobId": job_id},
        headers={"Authorization": api_key},
    )
    if url_response.status_code != 200:
        print(
            "API request failed with status code:",
            url_response.status_code,
        )
        print("Error downloading model:", url_response.text)
        url_response.raise_for_status()
    else:
        model_url = url_response.json()["message"]
        if download_path:
            print(f"Downloading model to {download_path}...")
            download_response = requests.get(
                model_url,
                timeout=60,
                stream=True,
            )

            with open(download_path, "wb") as f:
                with tqdm(
                    total=len(download_response.content),
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    colour="#EB3A6F",
                ) as pbar:
                    for chunk in download_response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                            pbar.update(len(chunk))
                    if download_response.status_code != 200:
                        print(
                            "API request failed with status code:",
                            download_response.status_code,
                        )
                        print("Error downloading model:", download_response.text)
                        download_response.raise_for_status()
                    else:
                        print(f"Download complete. Saved to {download_path}.")
        else:
            print(f"Model download URL: {model_url}")


if __name__ == "__main__":
    app()
