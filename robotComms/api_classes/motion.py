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

    def get_action(self, id: typing.Optional[str] = None) -> DictType:
        """Get the action behavior behavior

        Args:
            id: You can query the status of the last 20 actions. If state.status is 4, it means the action has ended. In this case, the success or failure can be determined by result. (Default: None => Returns current Actions)

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

        if id is not None:
            endpoint = f"actions/{id}"
        else:
            endpoint = "actions/:current"
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/{endpoint}",
            response_type=Response_Type.LIST_JSON,
        )
        result: CombinedType = response.data
        return result

    def get_entity(self, entity: str) -> DictType:
        """Get the action behavior behavior

        Args:
            entity:
                - "path": The remaining path points of the current Action
                - "milestones": The remaining target points of the current Action
                - "speed": Get the current speed of the robot
                - "time": Get the remaining movement time of the robot to the destination (estimated value)
                - "strategies": The motion strategy is a combination of a series of internal parameters of Slamware, involving various aspects such as motion speed and obstacle avoidance behavior. Different strategies can be applied to different scenarios. In general, the default strategy can be used.
                - "curr_strat": Get the current motion strategy
        Returns:
            Example:
                entity == "path":
                    {
                            "path_points": [
                                [
                                    0,
                                    0
                                    ]
                                ]
                    }
                entity == "milestones":
                    {
                            "path_points": [
                                [
                                    0,
                                    0
                                    ]
                                ]
                    }
                entity == "speed":
                    {
                            "vx": 0,
                            "vy": 0,
                            "omega": 0
                    }
                entity == "time":
                    0
                entity == "strategies":
                    [
                            "default"
                    ]
                entity == "curr_strat":
                    string

        """

        if entity not in [
            "path",
            "milestones",
            "speed",
            "time",
            "strategies",
            "curr_strat",
        ]:
            self.__LOGGER.ERROR("Invalid Entity Requested")
            return {}
        else:
            if entity == "curr_strat":
                r_type = Response_Type.STR
                entity = "strategies/:current"
            else:
                r_type = Response_Type.JSON
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/{entity}",
            response_type=r_type,
        )
        return response.data

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

    def set_search_path(self, param: DictType):
        """Search for the best path from the robot to the target point

        Args:
            param: Setting Search Path
                Example:
                    {
                            "target": {
                                "x": 0,
                                "y": 0
                                },
                            "timeout": 0
                    }

        Returns:
            Success =>
                {
                    "path_points": [
                        [
                            0,
                            0
                            ]
                        ]
                }
            Failure => {}
        """
        response: combined_Result = self.__REST_ADAPTER.post(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/actions/:search_path",
            response_type=Response_Type.JSON,
            body_params=param,
        )

        if response.status_code == 200:
            return response.data
        else:
            return {}

    def set_movement_strategy(self, strategy: str) -> bool:
        """Setting the Movement Strategy

        Args:
            strategy: String

        Returns:
            - True => Set Success
            - False => Set Failure
        """
        param = {"strategy": strategy}
        response: combined_Result = self.__REST_ADAPTER.post(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/actions/:search_path",
            response_type=Response_Type.STR,
            body_params=param,
        )

        if response.status_code == 200:
            return True
        else:
            return False
