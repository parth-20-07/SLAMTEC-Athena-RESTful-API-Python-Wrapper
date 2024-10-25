"""
Connection Module to Establish a connection to the Robot

If the Connection is Local, the connection is tested by pinging the IP Address of the robot.

If the Connection is Remote, the connection is made as follows:
    1. Check if the Docker Container for VPN exists
    2. If not, Make the Docker Container for VPN
    3. Verify that the Docker Container was successfully made
    4. Ping the Remote IP with VPN Active.

"""

# Custom Header
from utils.logger import systemLogger

# System Dependencies
import subprocess
from time import sleep
import docker
from docker.models.containers import Container
import typing
import os


class robotConnection:
    def __init__(self, logger: systemLogger, max_attempts: int = 5) -> None:
        """
        Initialize Connection Module

        Args:
            logger: Reference to the Logging Module
            max_attempts: Max number of Attempts to try pinging. Default: 5
        """
        self.__MAX_CONNECTION_ATTEMPTS = max_attempts
        self.__LOGGER: systemLogger = logger

    def __del__(self):
        """
        Destructor for the Communication Module

        Deletes the VPN Container if the Connection was Remote
        """
        if self.__REMOTE_CONNECTION:
            self.__LOGGER.INFO(f"Deleting Container: {self.__CONTAINER.name}")
            self.__CONTAINER.stop()
            self.__CLIENT.containers.prune()

    def initialize_connection(self, ip_addr: str, remote_connection: bool = False) -> bool:
        """
        1. Initialize the Process for Robot Connection if via VPN
        2. Ping the Robot IP to verify connections


        Args:
            ip_addr: IP Address at which the Robot is to be connected
            remote_connection: Flag to connect the robot via VPN. Default: False

        Returns:
            Connection Status:
                - True => Connection Successful. Robot Contact Successful!
                - False => Connection Failed. Robot cannot be contacted.
        """
        if not remote_connection:  # Connection in local network
            if self.__ping(ip_addr):
                return True
        else:  # Connection in remote network
            if self.__initialize_remote_connection():
                self.__REMOTE_CONNECTION = True
                if self.__ping(ip_addr):
                    return True
        return False

    def __initialize_remote_connection(self) -> bool:
        """
        Initialize Connection via VPN.
        1. Verify if VPN Container Exists.
            -> No:
                1. Make a new container
                2. Verify Container Status
            -> Yes: Start the Container
        Returns:
            setup_status:
                - True => Container Start Success
                - False => Container Start Failure
        """
        self.__LOGGER.INFO("Initializing Docker Client")
        try:
            self.__CLIENT: docker.DockerClient = docker.from_env()
        except Exception:
            self.__LOGGER.ERROR(
                "Docker Service does not seem to be running. Enable service and try again!"
            )
            exit()

        # Check if Docker Container Exists
        verify_container_exist: bool | Container = self.__check_docker_connection(
            docker_client=self.__CLIENT, container_name=self.__VPN_CONTAINER_NAME
        )

        # If container does not exists, make container
        if not isinstance(verify_container_exist, Container):
            verify_container_exist: bool | Container = self.__make_docker_container(
                docker_client=self.__CLIENT,
                container_name=self.__VPN_CONTAINER_NAME,
                docker_image=self.__VPN_IMAGE_NAME,
            )

        # Start Container if it already exists or we were able to make new one
        if isinstance(verify_container_exist, Container):
            self.__LOGGER.INFO(
                f"Starting Container:\n\tName:{verify_container_exist.name}\n\tID: {verify_container_exist.id}"
            )
            self.__CONTAINER: Container = verify_container_exist
            self.__CONTAINER.start()
            return True
        else:
            return False

    def __ping(self, ip_addr: str) -> bool:
        """
        Start a subprocess to run the system process to ping the ip.

        Tries for __MAX_CONNECTION_ATTEMPTS set during the initialization

        Args:
            ip_addr: Ip address. Should not have http:// or port

        Returns:
            ping_status:
                - True => Success to contact
                - False => Failure to contact

        """
        for tryIdx in range(self.__MAX_CONNECTION_ATTEMPTS):
            self.__LOGGER.CRITICAL(f"Checking Connection at IP: {ip_addr}")
            response: subprocess.CompletedProcess = subprocess.run(
                f"ping {ip_addr} -c 1 | grep 'received' | awk -F',' '{{ print $2}}' | awk '{{ print $1}}'",
                shell=True,
                capture_output=True,
                text=True,
            )

            try:
                result: int = int(response.stdout)
            except ValueError:
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

    def __check_docker_connection(
        self, docker_client: docker.DockerClient, container_name: str
    ) -> bool | Container:
        """
        Calls the Docker Client in Background to check if the docker container exists by name.

        Args:
            docker_client: Reference to Docker Client
            container_name: name of Docker Container

        Returns:
            status:
                True => Container Exists
                False => Container Does not Exists

        """
        self.__LOGGER.INFO(f"Searching for Docker Container: {container_name}")
        container_list: typing.List[Container] = docker_client.containers.list(since=container_name)
        if not container_list:
            self.__LOGGER.WARNING(f"Container {container_name} Not Found!!")
            return False
        else:
            self.__LOGGER.INFO(f"Container {container_name} Found!!")

        container: Container = container_list[0]
        return container

    def __make_docker_container(
        self, docker_client: docker.DockerClient, container_name: str, docker_image: str
    ) -> bool | Container:
        """

        Initialize the Docker Container using the ENV Variables:
            - PGY_UNM: Username for the VPN Client Login
            - PGY_PWD: Password for VPN Client Login

        Verify the container exists

        Args:
            docker_client: Reference to the Docker Client
            container_name: Name of Container
            docker_image: Image of Container

        Returns:
            container_id: Reference to container ID

        """
        self.__LOGGER.INFO(
            f"Initializing Docker Container with:\n\t Name: {container_name}\n\t Image: {docker_image}"
        )
        username: str | None = os.environ.get("PGY_UNM")
        password: str | None = os.environ.get("PGY_PWD")
        if username is None or password is None:
            self.__LOGGER.ERROR(
                "VPN Login Credentials don't exist in environment\nPlease ensure Environment Variables PGY_UNM and PGY_PWD Exist."
            )
            exit()

        docker_client.containers.run(
            image=docker_image,
            cap_add=["NET_ADMIN", "SYS_ADMIN"],
            devices=["/dev/net/tun"],
            network_mode="host",
            environment=[f"PGY_USERNAME={username}", f"PGY_PASSWORD={password}"],
            name=container_name,
            detach=True,
        )
        self.__LOGGER.INFO("Docker Initialization Complete. Verify Build!")

        container: bool | Container = self.__check_docker_connection(docker_client, container_name)

        if isinstance(container, Container):
            self.__LOGGER.INFO(f"Docker Initialization Success at ID: {container.id}")
            return container
        else:
            self.__LOGGER.ERROR("Docker Initialization Failed")
            return False

    # Variables
    # Max Number of Connection Attempts before stopping
    __MAX_CONNECTION_ATTEMPTS: int = 0
    # Sleep Time between each connection attempt
    __RETRY_TIME_SECONDS: int = 3
    # VPN Image Name. Make Sure this is correct
    __VPN_IMAGE_NAME: str = (
        "crpi-orhk6a4lutw1gb13.cn-hangzhou.personal.cr.aliyuncs.com/bestoray/pgyvpn"
    )
    # VPN Container Name
    __VPN_CONTAINER_NAME: str = "pgy_vpn"
    # Flag for VPN Connection
    __REMOTE_CONNECTION: bool = False
