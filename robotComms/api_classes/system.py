from utils.rest_adapter import restAdapter
from utils.logger import systemLogger
from utils.results import Result


class system:
    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    def get_capabilities(self) -> Result:
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
        return self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/capabilities"
        )

    def get_power_status(self) -> Result:
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
        return self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/status"
        )

    def set_power(self, status: str) -> None:
        """

        Change Power Status of Robot

        Args:
            status: Power Modes
            - "shutdown" => Turn off Robot
            - "hibernate" => Light Sleep, For Quick Startup
            - "wakeup" => Wake up Robot from sleep or Shutdown
            - "restart" => Restart Robot
        """
        if status == "shutdown":
            self.__LOGGER.INFO("Shutting Down")
            data = {"shutdown_time_interval": 0, "restart_time_interval": 0}
            self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:shutdown",
                params=data,
            )
        elif status == "hibernate":
            self.__LOGGER.INFO("Setting Hibernating Mode")
            self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:hibernate",
            )
        elif status == "wakeup":
            self.__LOGGER.INFO("Awakening Machine")
            self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:wakeup",
            )
        elif status == "restart":
            self.__LOGGER.INFO("Restarting Machine")
            data = {"mode": "RestartModeSoft"}
            self.__REST_ADAPTER.post(
                full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/power/:restartmodule",
                params=data,
            )
        else:
            self.__LOGGER.WARNING("Invalid Power State")

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/system"
