import subprocess
from time import sleep
from utils.logger import systemLogger


class robotConnection:
    def __init__(self, logger: systemLogger, max_attempts: int = 5) -> None:
        self.__MAX_CONNECTION_ATTEMPTS = max_attempts
        self.__LOGGER: systemLogger = logger

    def initialize_connection(
        self, ip_addr: str, remote_connection: bool = False
    ) -> bool:
        if not remote_connection:  # Connection in local network
            if self.__ping(ip_addr):
                return True
        else:  # Connection in remote network
            self.__initialize_docker_connection()
            if self.__ping(ip_addr):
                return True
        return False

    def __initialize_docker_connection(self):
        pass

    def __ping(self, ip_addr: str) -> bool:
        for tryIdx in range(self.__MAX_CONNECTION_ATTEMPTS):
            self.__LOGGER.CRITICAL(f"Checking Connection at IP: {ip_addr}")
            response = subprocess.run(
                f"ping {ip_addr} -c 1 | grep 'received' | awk -F',' '{{ print $2}}' | awk '{{ print $1}}'",
                shell=True,
                capture_output=True,
                text=True,
            )

            try:
                result: int = int(response.stdout)
            except:
                self.__LOGGER.ERROR("Incorrect IP Address provided. Please check!")
                return False

            if result == 1:
                self.__LOGGER.INFO(f"Connection Check Successful at: {ip_addr}")
                return True
            else:
                self.__LOGGER.WARNING(
                    f"Ping Trial {tryIdx}/{self.__MAX_CONNECTION_ATTEMPTS} Failure. Trying Again in {self.__RETRY_TIME_SECONDS}s!"
                )
                sleep(self.__RETRY_TIME_SECONDS)

        self.__LOGGER.ERROR(
            "Connection Check Failure at {ip_addr}. Check the IP Address and Robot Power State Again!"
        )
        return False

    # Variables
    __MAX_CONNECTION_ATTEMPTS: int = 0
    __RETRY_TIME_SECONDS: int = 3
