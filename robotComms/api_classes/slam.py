from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    DictType,
    ListDictType,
    CombinedType,
)


class slam:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/slam"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_current_robot_pose(self) -> DictType:
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

    def get_current_odometry_pose(self) -> DictType:
        """
        Get the robot's Odometery Pose

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
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/localization/odopose",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_localization_quality(self) -> int:
        """
        Get The positioning quality range is 0 ~ 100, the larger the value, the better the positioning

        Returns: int: 0 - 100

        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/localization/quality",
            response_type=Response_Type.STR,
        )
        result: CombinedType = response.data
        if isinstance(result, str):
            return int(result)
        else:
            return 0

    def check_if_localization_is_enabled(self) -> bool:
        """The return value true indicates that positioning is supported, and false indicates that positioning is suspended, that is, pure mileage mode

        Returns:
            - True => Enabled
            - False => Disabled
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/localization/:enable",
            response_type=Response_Type.STR,
        )
        result: CombinedType = response.data
        if result == "True":
            return True
        else:
            return False

    def check_if_robot_is_in_mapping_or_position_mode(self) -> bool:
        """Check if robot is in Mapping or Positioning Mode

        Returns:
            - True => Mapping Mode
            - False => Position Mode
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/mapping/:enable",
            response_type=Response_Type.STR,
        )
        result: CombinedType = response.data
        if result == "True":
            return True
        else:
            return False

    def check_if_loop_closure_is_enabled(self) -> bool:
        """Check if loop closure is enabled

        Returns:
            - True => Enabled
            - False => Disabled
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/loopclosure/:enable",
            response_type=Response_Type.STR,
        )
        result: CombinedType = response.data
        if result == "True":
            return True
        else:
            return False

    def get_homepose(self) -> DictType:
        """Get the location of the charging station

        Returns:
            Example:
                {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "yaw": 0,
                        "picth": 0,
                        "roll": 0
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/homepose",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        return result

    def get_homedocka(self) -> ListDictType:
        """Get all the charging pile information of the robot

        Returns:
            Example:
                [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                            "pose": {
                                "x": 0,
                                "y": 0,
                                "yaw": 0
                                },
                            "metadata": {}
                            }
                        ]
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/homedocks",
            response_type=Response_Type.LIST_JSON,
        )
        result: CombinedType = response.data
        return result

    def get_imu_data_in_robot_frame(self) -> DictType:
        """Get IMU data expressed in robot coordinate system

        Returns:
            Example:
                {
                        "acc": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "availibilityBitMap": 0,
                        "compass": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "euler_angle": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "gyro": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "quaternion": {
                            "w": 0,
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "raw_acc": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "raw_compass": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "raw_gyro": {
                            "x": 0,
                            "y": 0,
                            "z": 0
                            },
                        "timestamp": 0
                        }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/imu",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        return result

    def get_knoenarea(self) -> DictType:
        """The known area is the scope of the current map. The robot's activity space and various manually marked elements should be within this range

        Returns:
            Example:
                {
                        "x": 0,
                        "y": 0,
                        "width": 0,
                        "height": 0
                        }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/knownarea",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        return result

    def get_composite_map(self) -> str:
        """A composite map containing all data. The response message is a binary byte stream and can be directly saved as an stcm file."""
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/maps/stcm",
            response_type=Response_Type.STR,
        )
        result: CombinedType = response.data
        return result

    ##############################################################################################################
    # Setters
    ##############################################################################################################

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
