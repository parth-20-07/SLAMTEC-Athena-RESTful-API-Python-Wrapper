from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    DictType,
    CombinedType,
)


class slam:
    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/slam"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    def get_localization_pose(self) -> DictType:
        """
        Get Current Robot Pose

        Returns:
            Example:
                {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "yaw": 0,
                        "pitch": 0,
                        "roll": 0
                }

        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/localization/pose",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def set_localization_pose(
        self, x: float, y: float, z: float, roll: float, pitch: float, yaw: float
    ) -> bool:
        """

        Set Robot Pitch

        Args:
            x: in meter
            y: in meter
            z: in meter
            roll: in radian
            pitch: in radian
            yaw: in radian

        Returns:
            - True => Set Success
            - False => Set Failure

        """
        param = {"x": x, "y": y, "z": z, "roll": roll, "pitch": pitch, "yaw": yaw}
        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/localization/pose",
            response_type=Response_Type.JSON,
            dict_params=param,
        )
        status_code: int = response.status_code
        if status_code == 200:
            return True
        else:
            return False
