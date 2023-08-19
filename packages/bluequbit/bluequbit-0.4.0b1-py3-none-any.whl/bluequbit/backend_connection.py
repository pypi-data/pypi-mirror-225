import json
import logging
import os
from pathlib import Path

from .exceptions import BQAPIError, BQError, BQUnauthorizedAccessError
from .http_utils import request_retriable
from .version import __version__

logger = logging.getLogger("bluequbit-python-sdk")


class BackendConnection:
    def __init__(self, api_token=None):
        config_dir = Path.home() / ".config" / "bluequbit"
        config_location = config_dir / "config.json"

        main_endpoint_from_config_file = None
        ssl_verify_from_config_file = None
        token_from_env_variable = os.environ.get("BLUEQUBIT_API_TOKEN")

        if config_location.is_file():
            with config_location.open(encoding="utf-8") as f:
                config = json.load(f)
            main_endpoint_from_config_file = config.get("main_endpoint")
            ssl_verify_from_config_file = config.get("ssl_verify")

        if api_token is None:
            if token_from_env_variable is None:
                raise BQError(
                    "Please specify an API token to init(<your-api-token>) or have API"
                    " token set in BLUEQUBIT_API_TOKEN environment variable. You can"
                    " find your API token once you log in to https://app.bluequbit.io",
                )
            api_token = token_from_env_variable

        self._api_config = {
            "token": api_token,
            "main_endpoint": (
                "https://app.bluequbit.io/api/v1"
                if main_endpoint_from_config_file is None
                else main_endpoint_from_config_file
            ),
            "ssl_verify": (
                True
                if ssl_verify_from_config_file is None
                else ssl_verify_from_config_file
            ),
        }

        try:
            self._token = self._api_config["token"]
        except KeyError:
            raise BQError(
                "Incorrect config file: 'token' key is not present in the config"
                f" file {config_location}.",
            ) from None

        self._default_headers = {
            "Authorization": f"SDK {self._token}",
            "Connection": "close",
            "User-Agent": f"BlueQubit SDK {__version__}",
        }

        self._main_endpoint = "https://app.bluequbit.io/api/v1"
        if (
            "main_endpoint" in self._api_config
            and self._main_endpoint != self._api_config["main_endpoint"]
        ):
            self._main_endpoint = self._api_config["main_endpoint"]
            logger.warning("Using custom endpoint %s", self._main_endpoint)
        self._verify = True
        if "ssl_verify" in self._api_config:
            self._verify = self._api_config["ssl_verify"]
        self._session = None
        self._authenticated = False
        response = self.send_request(
            req_type="GET",
            path="/jobs",
            params={"limit": 1},
            authentication_request=True,
        )

        if response.ok:
            self._authenticated = True
        elif response.status_code == 401:
            raise BQUnauthorizedAccessError
        else:
            raise BQAPIError(
                response.status_code, f"Couldn't reach BlueQubit {response.text}."
            )

    def send_request(
        self,
        req_type,
        path,
        params=None,
        data=None,
        json_req=None,
        headers=None,
        authentication_request=False,
    ):
        if not authentication_request and not self._authenticated:
            raise BQError(
                "BQClient was not initialized. Please provide correct API token to"
                " BQClient(<token>).",
            )
        url = self._main_endpoint + path

        if params is not None:
            for key, value in params.items():
                if isinstance(value, str):
                    params[key] = value.replace("\\", "\\\\")
                if isinstance(value, list):
                    params[key] = ",".join(value)

        if headers is None:
            headers_to_send = self._default_headers
        else:
            headers_to_send = dict(self._default_headers, **headers)

        resp = request_retriable(
            method=req_type,
            url=url,
            data=data,
            json=json_req,
            params=params,
            headers=headers_to_send,
        )
        return resp
