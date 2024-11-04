from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    ListDictType,
    CombinedType,
)

import typing


class motion:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/motion"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_supported_actions(
        self,
    ) -> ListDictType:
        """Get All Supported Actions

        Returns:
            [
                    {
                        "action_name": "slamtec.agent.actions.MoveToAction"
                        }
            ]
        """
        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/action-factories",
            response_type=Response_Type.LIST_JSON,
        )
        result: CombinedType = response.data
        return result
