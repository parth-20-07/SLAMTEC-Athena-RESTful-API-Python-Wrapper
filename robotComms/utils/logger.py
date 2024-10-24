"""
Module to Setup Procedural Logging for the system.

Performs two forms of logging:
    -> Logging in a .log file. Is mandatory
    -> Console Logging. Can be turned off if not needed.

Reference: https://betterstack.com/community/questions/how-to-log-to-file-and-console-in-python/
"""

__name__ = "systemLogger"

import logging
import datetime
import os


class systemLogger:
    def __init__(
        self,
        logger_name: str = "logger",
        log_file_path: str = "logs",
        enable_console_logging: bool = True,
    ) -> None:
        """
        Setup Logging System.

        System will perform logging in a .log file,
        which is mandatory and an optional logging to the console.

        Args:
            logger_name: Name for the Logger Instance.
                            Default: 'logger'
            log_file_path: Path for saving the log file. Can be absolute or relative.
                            Default: `{project_dir}/logs/`
            enable_console_logging: Boolean to decide weather to log in console or not.
                            Setting to false will only print ERRORS AND CRITICAL Messages.
                            Default: True
        """
        # Setup Logger
        self._LOGGER: logging.Logger = logging.getLogger(logger_name)
        self._LOGGER.setLevel(logging.DEBUG)

        # Setup Formatting
        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

        # Setup Logger to File => Logs Everything
        if not os.path.exists(log_file_path):
            os.makedirs(log_file_path)
        fileHandler = logging.FileHandler(f"{log_file_path}/{datetime.datetime.now()}-log.log")
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(formatter)

        # Setup Logger for Console => Logs based on user decision
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(formatter)
        if enable_console_logging:
            consoleHandler.setLevel(logging.DEBUG)
        else:
            consoleHandler.setLevel(logging.ERROR)

        # Attach both loggers to logging object
        self._LOGGER.addHandler(fileHandler)
        self._LOGGER.addHandler(consoleHandler)
        self.INFO("Logger Setup Complete")

    def DEBUG(self, message: str) -> None:
        """
        Print Debug Level Messages

        Args:
            message: Message String
        """
        self._LOGGER.debug(message)

    def INFO(self, message: str) -> None:
        """
        Print INFO Level Messages

        Args:
            message: Message String
        """
        self._LOGGER.info(message)

    def WARNING(self, message: str) -> None:
        """
        Print Warning Level Messages

        Args:
            message: Message String
        """
        self._LOGGER.warning(message)

    def ERROR(self, message: str) -> None:
        """
        Print Error Level Messages

        Args:
            message: Message String
        """
        self._LOGGER.error(message)

    def CRITICAL(self, message: str) -> None:
        """
        Print Critical Level Messages

        Args:
            message: Message String
        """
        self._LOGGER.critical(message)
