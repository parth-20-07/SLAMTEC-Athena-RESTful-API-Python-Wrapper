# System Dependencies
from typing import List, Dict

# Utils Dependencies
from utils.logger import systemLogger
from utils.rest_adapter import restAdapter

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
        self._LOGGER: systemLogger = systemLogger(
            logger_name="api_logger",
            log_file_path="logs",
            enable_console_logging=console_logging,
        )
        if not run_remote_url:
            self._LOGGER.INFO("Communication Instantiated via Local URL")
            self._CURRENT_URL = self._LOCAL_URL
            self._reindex_api()
            self._LOGGER.INFO(f"Communication Initiated in Local Network at: {self._LOCAL_URL}")
        else:
            self._LOGGER.INFO("Communication Instantiated via Remote URL")
            self._REMOTE_URL = self.set_new_url(remote_url)
            self._CURRENT_URL = self._REMOTE_URL
            self._reindex_api()
            self._LOGGER.INFO(f"Communication Initiated in Remote Network at: {self._REMOTE_URL}")

    # Public Methods
    def set_new_url(self, new_url: str = "") -> str:
        # Get Input for Remote URL
        if new_url == "":
            self._LOGGER.INFO("URL Not Provided.")
            while new_url == "":
                custom_url: str = input("Please Enter New URL: ")
                custom_url = self.santize_url(new_url)
                confirmation: str = input(f"Confirm New URL: {custom_url}? (y/n)")
                if confirmation != "y":
                    self._LOGGER.INFO("Try Again")
                    custom_url = ""
                else:
                    new_url = custom_url
        else:
            new_url = self.santize_url(new_url)
        self._LOGGER.INFO(f"URL Confirmed: {new_url}")
        return new_url

    # Private Methods

    # TODO: URL Indexer

    def _reindex_api(self) -> None:
        self._LOGGER.DEBUG("Regenerating API")
        # Clear the existing API Dictionary
        self._API_DICTIONARY.clear()

        # Generate API and Appdend to Dictionary
        key: str = ""
        value: str = ""
        for plugin in self._plugins:
            for feature in self._feature[plugin]:
                if feature == "":
                    feature = plugin
                    for resource in self._resources[feature]:
                        key = f"{plugin}/{resource}"
                        value = f"{
                            self._CURRENT_URL}/api/{plugin}/{self._VERSION_NUM}/{resource}"
                        self._API_DICTIONARY[key] = value
                else:
                    for resource in self._resources[feature]:
                        key = f"{plugin}/{feature}/{resource}"
                        value = (
                            f"{self._CURRENT_URL}/api/{plugin}"
                            f"/{feature}/{self._VERSION_NUM}/{resource}"
                        )
                        self._API_DICTIONARY[key] = value

        for key in self._API_DICTIONARY:
            self._LOGGER.DEBUG(f"Key: {key} | Value: {self._API_DICTIONARY[key]}")

    # Static Methods
    @staticmethod
    def santize_url(url: str) -> str:
        # Check for http in Remote URL
        http_check: str = url[0:7]
        if http_check != "http://":
            url = "http://" + url
        return url

    # Class Variables
    _LOCAL_URL: str = "http://192.168.11.1:1448"

    def get_local_url(self) -> str:
        return self._LOCAL_URL

    def set_local_url(self, url: str = "") -> None:
        self._LOCAL_URL = self.set_new_url(url)
        self._CURRENT_URL = self._LOCAL_URL
        self._reindex_api()
        self._LOGGER.INFO(f"Communication Initiated in Local Network at: {self._LOCAL_URL}")

    _REMOTE_URL: str = ""

    def get_remote_url(self) -> str:
        return self._REMOTE_URL

    def set_remote_url(self, url: str = "") -> None:
        self._REMOTE_URL = self.set_new_url(url)
        self._CURRENT_URL = self._REMOTE_URL
        self._reindex_api()
        self._LOGGER.INFO(f"Communication Initiated in Remote Network at: {self._REMOTE_URL}")

    _VERSION_NUM: str = "v1"

    # API Interfaces
    _API_DICTIONARY: Dict[str, str] = {}
    _plugins: List[str] = ["core", "platform", "multi-floor", "delivery"]
    _feature: Dict[str, List[str]] = {
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
    _resources: Dict[str, List[str]] = {
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
    r1 = robotComms(console_logging=True)
    print(r1)
    ra = restAdapter()
    res = ra.get(
        full_endpoint="http://api.thecatapi.com/v1/images/search",
        ep_params={"limit": "5"},
    )
    print(res)


if __name__ == "__main__":
    main()
