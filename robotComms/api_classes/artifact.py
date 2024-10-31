from robotComms.utils.rest_adapter import restAdapter
from robotComms.utils.logger import systemLogger
from robotComms.utils.results import (
    combined_Result,
    Response_Type,
    ListDictType,
    CombinedType,
)

import typing


class artifact:
    ##############################################################################################################
    # Class Setup
    ##############################################################################################################

    __IP_ADDR: str = ""
    __API_VERSION: str = ""
    __API_TAG: str = "api/core/artifact"

    def __init__(self, ip_addr: str, api_version: str, logger: systemLogger):
        self.__IP_ADDR = ip_addr
        self.__API_VERSION = api_version
        self.__LOGGER = logger
        self.__REST_ADAPTER = restAdapter(self.__LOGGER)

    ##############################################################################################################
    # Getters
    ##############################################################################################################

    def get_artifact(
        self,
        a_type: str,
        a_usage: typing.Optional[str] = None,
        id: typing.Optional[str | int] = None,
    ) -> bool | ListDictType:
        """Get Map Semantic Elements

        Args:
            a_type: Type of Element to Fetch
                - "line" => Get Virtual Line Segment
                - "rect" => Get the Rectangular Area
                - "poi" => Get all Point of Interest (POIs) in the current Map
                - "laser" => Get Laser Landmarks
            a_usage:
                - a_type = "line":
                    - "tracks" => Virtual Track
                    - "walls" => Virtual Wall
                - a_type = "rect":
                    - "forbidden_area"
                    - "elevator_area"
                    - "dangerous_area"
                    - "coverage_area"
                    - "maintenance_area"
                    - "sensor_disable_area"
                    - "restricted_area"
                - a_type = "poi":
                    - None => Get POI
                - a_type = "laser":
                    - None => Laser landmark refers to the position of the reflector identified by the laser radar.
                    - "update" => Is Slamware automatically updating the laser landmarks?
            id:
                - a_type = "poi":
                    - None => Fetch All POI
                    - "UUID":str => Fetch POI by UUID

        Returns:

        """
        self.__LOGGER.INFO(f"Request: Type:{a_type} | Usage:{a_usage} | ID:{id}")
        endpoint = ""
        # Check Input Conditions
        if a_type == "lines":
            if a_usage not in ["tracks", "walls"]:
                self.__LOGGER.WARNING("Invalid Usage Argument Passed")
                return False
            else:
                endpoint = f"lines/{a_usage}"
            r_type = Response_Type.JSON
        elif a_type == "rect":
            if a_usage not in [
                "forbidden_area",
                "elevator_area",
                "dangerous_area",
                "coverage_area",
                "maintenance_area",
                "sensor_disable_area",
                "restricted_area",
            ]:
                self.__LOGGER.WARNING("Invalid Usage Argument Passed")
                return False
            else:
                endpoint = f"rectangle-areas/{a_usage}"
            r_type = Response_Type.JSON
        elif a_type == "poi":
            a_type = "pois"
            if id is not None:
                endpoint = f"pois/{id}"
            else:
                endpoint = "pois"
            r_type = Response_Type.JSON
        elif a_type == "laser":
            if a_usage is None:
                endpoint = "laser-landmarks"
                r_type = Response_Type.JSON
            elif a_usage == "update":
                endpoint = "laser-landmarks/:update"
                r_type = Response_Type.STR
            else:
                self.__LOGGER.WARNING("Invalid Usage Argument Passed")
                return False
            a_type = "laser-landmarks"
        else:
            self.__LOGGER.WARNING("Invalid Type Argument Passed")
            return False

        response: combined_Result = self.__REST_ADAPTER.get(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/{endpoint}",
            response_type=r_type,
        )
        result: CombinedType = response.data
        return result

    ##############################################################################################################
    # Setters
    ##############################################################################################################
