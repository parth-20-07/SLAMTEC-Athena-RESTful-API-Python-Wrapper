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
from typing import Dict, List, Tuple


httpStatusCode: Dict[int, str] = {
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
        self, full_endpoint: str, ep_params: Dict[str, str]
    ) -> Tuple[int, List[Dict[str, str]]]:
        response = requests.get(url=full_endpoint, params=ep_params)
        data: List[Dict[str, str]] = response.json()
        return (response.status_code, data)

    def post(
        self,
        full_endpoint: str,
        ep_params: Dict[str, str],
        data: Dict[str, str],
    ) -> int:
        response = requests.post(url=full_endpoint, params=ep_params, json=data)
        data_out = response.json()
        print(data_out)
        return response.status_code
