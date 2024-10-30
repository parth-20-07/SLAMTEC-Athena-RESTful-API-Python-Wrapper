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
from utils.results import (
    Response_Type,
    DictType,
    StrType,
    list_Result,
    dict_Result,
    str_Result,
    empty_Result,
    combined_Result,
)

# Imported Packages
import requests  # https://requests.readthedocs.io/en/latest/user/quickstart/#
import typing
import json


class restAdapter:
    def __init__(
        self,
        logger_instance: typing.Optional[systemLogger] = None,
        timeout: float = 2.0,
    ) -> None:
        """

        Args:
            logger_instance: Instance of systemLogger. If not provided, initiates with log name 'restApi_logger'
            timeout: API Request Timeout. Default = 2s
        """
        self._LOGGER: systemLogger = logger_instance or systemLogger(
            logger_name="restApi_logger",
            log_file_path="logs",
            enable_console_logging=True,
        )
        self._REQUEST_TIMEOUT: float = timeout

    def get(
        self,
        full_endpoint: str,
        response_type: Response_Type,
        dict_params: typing.Optional[DictType] = None,
        str_params: typing.Optional[StrType] = None,
    ) -> combined_Result:
        """
        Generate GET Request

        Args:
            full_endpoint: Complete endpoint of format: http://{ip}:{port}/{endpoint}
            params: Dictionary of Parameters to Fetch Data or String Parameter

        Returns:
            Result: Status Code with message
        """
        return self.__do(
            http_method="GET",
            endpoint=full_endpoint,
            response_type=response_type,
            json_params=dict_params,
            str_param=str_params,
        )

    def put(
        self,
        full_endpoint: str,
        response_type: Response_Type,
        dict_params: typing.Optional[DictType] = None,
        str_params: typing.Optional[StrType] = None,
    ) -> combined_Result:
        """
        Generate PUT Request

        Args:
            full_endpoint: Complete endpoint of format: http://{ip}:{port}/{endpoint}
            params: Dictionary of Parameters to Put Data or String Parameter

        Returns:
            Result: Status Code with message
        """
        return self.__do(
            http_method="PUT",
            endpoint=full_endpoint,
            response_type=response_type,
            json_params=dict_params,
            str_param=str_params,
        )

    def post(
        self,
        full_endpoint: str,
        response_type: Response_Type,
        dict_params: typing.Optional[DictType] = None,
        str_params: typing.Optional[StrType] = None,
    ) -> combined_Result:
        """
        Generate POST Request

        Args:
            full_endpoint: Complete endpoint of format: http://{ip}:{port}/{endpoint}
            params: Dictionary of Parameters to Post Data

        Returns:
            Result: Status Code with message
        """
        return self.__do(
            http_method="POST",
            endpoint=full_endpoint,
            response_type=response_type,
            json_params=dict_params,
            str_param=str_params,
        )

    def __do(
        self,
        http_method: str,
        endpoint: str,
        response_type: Response_Type,
        json_params: typing.Optional[DictType] = None,
        str_param: typing.Optional[StrType] = None,
    ) -> combined_Result:
        """

        Perform HTTP Requests

        Args:
            http_method: Request Method GET/PUT/POST/DELETE
            endpoint: API Endpoint
            ep_params: Dictionary of Parameters to pass in request
            data:

        Raises:
            Exception: Status Code Errors

        Returns:
            Result: Status Code with message

        """
        if str_param != "":
            str_param = f"param={str_param}"

        try:
            response: requests.Response = requests.request(
                method=http_method,
                url=endpoint,
                json=json_params,
                params=str_param,
                timeout=self._REQUEST_TIMEOUT,
            )
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            self._LOGGER.INFO(f"{http_method} => {response.url}")

        except requests.exceptions.Timeout as e:
            self._LOGGER.ERROR(f"[ERROR] => 408: Request Timeout | {e}")
            self._LOGGER.INFO(f"Error Requst {http_method} => {e.request}")
            if response_type == Response_Type.LIST_JSON:
                return list_Result(408)
            elif response_type == Response_Type.JSON:
                return dict_Result(408)
            elif response_type == Response_Type.STR:
                return str_Result(408)
            elif response_type == Response_Type.EMPTY:
                return empty_Result(408)

        status_code: int = response.status_code

        if (
            response_type == Response_Type.LIST_JSON
            or response_type == Response_Type.JSON
            or response_type == Response_Type.STR
        ):
            data_out = response.json()

            if isinstance(data_out, list):
                self._LOGGER.INFO(f"[OK] => {status_code} : {json.dumps(data_out, indent =2)}")
                return list_Result(status_code, data_out)
            elif isinstance(data_out, dict):
                self._LOGGER.INFO(f"[OK] => {status_code} : {json.dumps(data_out, indent =2)}")
                return dict_Result(status_code, data_out)
            elif isinstance(data_out, str):
                self._LOGGER.INFO(f"[OK] => {status_code} : {data_out}")
                return str_Result(status_code, data_out)

        else:
            self._LOGGER.INFO(f"[OK] => {status_code}")
            return empty_Result(status_code)
        raise Exception(f"{status_code}: {response.reason}")
