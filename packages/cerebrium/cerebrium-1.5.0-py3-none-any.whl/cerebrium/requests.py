import json
import os
import re
import time
import requests
from typing import Tuple, Union
from tenacity import retry, stop_after_delay, wait_fixed
from termcolor import colored
from yaspin import yaspin
from yaspin.spinners import Spinners

from cerebrium.errors import CerebriumRequestError, CerebriumError

ENV = os.getenv("ENV", "prod")
if ENV == "dev":
    print("Using development environment")
    BASE_CEREBRIUM_URL = "https://dev-rest-api.cerebrium.ai"
    DASHBOARD_URL = "https://dev-dashboard.cerebrium.ai"
    TRAINING_URL = "http://dev-training-api.cerebrium.ai/"
else:
    BASE_CEREBRIUM_URL = "https://rest-api.cerebrium.ai"
    DASHBOARD_URL = "https://dashboard.cerebrium.ai"
    TRAINING_URL = "http://training-api.cerebrium.ai/"


def _check_payload(method: str, payload: dict) -> bool:
    """
    Check that the payload for a given method is valid.

    Args:
        payload (dict): The payload to check.

    Returns:
        bool: True if the payload is valid, False otherwise.
    """
    if method == "getUploadUrl":
        if "name" not in payload:
            raise ValueError(f"Payload for '{method}' must contain 'name' key")
    elif method == "pre-built-model":
        if (
            "name" not in payload["arguments"]
            or "externalId" not in payload["arguments"]
            or "modelType" not in payload["arguments"]
        ):
            raise ValueError(
                f"Payload for '{method}' must contain 'name', 'externalId' and 'modelType' keys"
            )
    elif method == "checkDeploymentStatus":
        if "name" not in payload["arguments"]:
            raise ValueError(f"Payload for '{method}' must contain 'name' key")


def _cerebrium_request(
    method: str,
    http_method: str,
    api_key: str,
    payload: Union[dict, None] = None,
    enable_spinner: Tuple[bool, Tuple[str, str]] = (False, ("", "")),
) -> dict:
    """
    Make a request to the Cerebrium API.

    Args:
        method (str): The server method to use.
        api_key (str): The API key for the Cerebrium account.
        payload (dict): The payload to send with the request.
        enable_spinner (List[bool, List[str, str]]): A list containing a boolean to enable the spinner and a list containing the spinner text and spinner type.

    Returns:
        dict ('status_code': int, 'data': dict): The response code and data.
    """

    headers = {"Authorization": api_key, "ContentType": "application/json"}
    url = f"{BASE_CEREBRIUM_URL}/{method}"

    # Make a request to the Cerebrium API
    @retry(stop=stop_after_delay(60), wait=wait_fixed(8))
    def _request():
        data = None if payload is None else json.dumps(payload)
        if http_method == "POST":
            response = requests.post(url, headers=headers, data=data, timeout=30)
        else:
            response = requests.get(url, headers=headers, params=payload, timeout=30)
        return {"status_code": response.status_code, "data": json.loads(response.text)}

    if enable_spinner[0]:
        with yaspin(Spinners.arc, text=enable_spinner[1][0], color="magenta"):
            response = _request()
        if response["status_code"] == 200:
            print(f"✅ {enable_spinner[1][1]}")
        else:
            print(f"✗ {enable_spinner[1][1]}")
            raise CerebriumRequestError(
                response["status_code"],
                method,
                response["data"],
            )
    else:
        response = _request()
    return response


@retry(stop=stop_after_delay(60), wait=wait_fixed(2))
def _poll_deployment_status(
    api_key: str, build_id: str, name: str, project_id: str, endpoint: str
):
    """
    Poll the deployment status of a conduit.

    Args:
        conduit_name (str): The name of the conduit to check the status of.
        api_key (str): The API key for the Cerebrium account.

    Returns:
        str: The endpoint of the deployed model.
    """
    # Check the status of the deployment by polling the Cerebrium API for deployment status
    t1 = time.time()
    seen_index = 0
    with yaspin(text="🔨 Building...", color="yellow") as spinner:
        build_status = "IN_PROGRESS"
        while build_status != "success":
            build_status_response = requests.get(
                f"{BASE_CEREBRIUM_URL}/streamBuildLogs",
                params={"buildId": build_id},
                headers={"Authorization": api_key},
            )
            if build_status_response.status_code != 200:
                print(
                    "API request failed with status code:",
                    build_status_response.status_code,
                )
                raise CerebriumError(
                    build_status_response.text,
                )
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
                        spinner.write(f"{message}")
                    else:
                        spinner.write("\n")
                seen_index = len(logs)
                spinner.text = f"🔨 Building... Status: {build_status}"
                time.sleep(1)
            if time.time() - t1 > 600:
                spinner.fail("Build timed out.")
                raise CerebriumError(
                    "Deployment Timed Out. Your conduit might be large and take longer to deploy. Please try again later."
                )
            elif build_status == "failed":
                spinner.fail("Build failed.")
                raise CerebriumError(
                    "Deployment Failed. Please check your conduit and try again."
                )
        spinner.text = f"Status: {build_status}"
        spinner.ok("🚀 Build complete!")
        print("\n🌍 Endpoint:", endpoint)
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
            f"🔗 View builds: https://dashboard.cerebrium.ai/projects/{project_id}/models/{project_id}-{name}?tab=builds"
        )
        print(
            f"🔗 View runs: https://dashboard.cerebrium.ai/projects/{project_id}/models/{project_id}-{name}?tab=runs"
        )


@retry(stop=stop_after_delay(60), wait=wait_fixed(2))
def _poll_training_deploy_status(training_name: str, api_key: str) -> str:
    """
    Poll the deployment status of a training job.

    Args:
        training_name (str): The name of the training to check the status of.
        api_key (str): The API key for the Cerebrium account.

    Returns:
        str: The endpoint of the deployed model.
    """
    # Check the status of the deployment by polling the Cerebrium API for deployment status
    with yaspin(
        spinner=Spinners.arc, text="Checking deployment status...", color="magenta"
    ) as _:
        response = _cerebrium_request(
            "checkDeploymentStatus",
            "POST",
            api_key,
            payload={"arguments": {"name": training_name}},
        )
    if response["data"]["status"] == "deployed":
        endpoint = response["data"]["endpoint"]
        print("✅ FineTuning deployed!")
        return endpoint
    elif response["data"]["status"] == "failed":
        print("❌ FineTuning deployment failed.")
        raise CerebriumError(response["data"]["failureMessage"])
    else:
        print("⏳ FineTuning deployment in progress...")
        raise CerebriumError(
            "Deployment Not Complete. Your conduit might be large and take longer to deploy. Please try again later."
        )
