# System Dependencies
import typing

# Utils Dependencies
from utils.results import Result
from utils.logger import systemLogger
from utils.rest_adapter import restAdapter
from utils.connection import robotConnection

# TODO: Project Plan
# [x] Setup a Switching Interface for URL Connection
# [x] Setup an Endpoint Indexer so we dont make URL at everycall
# [x] Setup Logger:
#       [x] Console Logging
#       [x] File Logging
# [ ] Setup Interface Functions for the ENDPOINTS
# [ ] Restructure Code to meeting the library standards
# [ ] Setup .whl file release to install via pip


class robotComms:
    # Constructors
    def __init__(
        self,
        console_logging: bool = True,
        run_remote_url: bool = False,
        remote_url: str = "",
    ) -> None:
        self.__LOGGER: systemLogger = systemLogger(
            logger_name="robotComms_logger",
            log_file_path="logs",
            enable_console_logging=console_logging,
        )
        self.__ROBOT_CONNETION: robotConnection = robotConnection(self.__LOGGER)

        if not run_remote_url:
            self.__LOGGER.INFO("Communication Instantiated via Local URL")
            self._CURRENT_URL = self.__LOCAL_URL
            self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
                ip_addr=self.__desantize_url(self._CURRENT_URL), remote_connection=False
            )
            if self.__VALID_CONNECTION:
                self.__reindex_api()
                self.__LOGGER.INFO(
                    f"Communication Initiated in Local Network at: {self.__LOCAL_URL}"
                )
            else:
                self.set_local_url()
        else:
            self.__LOGGER.INFO("Communication Instantiated via Remote URL")
            if remote_url == "":
                self.__LOGGER.CRITICAL("You have not provided any Remote URL")
                self.__LOGGER.CRITICAL(
                    f"Do You want to use the saved url: {self.__SAVED_REMOTE_URL} ?"
                )
                confirmation: str = input("(y/n)")
                if confirmation != "y":
                    self.__REMOTE_URL = self.set_new_url()
                else:
                    self.__REMOTE_URL = self.__SAVED_REMOTE_URL
                self._CURRENT_URL = self.__REMOTE_URL
                self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
                    ip_addr=self.__desantize_url(self._CURRENT_URL),
                    remote_connection=True,
                )

            if self.__VALID_CONNECTION:
                self.__reindex_api()
                self.__LOGGER.INFO(
                    f"Communication Initiated in Remote Network at: {self.__REMOTE_URL}"
                )
            else:
                self.set_remote_url()

        self.__API_ADAPTER: restAdapter = restAdapter(logger_instance=self.__LOGGER)

    # Public Methods
    def set_new_url(self, new_url: str = "") -> str:
        # Get Input for Remote URL
        if new_url == "":
            self.__LOGGER.INFO("URL Not Provided.")
            while new_url == "":
                custom_url: str = input("Please Enter New URL: ")
                custom_url = self.__santize_url(custom_url)
                confirmation: str = input(f"Confirm New URL: {custom_url}? (y/n)")
                if confirmation != "y":
                    self.__LOGGER.INFO("Try Again")
                    custom_url = ""
                else:
                    new_url = custom_url
        else:
            new_url = self.__santize_url(new_url)
        self.__LOGGER.INFO(f"URL Confirmed: {new_url}")
        return new_url

    def get_core_system_capabilities(self) -> Result:
        endpoint: str = self.__API_DICTIONARY["core/system/capabilities"]
        response: Result = self.__API_ADAPTER.get(full_endpoint=endpoint)
        return response

    # Private Methods
    def __reindex_api(self) -> None:
        self.__LOGGER.DEBUG("Regenerating API")
        # Clear the existing API typing.Dictionary
        self.__API_DICTIONARY.clear()

        # Generate API and Appdend to typing.Dictionary
        key: str = ""
        value: str = ""
        for plugin in self.__plugins:
            for feature in self.__feature[plugin]:
                if feature == "":
                    feature = plugin
                    for resource in self.__resources[feature]:
                        key = f"{plugin}/{resource}"
                        value = f"{
                            self._CURRENT_URL}/api/{plugin}/{self.__VERSION_NUM}/{resource}"
                        self.__API_DICTIONARY[key] = value
                else:
                    for resource in self.__resources[feature]:
                        key = f"{plugin}/{feature}/{resource}"
                        value = (
                            f"{self._CURRENT_URL}/api/{plugin}"
                            f"/{feature}/{self.__VERSION_NUM}/{resource}"
                        )
                        self.__API_DICTIONARY[key] = value

    def __santize_url(self, url: str) -> str:
        # Check for http in Remote URL
        http_check: str = url[0:7]
        if http_check != "http://":
            url = "http://" + url
        port_check: str = url[-5:]
        if port_check[0] != ":":
            url = url + ":1448"
        return url

    def __desantize_url(self, url: str) -> str:
        # Check for http in Remote URL
        http_check: str = url[0:7]
        if http_check == "http://":
            url = url[7:]
        port_check: str = url[-5:]
        if port_check[0] == ":":
            url = url[0:-5]
        return url

    def get_local_url(self) -> str:
        return self.__LOCAL_URL

    def set_local_url(self, url: str = "") -> None:
        self.__LOCAL_URL = self.set_new_url(url)
        self._CURRENT_URL = self.__LOCAL_URL
        self.__VALID_CONNECTION = self.__VALID_CONNECTION = (
            self.__ROBOT_CONNETION.initialize_connection(
                ip_addr=self.__desantize_url(self._CURRENT_URL), remote_connection=False
            )
        )

        if self.__VALID_CONNECTION:
            self.__reindex_api()
            self.__LOGGER.INFO(
                f"Communication Initiated in Local Network at: {self.__LOCAL_URL}"
            )
        else:
            self.set_local_url()

    def get_remote_url(self) -> str:
        return self.__REMOTE_URL

    def set_remote_url(self, url: str = "") -> None:
        self.__REMOTE_URL = self.set_new_url(url)
        self._CURRENT_URL = self.__REMOTE_URL
        self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
            ip_addr=self.__desantize_url(self._CURRENT_URL), remote_connection=True
        )

        if self.__VALID_CONNECTION:
            self.__reindex_api()
            self.__LOGGER.INFO(
                f"Communication Initiated in Remote Network at: {self.__REMOTE_URL}"
            )
        else:
            self.set_remote_url()

    # Class Variables
    __VALID_CONNECTION: bool = False
    __LOCAL_URL: str = "http://192.168.11.1:1448"
    __SAVED_REMOTE_URL: str = "http://10.168.1.101:1448"
    __REMOTE_URL: str = ""
    __VERSION_NUM: str = "v1"
    # API Interfaces
    __API_DICTIONARY: typing.Dict[str, str] = {}
    __plugins: typing.List[str] = ["core", "platform", "multi-floor", "delivery"]
    __feature: typing.Dict[str, typing.List[str]] = {
        "core": [
            "system",
            "slam",
            "artifact",
            "motion",
            "firmware",
            "statistics",
            "sensors",
            "application",
        ],
        "platform": [""],
        "multi-floor": [
            "map",
            "localization",
        ],
        "delivery": [""],
    }
    __resources: typing.Dict[str, typing.List[str]] = {
        "system": [
            "capabilities",
            "power/status",
            "power/:shutdown",
            "power/:hibernate",
            "power/:wakeup",
            "power/:restartmodule",
            "robot/info",
            "robot/health",
            "laserscan",
            "parameter",
            "network/status",
            "network/route",
            "network/apn",
            "cube/config",
            "light/control",
            "rawadcimu",
            "rawimu",
        ],
        "slam": [
            "localization/pose",
            "localization/odopose",
            "localization/quality",
            "localization/:enable",
            "localization/status/:reset",
            "mapping/:enable",
            "loopclosure/:enable",
            "homepose",
            "homedocks",
            "homedocks/:register",
            "imu",
            "knownarea",
            "maps",
            "maps/explore",
            "maps/stcm",
            "maps/origin",
        ],
        "artifact": [
            "lines",
            "rectangle-areas",
            "pois",
            "pois/:adjust",
            "laser-landmarks",
            "laser-landmarks/:update",
            "laser-landmarks/:remove",
        ],
        "motion": [
            "actions",
            "action-factories",
            "actions/:current",
            "path",
            "milestones",
            "speed",
            "time",
            ":search_path",
            "strategies",
            "strategies/:current",
        ],
        "firmware": [
            "newversion",
            "autoupdate/:enable",
            "autoupdate/:start",
            "update/:start",
            "progress",
        ],
        "statistics": [
            "odometry",
            "runtime",
        ],
        "sensors": [
            "depth/:enable",
            "masks",
        ],
        "application": [
            "apps",
        ],
        "platform": [
            "timestamp",
            "events",
        ],
        "map": [
            "floors",
            "floors/:current",
            "pois",
            "pois/:search_nearby",
            "pois/:dispatch",
            "homedocks",
            "homedocks/:current",
            "homedocks/:search_nearby",
            "stcm",
            "stcm/:save",
            "stcm/:reload",
            "stcm/:sync",
            "search_path_points",
            "elevators",
        ],
        "localization": ["pose"],
        "delivery": [
            "admin/password",
            "admin/mode",
            "admin/language",
            "admin/working_time",
            "admin/move_options",
            "admin/line_speed",
            "configurations",
            "settings",
            "settings/timeout",
            "voice_resources",
            "cargos",
            "cargos/assigned",
            "tasks",
            "tasks/:batch",
            "tasks/orders",
            "tasks/:task_execution",
            "tasks/:task_finish",
            "tasks/:start_pickup",
            "tasks/:end_pickup",
            "tasks/:end_operation",
            "stage",
        ],
    }


def main():
    r1 = robotComms(console_logging=True, run_remote_url=True)
    result = r1.get_core_system_capabilities()
    print(f"Code: {result.status_code} | Log: {result.data}")


if __name__ == "__main__":
    main()
