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
import utils.logger as log

# Imported Packages
import requests  # https://requests.readthedocs.io/en/latest/user/quickstart/#
import typing


class restAdapter:
    def __init__(self, logger_instance: log.systemLogger, timeout: float = 1.0) -> None:
        self._LOGGER: log.systemLogger = logger_instance
        self._REQUEST_TIMEOUT: float = timeout

    def get(
        self,
        full_endpoint: str,
        dict_payload: typing.Dict[str, str] = None,
    ) -> typing.Tuple[int, typing.List[typing.Dict[str, str]]]:
        response: requests.Response = requests.request(
            method="GET",
            url=full_endpoint,
            params=dict_payload,
            timeout=self._REQUEST_TIMEOUT,
        )
        data_out: typing.List[typing.Dict[str, str]] = response.json()

        self._LOGGER.INFO(f"GET => {response.url}")
        if response.status_code == requests.codes.ok:
            self._LOGGER.INFO(f"[OK] => {response.status_code} : {response.json()}")
        else:
            self._LOGGER.CRITICAL(f"[ERROR] => {response.status_code} : {response.json()}")
        return (response.status_code, data_out)

    def post(self, full_endpoint: str, dict_payload: typing.Dict[str, str] = None) -> int:
        response: requests.Response = requests.request(
            method="POST",
            url=full_endpoint,
            data=dict_payload,
            timeout=self._REQUEST_TIMEOUT,
        )
        data_out: typing.List[typing.Dict[str, str]] = response.json()
        self._LOGGER.INFO(f"POST => {response.url}")
        if response.status_code == requests.codes.ok:
            self._LOGGER.INFO(f"[OK] => {response.status_code} : {response.json()}")
        else:
            self._LOGGER.CRITICAL(f"[ERROR] => {response.status_code} : {response.json()}")
        return response.status_code

    def delete(
        self,
        full_endpoint: str,
        ep_params: typing.Dict[str, str] = None,
        data: typing.Dict[str, str] = None,
    ) -> int:
        response: requests.Response = requests.request(
            method="DELETE",
            url=full_endpoint,
            params=ep_params,
            json=data,
            timeout=self._REQUEST_TIMEOUT,
        )
        data_out: typing.List[typing.Dict[str, str]] = response.json()
        self._LOGGER.INFO(f"DELETE => {response.url}")
        if response.status_code == requests.codes.ok:
            self._LOGGER.INFO(f"[OK] => {response.status_code} : {response.json()}")
        else:
            self._LOGGER.CRITICAL(f"[ERROR] => {response.status_code} : {response.json()}")
        return response.status_code

    def put(
        self,
        full_endpoint: str,
        ep_params: typing.Dict[str, str] = None,
        data: typing.Dict[str, str] = None,
    ) -> int:
        response: requests.Response = requests.request(
            method="PUT",
            url=full_endpoint,
            params=ep_params,
            json=data,
            timeout=self._REQUEST_TIMEOUT,
        )

        data_out: typing.List[typing.Dict[str, str]] = response.json()
        self._LOGGER.INFO(f"PUT => {response.url}")
        if response.status_code == requests.codes.ok:
            self._LOGGER.INFO(f"[OK] => {response.status_code} : {response.json()}")
        else:
            self._LOGGER.CRITICAL(f"[ERROR] => {response.status_code} : {response.json()}")
        return response.status_code
