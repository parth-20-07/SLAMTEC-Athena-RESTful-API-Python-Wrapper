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
                - a_type = "lines":
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

    def add_artifact(
        self,
        a_type: str,
        a_usage: typing.Optional[str] = None,
        dict_value: typing.Optional[ListDictType] = None,
    ) -> bool | ListDictType:
        """Add Map Semantic Elements

                        Args:
                            a_type: Type of Element to Fetch
                                - "line" => Add Virtual Line Segment
                                - "rect" => Add a Rectangular Area
                                - "poi" => Add POI
                                - "laser" => Set Laser Landmarks
                            a_usage:
                                - a_type = "lines":
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
                                    - "adjust" => If you add POIs when building a map, the POIs will adjust their poses after the loop is closed. Calling this interface can further reduce the error of pose adjustment.
        [Note] This is only valid after the loop is closed, and it is not necessary to call it at other times.
                                - a_type = "laser":
                                    - "remove" => Delete some laser landmarks. The request message is an ID array. The ID comes from the id field of the content returned by the laser landmark acquisition interface.
                            dict_value: Data to add to Map
                                Examples:
                                    - a_type = "lines" ["tracks", "walls"]: When adding, id is an invalid field and can be any value.
                                        [
                                                {
                                                    "id": 0,
                                                    "start": {
                                                        "x": 0,
                                                        "y": 0
                                                        },
                                                    "end": {
                                                        "x": 0,
                                                        "y": 0
                                                        },
                                                    "metadata": {}
                                                    }
                                        ]
                                    - a_type = "rect" ["forbidden_area", "elevator_area", "dangerous_area", "coverage_area", "maintenance_area", "sensor_disable_area", "restricted_area"]: Different types of rectangular areas require different metadata. Please refer to the document description.
                                        {
                                                "area": {
                                                    "start": {
                                                        "x": 0,
                                                        "y": 0
                                                        },
                                                    "end": {
                                                        "x": 0,
                                                        "y": 0
                                                        },
                                                    "half_width": 0
                                                    },
                                                "metadata": {
                                                    "escape_distance": "0.4"
                                                    }
                                        }
                                    - a_type = "poi" [None]: The caller should randomly generate a UUID as the id, the display_name in metadata is used for interface display, and the type is used to distinguish the POI type.
                When adding POIs during the map construction process, it is recommended not to include Pose. In this case, the POI will be created with the current position of the robot, and the sensor observation information will be recorded. The posture will be adjusted after the loop is closed.
                                        {
                                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                                "pose": {
                                                    "x": 0,
                                                    "y": 0,
                                                    "yaw": 0
                                                    },
                                                "metadata": {}
                                        }
                                    - a_type = "laser" ["remove"]:
                                        [
                                            0
                                        ]

                        Returns:
                            - True => Add Success
                            - False => Add Failure
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
            if a_usage == "adjust":
                endpoint = "pois/:adjust"
                r_type = Response_Type.EMPTY
            else:
                endpoint = "pois"
                r_type = Response_Type.JSON
        elif a_type == "laser":
            if a_usage == "remove":
                endpoint = "laser-landmarks/:remove"
                r_type = Response_Type.JSON
            else:
                self.__LOGGER.WARNING("Invalid Usage Argument Passed")
                return False
            a_type = "laser-landmarks"
        else:
            self.__LOGGER.WARNING("Invalid Type Argument Passed")
            return False

        response: combined_Result = self.__REST_ADAPTER.post(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/{endpoint}",
            response_type=r_type,
            body_params=dict_value,
        )

        status_code = response.status_code
        if status_code == 200:
            return True
        else:
            return False

    def modify_artifact(
        self,
        a_type: str,
        a_usage: typing.Optional[str] = None,
        id: typing.Optional[str] = None,
        dict_value: typing.Optional[ListDictType] = None,
    ) -> bool | ListDictType:
        """Modify Map Semantic Elements

        Args:
            a_type: Type of Element to Fetch
                - "line" => Modify Virtual Line Segment
                - "poi" => Modify POI
                - "laser" => Setting Up Laser Landmarks
            a_usage:
                - a_type = "lines":
                    - "tracks" => Virtual Track
                    - "walls" => Virtual Wall
                - a_type = "laser":
                    - None => Set the laser landmark information read from the map into Slamware
                    - "update" => Set whether to allow Slamware to automatically update laser landmarks
            dict_value: Data to add to Map
                Examples:
                    - a_type = "lines" ["tracks", "walls"]: When adding, id is an invalid field and can be any value.
                        [
                                {
                                    "id": 0,
                                    "start": {
                                        "x": 0,
                                        "y": 0
                                        },
                                    "end": {
                                        "x": 0,
                                        "y": 0
                                        },
                                    "metadata": {}
                                    }
                        ]
                    - a_type = "poi" [None]: The request message can contain only one of pose and metadata, and the other field remains unchanged.
                        {
                            "pose": {
                                "x": 0,
                                "y": 0,
                                "z": 0,
                                "yaw": 0,
                                "picth": 0,
                                "roll": 0
                                },
                            "metadata": {}
                        }
                    - a_type = "laser":
                        - a_usage = None:
                            Example:
                                [
                                        {
                                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                                            "pose": {
                                                "x": 0,
                                                "y": 0,
                                                "yaw": 0
                                                },
                                            "metadata": {}
                                            }
                                ]
                        - a_usage = "update":
                            Example:
                                {
                                        "enable": true
                                }

            id: ID Value for the parameter to change
                - a_type = "poi": String UUID
                    Example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"



        Returns:
            - True => Modify Success
            - False => Modify Failure
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
        elif a_type == "poi":
            a_type = "pois"
            if id is not None:
                endpoint = f"pois/{id}"
                r_type = Response_Type.JSON
            else:
                return False
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

        response: combined_Result = self.__REST_ADAPTER.put(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/{endpoint}",
            response_type=r_type,
            body_params=dict_value,
        )
        status_code = response.status_code
        if status_code == 200:
            return True
        else:
            return False

    def delete_artifact(
        self,
        a_type: str,
        a_usage: typing.Optional[str] = None,
        id: typing.Optional[int | str] = None,
    ) -> bool | ListDictType:
        """Delete Map Semantic Elements

        Args:
            a_type: Type of Element to Fetch
                - "line" => Delete Virtual Line Segment
                - "rect" => Delete Rectangular Area
                - "poi" => Delete POI
                - "laser" => Delete Laser Landmarks
            a_usage:
                - a_type = "lines":
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
                - a_type = "laser":
                    - None => Clear all laser landmarks
            id: ID Value for the parameter to change
                - a_type = "lines": ["tracks", "walls"]: Int ID
                - a_type = "rect": Int ID
                - a_type = "poi": String UUID
                    Example: "3fa85f64-5717-4562-b3fc-2c963f66afa6"



        Returns:
            - True => Modify Success
            - False => Modify Failure
        """
        self.__LOGGER.INFO(f"Request: Type:{a_type} | Usage:{a_usage} | ID:{id}")
        endpoint = ""
        # Check Input Conditions
        if a_type == "lines":
            if a_usage not in ["tracks", "walls"]:
                self.__LOGGER.WARNING("Invalid Usage Argument Passed")
                return False
            elif id is not None:
                endpoint = f"lines/{a_usage}/{id}"
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
            elif id is not None:
                endpoint = f"rectangle-areas/{a_usage}/{id}"
            else:
                endpoint = f"rectangle-areas/{a_usage}"
            r_type = Response_Type.JSON
        elif a_type == "poi":
            a_type = "pois"
            if id is not None:
                endpoint = f"pois/{id}"
                r_type = Response_Type.JSON
            else:
                endpoint = "pois"
                r_type = Response_Type.JSON
        elif a_type == "laser":
            endpoint = "laser-landmarks"
            r_type = Response_Type.JSON
            a_type = "laser-landmarks"
        else:
            self.__LOGGER.WARNING("Invalid Type Argument Passed")
            return False

        response: combined_Result = self.__REST_ADAPTER.delete(
            full_endpoint=f"{self.__IP_ADDR}/{self.__API_TAG}/{self.__API_VERSION}/{endpoint}",
            response_type=r_type,
        )
        status_code = response.status_code
        if status_code == 200:
            return True
        else:
            return False
