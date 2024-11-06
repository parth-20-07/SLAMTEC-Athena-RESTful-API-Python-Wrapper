from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    DictType,
    CombinedType,
)


class statistics:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/statistics"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_odometry(
        self,
    ) -> DictType:
        """The total running distance of the robot, in meters

        Returns:
            0
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/odometry",
            response_type=Response_Type.JSON,
        )
        result: CombinedType = response.data
        return result


def get_runtime(
    self,
) -> DictType:
    """The total running time of the robot, in seconds

    Returns:
        0
    """
    response: combined_Result = self.__REST_ADAPTER.get(
        full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/runtime",
        response_type=Response_Type.JSON,
    )
    result: CombinedType = response.data
    return result
