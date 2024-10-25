# Utils Dependencies
from utils.logger import systemLogger
from utils.connection import robotConnection
from api_classes.system import system

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
            self.__CURRENT_URL = self.__LOCAL_URL
            self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
                ip_addr=self.__desantize_url(self.__CURRENT_URL),
                remote_connection=False,
            )
            if self.__VALID_CONNECTION:
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
                self.__CURRENT_URL = self.__REMOTE_URL
                self.__VALID_CONNECTION = self.__ROBOT_CONNETION.initialize_connection(
                    ip_addr=self.__desantize_url(self.__CURRENT_URL),
                    remote_connection=True,
                )

            if self.__VALID_CONNECTION:
                self.__LOGGER.INFO(
                    f"Communication Initiated in Remote Network at: {self.__REMOTE_URL}"
                )
            else:
                self.set_remote_url()

        self.system = system(self.__CURRENT_URL, self.__API_VERSION_NUM, self.__LOGGER)

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

    # Class Variables
    __VALID_CONNECTION: bool = False
    __LOCAL_URL: str = "http://192.168.11.1:1448"
    __SAVED_REMOTE_URL: str = "http://10.168.1.101:1448"
    __REMOTE_URL: str = ""
    __API_VERSION_NUM: str = "v1"


def main():
    r1 = robotComms(console_logging=True, run_remote_url=True)
    power = r1.system.get_power_status()
    print(power)
    result = r1.system.set_power("wakeup")
    print(result)
    power = r1.system.get_power_status()
    print(power)


if __name__ == "__main__":
    main()
