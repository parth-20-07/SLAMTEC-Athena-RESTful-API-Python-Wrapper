"""
Module to Setup REST Protocol.

Contains Standard Requests for:
    -> GET
    -> POST
    -> DELETE
    -> PUT

Reference: https://www.pretzellogix.net/2021/12/08/step-2-write-a-low-level-rest-adapter/
"""

__name__ = "restAdapter"

# Custom Packages
from utils.logger import systemLogger
from utils.exceptions import restApiExceptions
from utils.models import Result

# Imported Packages
import requests  # https://requests.readthedocs.io/en/latest/user/quickstart/#
import typing
import json


class restAdapter:
    def __init__(
        self,
        logger_instance: typing.Optional[systemLogger] = None,
        timeout: float = 1.0,
    ) -> None:
        self._LOGGER: systemLogger = logger_instance or systemLogger(
            logger_name="restApi_logger",
            log_file_path="logs",
            enable_console_logging=True,
        )
        self._REQUEST_TIMEOUT: float = timeout

    def get(
        self,
        full_endpoint: str,
        params: typing.Optional[typing.Dict[str, str]] = None,
    ) -> Result:
        return self._do(http_method="GET", endpoint=full_endpoint, ep_params=params)

    def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params: typing.Optional[typing.Dict[str, str]] = None,
        data: typing.Optional[typing.Dict[str, str]] = None,
    ) -> Result:
        try:
            self._LOGGER.INFO(f"{http_method} => {endpoint} | Payload: {ep_params}")
            response: requests.Response = requests.request(
                method=http_method,
                url=endpoint,
                params=ep_params,
                timeout=self._REQUEST_TIMEOUT,
            )

        except requests.exceptions.RequestException as e:
            raise restApiExceptions("Request Failed") from e

        try:
            status_code: int = response.status_code
            data_out: typing.List[typing.Dict[str, str]] = response.json()
        except (ValueError, requests.JSONDecodeError) as e:
            raise restApiExceptions("Bad JSON in Response") from e

        if status_code == requests.codes.ok:
            self._LOGGER.INFO(
                f"[OK] => {status_code} : {json.dumps(data_out, indent =2)}"
            )
            return data_out

        raise restApiExceptions(f"{status_code}: {response.reason}")
