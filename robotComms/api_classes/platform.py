from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    ListDictType,
    CombinedType,
)


class platform:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/platform"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_timestamp(
        self,
    ) -> str:
        """Gets the number of milliseconds since the system was started. The return value is an integer in string format.

        Returns:
            "string"
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/timestamp",
            response_type=Response_Type.STR,
        )
        result: CombinedType = response.data
        return result

    def get_events(
        self,
    ) -> ListDictType:
        """Get the events that occurred in the robot. The host computer can broadcast voice or perform other interactions. Enabling different plug-ins will expand different event types.

        Returns:
            [
                    {
                        "type": "DEVICE_ERROR",
                        "timestamp": "string"
                        }
            ]
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/events",
            response_type=Response_Type.LIST_JSON,
        )
        result: CombinedType = response.data
        return result
