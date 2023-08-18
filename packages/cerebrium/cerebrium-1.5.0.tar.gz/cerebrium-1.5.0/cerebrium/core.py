import json
import os
import requests
import yaml
from typing import Union, List
from uuid import uuid4

from cerebrium.conduit import Conduit
from cerebrium.flow import CerebriumFlow
from cerebrium.requests import _cerebrium_request, ENV
from cerebrium.utils import _convert_input_data
from cerebrium.errors import CerebriumError


IS_SERVER = os.getenv("IS_SERVER", "false")
_objects = {}
if os.path.exists("secrets.json"):
    with open("secrets.json") as f:
        SECRETS = json.load(f)
elif os.path.exists("secrets.yaml"):
    with open("secrets.yaml") as f:
        SECRETS = yaml.load(f, Loader=yaml.FullLoader)
else:
    SECRETS = {}


def get_secret(key):
    secret = SECRETS.get(key, "") if SECRETS else os.getenv(key, "")
    if secret == "":
        raise CerebriumError(
            f"Secret not found for key: {key}, please check set your environment variable"
        )
    else:
        return secret


def upload(file_name):
    # Upload a file to Cerebrium S3 and return a URL to the file
    from cerebrium.conduit import API_KEY
    from boto3 import client

    if API_KEY and IS_SERVER == "true":
        if not os.environ.get("HARDWARE") in ("GPU", "A10"):
            raise CerebriumError(
                "File storage is only available on GPU and A10 hardware at this time. We are working on expanding this to other hardware."
            )
        s3_client = client("s3")
        file_id = str(uuid4())
        s3_client.upload_file(file_name, f"cerebrium-file-storage-{ENV}", id)
        return _cerebrium_request(
            method="getFileUrl",
            http_method="POST",
            api_key=API_KEY,
            payload={"file_name": file_id},
        )
    else:
        return file_name


def save(name: str, obj: object) -> None:
    """
    Save a Python objec from the current scope to persistent memory so that it can be accessed by processing functions.

    Args:
        name (str): The name to save the object under.
        obj (object): The object to save. This can be any Python object, but must be contained within the scope of the function.
    """
    _objects[name] = obj


def get(name: str) -> None:
    """
    Get a Python object from persistent memory.

    Args:
        name (str): The name of the object to get.

    Returns:
        object: The object saved under the given name.
    """
    try:
        return _objects[name]
    except KeyError as error:
        raise NameError(f"Object '{name}' not found in persistent memory.") from error


def delete(name: str) -> None:
    """
    Delete a Python object from persistent memory.
    """
    try:
        del _objects[name]
    except KeyError as error:
        raise NameError(f"Object '{name}' not found in persistent memory.") from error


def model_api_request(
    model_endpoint: str,
    data: list,
    api_key: str,
    files: Union[List[bytes], None] = None,
) -> dict:
    """
    Make a request to the Cerebrium model API.

    Args:
        model_endpoint (str): The endpoint of the model to make a request to.
        data (list): The data to send to the model.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data.
    """
    payload = _convert_input_data(data)
    headers = {
        "Authorization": api_key,
    }
    if files is not None:
        byte_files = {f"file{i}": (f, open(f, "rb")) for i, f in enumerate(files)}
        byte_files["data"] = (None, json.dumps(payload), "application/json")  # type: ignore
        response = requests.request(
            "POST", model_endpoint, headers=headers, timeout=30, files=byte_files  # type: ignore
        )
    else:
        payload = json.dumps(payload)
        headers["Content-Type"] = "application/json"
        response = requests.request(
            "POST", model_endpoint, headers=headers, data=payload, timeout=30
        )
    return {"status_code": response.status_code, "data": json.loads(response.text)}


def deploy(
    model_flow: CerebriumFlow,
    name: str,
    api_key: str,
    dry_run=False,
    loggers=[],
    hardware=None,
) -> Union[str, Conduit]:  # sourcery skip: default-mutable-arg
    """
    Deploy a model to Cerebrium.

    Args:
        model_flow (CerebriumFlow): The flow to deploy. This is a list of ModelType, model path and postprocessor tuples, as such:
            [(ModelType.TORCH, "model.pt", postprocess_f)]
        name (str): The name to deploy the flow under.
        api_key (str): The API key for the Cerebrium account.
        dry_run (bool): Whether to run the deployment in dry-run mode.
            If True, the model will not be deployed, and deploy will return a flow function which can be used to test with.
        logger (dict): A logger configuration used to create logger which will log ML stats to a metrics platform.
        hardware (Hardware): The hardware to deploy the model on. Can be either "cpu" or "gpu".

    Returns:
        str: The newly deployed REST endpoint. If dry_run is True, a flow function will be returned instead.
    """
    # Check that the flow is valid and create the Conduit
    conduit = Conduit(name, api_key, model_flow, hardware)
    if loggers != []:
        for logger in loggers:
            conduit.add_logger(**logger)
    return conduit.deploy(dry_run=dry_run)
