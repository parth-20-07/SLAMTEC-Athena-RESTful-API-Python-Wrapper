from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    ListDictType,
    DictType,
    CombinedType,
)

import typing


class motion:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/motion"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_supported_actions(
        self,
    ) -> ListDictType:
        """Get All Supported Actions

        Returns:
            [
                    {
                        "action_name": "slamtec.agent.actions.MoveToAction"
                        }
            ]
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/action-factories",
            response_type=Response_Type.LIST_JSON,
        )
        result: CombinedType = response.data
        return result

    def get_current_action(
        self,
    ) -> DictType:
        """Get the current behavior

        Returns:
            {
                    "action_id": 0,
                    "action_name": "string",
                    "stage": "GOING_TO_TARGET",
                    "state": {
                        "status": 0,
                        "result": 0,
                        "reason": ""
                        }
            }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/actions/:current",
            response_type=Response_Type.LIST_JSON,
        )
        result: CombinedType = response.data
        return result

    ##############################################################################################################
    # Setters
    ##############################################################################################################
    def delete_current_action(
        self,
    ) -> bool:
        """Terminate the current behavior

        Returns:
            - True => Action Delete Success
            - False => Action Delete Failure
        """
        response: combined_Result = self.__REST_ADAPTER.delete(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/actions/:current",
            response_type=Response_Type.EMPTY,
        )
        status_code: int = response.status_code
        if status_code == 200:
            return True
        else:
            return False

    def create_new_motion(self, request_body: DictType) -> DictType:
        """Create New Motion Behavior

        Args:
            request_body: action_name is queried through the `get_supported_actions()` interface, and the specific content of options depends on the action type.
            Example:
                {
                        "action_name": "slamtec.agent.actions.MoveToAction",
                        "options": {
                            "target": {
                                "x": 0,
                                "y": 0,
                                "z": 0
                                },
                            "move_options": {
                                "mode": 0,
                                "flags": [],
                                "yaw": 0,
                                "acceptable_precision": 0,
                                "fail_retry_count": 0,
                                "speed_ratio": 0
                                }
                            }
                }

        Returns:
            - Success
                Example:
                    {
                            "action_id": 0,
                            "action_name": "string",
                            "stage": "GOING_TO_TARGET",
                            "state": {
                                "status": 0,
                                "result": 0,
                                "reason": ""
                                }
                    }
            - Failure => Empty Dictionary
        """
        response: combined_Result = self.__REST_ADAPTER.post(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/actions/:current",
            response_type=Response_Type.JSON,
            body_params=request_body,
        )

        if response.status_code == 200:
            return response.data
        else:
            return {}
