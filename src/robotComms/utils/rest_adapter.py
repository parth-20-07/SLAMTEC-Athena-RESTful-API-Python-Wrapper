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


class restAdapter:
    def __init__(self, logger_instance: systemLogger, timeout: float = 1.0) -> None:
        self._LOGGER: systemLogger = logger_instance
        self._REQUEST_TIMEOUT: float = timeout

    def get(
        self,
        full_endpoint: str,
        params: typing.Optional[typing.Dict[str, str]] = None,
    ) -> typing.Tuple[int, typing.List[typing.Dict[str, str]]]:
        self._do(http_method="GET", endpoint=full_endpoint, ep_params=params)

    def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params: typing.Optional[typing.Dict[str, str]] = None,
        data: typing.Optional[typing.Dict[str, str]] = None,
    ):
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
            data_out: typing.List[typing.Dict[str, str]] = response.json()
        except (ValueError, requests.JSONDecodeError) as e:
            raise restApiExceptions("Bad JSON in Response") from e

        if reponse.status_code == requests.Response.ok:
            self._LOGGER.INFO(f"[OK] => {response.status_code} : {response.json()}")
            return response.json

        raise restApiExceptions(f"{response.status_code}: {response.reason}")
