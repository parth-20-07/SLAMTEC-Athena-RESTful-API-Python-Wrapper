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


class system:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/system"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_capabilities(self) -> ListDictType:
        """Get Robot Capabilities for active agents.

        Returns:
            List of Dictionary Format:
                {
                        "name": "{agent name}":str,
                        "version": "{agent version}":str,
                        "enabled": {enable status}:bool
                }


        """
        self.__LOGGER.INFO("Fetch Robot Capabilities")
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
        """Get Current Power Status

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
        self.__LOGGER.INFO("Fetch Robot Info")
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/status",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    def get_robot_info(self) -> DictType:
        """Get Device Information

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
        self.__LOGGER.INFO("Fetch Robot Information")
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
        """Get Robot Health Status Information.

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
        self.__LOGGER.INFO("Fetch Robot Health")
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
        """Get the current laser observation frame

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
        self.__LOGGER.INFO("Fetch Robot LIDAR Laser Scan")
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
        """Get the system Parameters

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
            self.__LOGGER.INFO("Fetch Max Moving Speed")
            request_param: str = "base.max_moving_speed"
        elif param == "max_w":
            self.__LOGGER.INFO("Fetch Max Angular Velocity")
            request_param: str = "base.max_angular_speed"
        elif param == "dock":
            self.__LOGGER.INFO("Fetch Docking Strategy")
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

    def get_network_status(self) -> DictType:
        """Get the robot's current network status

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
        self.__LOGGER.INFO("Fetch Robot Network Status")
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
        """Get the ADC raw value of the robot IMU

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
        self.__LOGGER.INFO("Fetch Robot Raw ADC IMU Value")
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
        """Get the raw value of the robot IMU

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
        self.__LOGGER.INFO("Fetch Robot Raw Calculated IMU Value")
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/rawimu",
            response_type=Response_Type.JSON,
        )

        result: CombinedType = response.data
        if isinstance(result, dict):
            return result
        else:
            return {}

    ##############################################################################################################
    # Setters
    ##############################################################################################################

    def set_power_status(
        self,
        status: str,
        restart_time_minutes: int = 60,
        shutdown_time_minutes: int = 0,
    ) -> bool:
        """Change Power Status of Robot

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

    def set_robot_max_linear_speed(self, max_speed: float) -> bool:
        """Set Max Linear Speed for Robot

        Args:
            max_speed: Max Speed in m/s. Should be greater than 0.0

        Returns:
            - True => Speed Changed successfully.
            - False => Speed Change Failure
        """
        if max_speed <= 0:
            self.__LOGGER.WARNING("Max Speed Cannot be Less than zero!")
            return False

        self.__LOGGER.INFO("Changing Robot Max Speed")
        request_param: typing.Dict[str, typing.Any] = {
            "param": "base.max_moving_speed",
            "value": str(max_speed),
        }

        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/parameter",
            response_type=Response_Type.JSON,
            body_params=request_param,
        )

        if response.status_code == 200:
            return True
        else:
            return False

    def set_robot_max_angular_velocity(self, max_angular_velocity: float) -> bool:
        """Set Max Angular Velocity for Robot

        Args:
            max_angular_velocity: Max Angular Velocity in rad/s. Should be greater than 0.0

        Returns:
            - True => Speed Changed successfully.
            - False => Speed Change Failure
        """
        if max_angular_velocity <= 0:
            self.__LOGGER.WARNING("Max Angular Velocity Cannot be Less than zero!")
            return False

        self.__LOGGER.INFO("Changing Robot Max Angular Velocity")
        request_param: typing.Dict[str, typing.Any] = {
            "param": "base.max_angular_speed",
            "value": str(max_angular_velocity),
        }

        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/parameter",
            response_type=Response_Type.JSON,
            body_params=request_param,
        )

        if response.status_code == 200:
            return True
        else:
            return False

    def set_robot_emergency_brake(self, engage_brake: bool) -> bool:
        """Engage/Disengage Emergency Brake for Robot

        Args:
            engage_brake:
                - True => Engage Emergency Brake
                - False => Disengage Emergency Brake

        Returns:
            - True => Request success.
            - False => Request Failure
        """
        if engage_brake:
            self.__LOGGER.INFO("Engage Emergency Brake")
            value: str = "on"
        else:
            self.__LOGGER.INFO("Disengage Emergency Brake")
            value: str = "off"

        request_param: typing.Dict[str, typing.Any] = {
            "param": "base.emergency_stop",
            "value": value,
        }

        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/parameter",
            response_type=Response_Type.JSON,
            body_params=request_param,
        )

        if response.status_code == 200:
            return True
        else:
            return False

    def set_robot_brake_release(self, engage_brake: bool) -> bool:
        """Brake Release / Brake Recovery for Robot

        Args:
            engage_brake:
                - True => Brake Release
                - False => Brake Recovery

        Returns:
            - True => Request success.
            - False => Request Failure
        """
        if engage_brake:
            self.__LOGGER.INFO("Release Parking Brake")
            value: str = "on"
        else:
            self.__LOGGER.INFO("Engage Parking Brake")
            value: str = "off"
        request_param: typing.Dict[str, typing.Any] = {
            "param": "base.brake_release",
            "value": value,
        }

        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/parameter",
            response_type=Response_Type.JSON,
            body_params=request_param,
        )

        if response.status_code == 200:
            return True
        else:
            return False

    def set_robot_lights(
        self,
        channel: str,
        control_part: str,
        mode: str,
        color: typing.Tuple[int, int, int],
        brightnessEndColor: typing.Tuple[int, int, int],
        duration: int,
        off_time: int,
    ) -> bool:
        """Set up lighting control effects

        Args:
            channel: LED control channel
                - "One" => One Channel
                - "Two" => Two Channel
            control_part: LED Control Part
                - "Left" => Left Half
                - "Right" => Right Half
            mode: LED control mode
                - "AlwaysBright"
                - "Breathe"
                - "Blink"
                - "HorseLamp"
            color: The constant light, flashing and running modes indicate the color of the LED to be set. The breathing mode indicates the color of the LED when it starts breathing (usually black).
                - r: Red (0-255)
                - g: Green (0-255)
                - b: Blue (0-255)
            brightnessEndColor: The breathing mode indicates the color of the LED at the end of breathing (set the color you want to reach when breathing). The set value needs to be larger than the color value; any value can be filled in for other modes
                - r: Red (0-255)
                - g: Green (0-255)
                - b: Blue (0-255)
            duration: In the constant light mode, you can enter any value; in the breathing mode, enter the single brightness change time (a single change means the time for the color to increase by 1 each time); in the flashing mode, enter the duration of the lighting; in the running mode, enter the time to light up the next light0 (Greater than -1).
            off_time: For flashing mode, enter the duration of the off time; for other modes, enter any value (Greater than -1)

        Returns:
            - True => Set Success
            - False => Set Failure
        """

        self.__LOGGER.INFO("Changing Robot Light Pattern")
        if channel not in ["One", "Two"]:
            self.__LOGGER.WARNING("Invalid Channel Selection")
            return False
        if control_part not in ["Left", "Right"]:
            self.__LOGGER.WARNING("Invalid Control Part")
            return False
        if mode not in ["AlwaysBright", "Bright", "Blink", "HorseLamp"]:
            self.__LOGGER.WARNING("Invalid LED Mode")
            return False

        rc, gc, bc = color
        if (rc > 255 or rc < 0) or (gc > 255 or gc < 0) or (bc > 255 or bc < 0):
            self.__LOGGER.WARNING("Invalid LED Color Value")
            return False
        rb, gb, bb = brightnessEndColor
        if (rb > 255 or rb < 0) or (gb > 255 or gb < 0) or (bb > 255 or bb < 0):
            self.__LOGGER.WARNING("Invalid Brightness End Color Value")
            return False
        if duration < 0:
            self.__LOGGER.WARNING("Duration Value cannot be less than zero")
            return False
        if off_time < 0:
            self.__LOGGER.WARNING("OffTime Value cannot be less than zero")
            return False

        request_param = {
            "channel": channel,
            "controlPart": control_part,
            "mode": mode,
            "color": {"red": rc, "green": gc, "blue": bc},
            "brightnessEndColor": {"red": rb, "green": gb, "blue": bb},
            "brightMs": duration,
            "offMs": off_time,
        }
        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/light/control",
            response_type=Response_Type.JSON,
            body_params=request_param,
        )

        if response.status_code == 200:
            return True
        else:
            return False
