from utils.rest_adapter import restAdapter
from utils.logger import systemLogger
from utils.results import (
    combined_Result,
    Response_Type,
    ListDictType,
    DictType,
    CombinedType,
)

import typing


class system:
    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/system"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    def get_capabilities(self) -> ListDictType:
        """

        Get Robot Capabilities for active agents.

        Returns:
            List of Dictionary Format:
                {
                        "name": "{agent name}":str,
                        "version": "{agent version}":str,
                        "enabled": {enable status}:bool
                }


        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/capabilities",
            response_type=Response_Type.LIST_JSON,
        )

        result: CombinedType = response.data
        if isinstance(result, list):
            return result
        else:
            return []

    def get_power_status(self) -> DictType:
        """
        Get Current Power Status

        Returns:
            Example:
            {
                    "batteryPercentage": 90,
                    "dockingStatus": "on_dock",
                    "isCharging": true,
                    "isDCConnected": false,
                    "powerStage": "running",
                    "sleepMode": "awake"
            }

        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/status",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def set_power_status(
        self,
        status: str,
        restart_time_minutes: int = 60,
        shutdown_time_minutes: int = 0,
    ) -> bool:
        """
        Change Power Status of Robot

        Args:
            status: Power Modes
            - "shutdown" => Turn off Robot
            - "hibernate" => Light Sleep, For Quick Startup
            - "wakeup" => Wake up Robot from sleep or Shutdown
            - "restart" => Restart Robot

            restart_time_minutes: Time after which the Robot Should Restart. Kindly do not set it to '0' unless you have an option to physically press the start button on robot. Default: 60
            shutdown_time_minutes: Time after which the Robot Should Shutdown after sending the shutdown command. Default: 0 for immediate shutdown

        Returns:
            request_success:
                - True => Request Success
                - False => Request Failure
            `False` for incorrect Input
        """
        if status == "shutdown":
            if shutdown_time_minutes < 0 or restart_time_minutes < 0:
                return False

            self.__LOGGER.INFO("Shutting Down")
            data = {
                "shutdown_time_interval": shutdown_time_minutes,
                "restart_time_interval": restart_time_minutes,
            }
            response = self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:shutdown",
                response_type=Response_Type.JSON,
                dict_params=data,
            )
            if response.status_code == 200:
                return True
            else:
                return False

        elif status == "hibernate":
            self.__LOGGER.INFO("Setting Hibernating Mode")
            response = self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:hibernate",
                response_type=Response_Type.EMPTY,
            )
            if response.status_code == 200:
                return True
            else:
                return False

        elif status == "wakeup":
            self.__LOGGER.INFO("Awakening Machine")
            response = self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:wakeup",
                response_type=Response_Type.EMPTY,
            )
            if response.status_code == 200:
                return True
            else:
                return False

        elif status == "restart":
            self.__LOGGER.INFO("Restarting Machine")
            data = {"mode": "RestartModeSoft"}
            response = self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:restartmodule",
                response_type=Response_Type.JSON,
                dict_params=data,
            )
            if response.status_code == 200:
                return True
            else:
                return False

        else:
            self.__LOGGER.WARNING("Invalid Power State")
            return False

    def get_robot_info(self) -> DictType:
        """
        Get Device Information

        Returns:
            Example:
                {
                    "manufacturerId": 255,
                    "manufacturerName": "Slamtec",
                    "modelId": 43792,
                    "modelName": "Apollo",
                    "deviceID": "D2E6D7C0F7ABF29EDFEAFEFE1C781D09",
                    "hardwareVersion": "511",
                    "softwareVersion": "3.6.1-rtm+20210807"
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/robot/info",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_robot_health(self) -> DictType:
        """

        Get Robot Health Status Information.

        Returns:
            Example:
                {
                    "hasWarning": false,
                    "hasError": true,
                    "hasFatal": false,
                    "baseError": [
                        {
                            "id": 0,
                            "component": 1,
                            "errorCode": 33621760,
                            "level": 2,
                            "message": "motor barke released"
                        }
                    ]
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/robot/health",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_laserscan(self) -> DictType:
        """

        Get the current laser observation frame

        Returns:
            Example:
                {
                    "pose": {
                        "x": 0,
                        "y": 0,
                        "z": 0,
                        "yaw": 0,
                        "picth": 0,
                        "roll": 0
                    },
                    "laser_points": [
                        {
                            "distance": 0,
                            "angle": 0,
                            "valid": true
                        }
                    ]
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/laserscan",
            response_type=Response_Type.JSON,
        )

        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_system_parameters(self, param: str) -> float | int:
        """
        Get the system Parameters

        Args:
            param:
                - "max_s" => Get Maximum Line Speed
                - "max_w" => Get Maximum Angular Velocity
                - "dock" => Charging pile registration strategy
        Returns:
            value:
                - "max_s" => Maximum Line Speed (default:  -1 for error)
                - "max_w" => Maximum Angular Velocity (default: -1 for error)
                - "dock" =>
                    - -1 => Error,
                    - 1 => Register every time you return to the pile,
                    - 2 => Register when the pile does not exist
                - `-2` for Incorrect Input

        """
        if param == "max_s":
            request_param: str = "base.max_moving_speed"
        elif param == "max_w":
            request_param: str = "base.max_angular_speed"
        elif param == "dock":
            request_param: str = "docking.docked_register_strategy"
        else:
            self.__LOGGER.WARNING("Incorrect System Param Requested!")
            return -2

        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/parameter",
            response_type=Response_Type.STR,
            str_params=request_param,
        )

        if response.status_code != 200:  # Response was empty
            return -1

        value: CombinedType = response.data
        if isinstance(value, str):
            if param == "max_s" or param == "max_w":
                return float(value)
            else:
                if value == "always":
                    return 1
                else:
                    return 2
        return -1

    def set_robot_max_linear_speed(self, max_speed: float) -> bool:
        """

        Set Max Linear Speed for Robot

        Args:
            max_speed: Max Speed in m/s. Should be greater than 0.0

        Returns:
            - True => Speed Changed successfully.
            - False => Speed Change Failure
        """
        if max_speed <= 0:
            self.__LOGGER.WARNING("Max Speed Cannot be Less than zero!")
            return False

        request_param: typing.Dict[str, typing.Any] = {
            "param": "base.max_moving_speed",
            "value": str(max_speed),
        }

        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/parameter",
            response_type=Response_Type.JSON,
            dict_params=request_param,
        )

        if response.status_code == 200:
            return True
        else:
            return False

    def get_network_status(self) -> DictType:
        """
        Get the robot's current network status

        Returns:
            Example:
                {
                    "networkstatus": {
                    "ethip1": "192.168.11.1/24",
                    "ip": "10.6.128.147",
                    "mac": "ec:0e:c4:0a:e4:3b",
                    "mode": "STA",
                    "quality": 100,
                    "ssid": "string"
                    }
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/network/status",
            response_type=Response_Type.JSON,
        )

        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_raw_adc_imu_value(self) -> DictType:
        """
        Get the ADC raw value of the robot IMU

        Returns:
            Example:
                {
                    "acc_x": 0,
                    "acc_y": 0,
                    "acc_z": 0,
                    "gyro_x": 0,
                    "gyro_y": 0,
                    "gyro_z": 0,
                    "comp_x": 0,
                    "comp_y": 0,
                    "comp_z": 0,
                    "timestamp": 0
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/rawadcimu",
            response_type=Response_Type.JSON,
        )

        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_raw_calculated_imu_value(self) -> DictType:
        """
        Get the raw value of the robot IMU

        Returns:
            Example:
                {
                    "acc_x": 0,
                    "acc_y": 0,
                    "acc_z": 0,
                    "gyro_x": 0,
                    "gyro_y": 0,
                    "gyro_z": 0,
                    "comp_x": 0,
                    "comp_y": 0,
                    "comp_z": 0,
                    "timestamp": 0
                }
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/rawimu",
            response_type=Response_Type.JSON,
        )

        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}
