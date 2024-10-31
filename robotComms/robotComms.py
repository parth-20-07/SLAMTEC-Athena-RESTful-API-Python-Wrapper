# Utils Dependencies
from .utils.logger import systemLogger
from .utils.connection import robotConnection
from .api_classes import system, slam

import json
from pathlib import Path
import typing

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
        remote_url: typing.Optional[str] = None,
    ) -> None:
        self.__LOGGER: systemLogger = systemLogger(
            logger_name="robotComms_logger",
            log_file_path="logs",
            enable_console_logging=console_logging,
        )
        self.__load_old_ip_addresses()
        self.__ROBOT_CONNETION: robotConnection = robotConnection(self.__LOGGER)

        if not run_remote_url:
            self.__LOGGER.INFO("Communication Instantiated via Local URL")
            self.__CURRENT_URL = self.__LOCAL_URL
            self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
                ip_addr=self.__desantize_url(self.__CURRENT_URL),
                remote_connection=False,
            )
            if self.__VALID_CONNECTION:
                self.__CURRENT_URL = self.__santize_url(self.__CURRENT_URL)
                self.__LOGGER.INFO(
                    f"Communication Initiated in Local Network at: {self.__CURRENT_URL}"
                )
            else:
                self.set_local_url()
        else:
            self.__LOGGER.INFO("Communication Instantiated via Remote URL")

            if remote_url is None:
                self.__CURRENT_URL = self.__REMOTE_URL
            else:
                self.__CURRENT_URL = remote_url

            if self.__CURRENT_URL == "":
                self.__REMOTE_URL = self.set_new_url()
                self.__CURRENT_URL = self.__REMOTE_URL

            self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
                ip_addr=self.__desantize_url(self.__CURRENT_URL),
                remote_connection=True,
            )

            if self.__VALID_CONNECTION:
                self.__CURRENT_URL = self.__santize_url(self.__CURRENT_URL)
                self.__LOGGER.INFO(
                    f"Communication Initiated in Remote Network at: {self.__CURRENT_URL}"
                )
            else:
                self.set_remote_url()

        self.system = system(self.__CURRENT_URL, self.__API_VERSION_NUM, self.__LOGGER)
        self.slam = slam(self.__CURRENT_URL, self.__API_VERSION_NUM, self.__LOGGER)

    def __del__(self):
        self.__save_ip_addresses()

    ##############################################################################################################
    # Public Methods
    ##############################################################################################################
    def set_new_url(self, new_url: str = "") -> str:
        # Get Input for Remote URL
        if new_url == "":
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

    def get_local_url(self) -> str:
        return self.__LOCAL_URL

    def set_local_url(self, url: str = "") -> None:
        self.__LOCAL_URL = self.set_new_url(url)
        self.__CURRENT_URL = self.__LOCAL_URL
        self.__VALID_CONNECTION = self.__VALID_CONNECTION = (
            self.__ROBOT_CONNETION.initialize_connection(
                ip_addr=self.__desantize_url(self.__CURRENT_URL),
                remote_connection=False,
            )
        )

        if self.__VALID_CONNECTION:
            self.__LOGGER.INFO(f"Communication Initiated in Local Network at: {self.__LOCAL_URL}")
        else:
            self.set_local_url()

    def get_remote_url(self) -> str:
        return self.__REMOTE_URL

    def set_remote_url(self, url: str = "") -> None:
        self.__REMOTE_URL = self.set_new_url(url)
        self.__CURRENT_URL = self.__REMOTE_URL
        self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
            ip_addr=self.__desantize_url(self.__CURRENT_URL), remote_connection=True
        )

        if self.__VALID_CONNECTION:
            self.__LOGGER.INFO(f"Communication Initiated in Remote Network at: {self.__REMOTE_URL}")
        else:
            self.set_remote_url()

    ##############################################################################################################
    # Private Methods
    ##############################################################################################################

    def __load_old_ip_addresses(self) -> None:
        self.__LOGGER.INFO("Loading Old Remote and Local IP Addresses")
        if Path("ip.json").is_file():
            ip_addr = json.load(open("ip.json"))
            self.__LOCAL_URL = ip_addr["local"]
            self.__REMOTE_URL = ip_addr["remote"]
            self.__LOGGER.INFO(f"Local URL: {self.__LOCAL_URL}")
            self.__LOGGER.INFO(f"Remote URL: {self.__REMOTE_URL}")
        else:
            self.__LOGGER.INFO("IP Log File Does Not Exist!")

    def __save_ip_addresses(self) -> None:
        self.__LOGGER.INFO("Saving Current Remote and Local IP Addresses")
        ip_addr = {"local": self.__LOCAL_URL, "remote": self.__REMOTE_URL}
        json.dump(ip_addr, open("ip.json", "w"))

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
        if port_check != "" and port_check[0] == ":":
            url = url[0:-5]
        return url

    ##############################################################################################################
    # Class Variables
    ##############################################################################################################

    __VALID_CONNECTION: bool = False
    __LOCAL_URL: str = "192.168.11.1"
    __REMOTE_URL: str = ""
    __API_VERSION_NUM: str = "v1"
    __CURRENT_URL: str = ""
