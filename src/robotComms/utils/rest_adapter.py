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

import requests
import requests.packages
import typing

httpStatusCode: typing.Dict[int, str] = {
    200: "SUCCESS",
    204: "NO_CONTENT",
    400: "BAD_REQUEST",
    404: "NOT_FOUND",
    500: "SERVER_INTERNAL_ERROR",
}


class restAdapter:
    def __init__(self) -> None:
        pass

    def get(
        self,
        full_endpoint: str,
        payload: typing.Dict[str, str] = None,
    ) -> typing.Tuple[int, typing.List[typing.Dict[str, str]]]:
        response: requests.Response = requests.get(url=full_endpoint, params=payload)
        data_out: typing.List[typing.Dict[str, str]] = response.json()
        return (response.status_code, data_out)

    def post(
        self,
        full_endpoint: str,
        ep_params: typing.Dict[str, str] = None,
        data: typing.Dict[str, str] = None,
    ) -> int:
        response: requests.Response = requests.post(url=full_endpoint, params=ep_params, json=data)
        data_out: typing.List[typing.Dict[str, str]] = response.json()
        print(data_out)
        return response.status_code

    def delete(
        self,
        full_endpoint: str,
        ep_params: typing.Dict[str, str] = None,
        data: typing.Dict[str, str] = None,
    ) -> int:
        response: requests.Response = requests.delete(
            url=full_endpoint, params=ep_params, json=data
        )
        data_out: typing.List[typing.Dict[str, str]] = response.json()
        print(data_out)
        return response.status_code

    def put(
        self,
        full_endpoint: str,
        ep_params: typing.Dict[str, str] = None,
        data: typing.Dict[str, str] = None,
    ) -> int:
        response: requests.Response = requests.post(url=full_endpoint, params=ep_params, json=data)
        data_out: typing.List[typing.Dict[str, str]] = response.json()
        print(data_out)
        return response.status_code
