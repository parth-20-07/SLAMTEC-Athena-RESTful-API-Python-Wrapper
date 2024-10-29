import typing
from enum import Enum


##############################################################################################################
# Result Formats for Public Use. These are just alias for longer names
##############################################################################################################
ListDictType = typing.List[typing.Dict[str, typing.Any]]
DictType = typing.Dict[str, typing.Any]
StrType = str
CombinedType = ListDictType | DictType | StrType


##############################################################################################################
# Result Classes for internal Use
##############################################################################################################
class list_Result:
    def __init__(
        self,
        status_code: int,
        data: typing.Optional[ListDictType] = None,
    ) -> None:
        """
        Holds the List of Dictionary results from HTTP Request

        Args:
            status_code: Status Code from the HTTP Request
            - 200 (OK) -> indicates that any operation requested by the Client was successfully performed.
            - 204 (no content) -> indicates that the server has successfully completed the request and there is no content to send in the response payload body.
            - 400 (Bad Request) -> Generic Client error state, used when there are no other 4xx error codes.
            - 404 (Not Found) -> The URI resource requested by the REST API could not be found.
            - 500 -> Server Internal Error

            data: Contains the Results from the REST Request.
            - Returns a List of Dictionary for 200 Status Code
            - Returns an empty list in case of 204/4xx/500 status code.
        """
        self.status_code: int = int(status_code)
        self.data: ListDictType = data if data else []


class dict_Result:
    def __init__(
        self,
        status_code: int,
        data: typing.Optional[DictType] = None,
    ) -> None:
        """
        Holds the Dictionary results from HTTP Request

        Args:
            status_code: Status Code from the HTTP Request
            - 200 (OK) -> indicates that any operation requested by the Client was successfully performed.
            - 204 (no content) -> indicates that the server has successfully completed the request and there is no content to send in the response payload body.
            - 400 (Bad Request) -> Generic Client error state, used when there are no other 4xx error codes.
            - 404 (Not Found) -> The URI resource requested by the REST API could not be found.
            - 500 -> Server Internal Error

            data: Contains the Results from the REST Request.
            - Returns a Dictionary for 200 Status Code
            - Returns an empty Dictionary in case of 204/4xx/500 status code.
        """
        self.status_code: int = int(status_code)
        self.data: DictType = data if data else {}


class str_Result:
    def __init__(
        self,
        status_code: int,
        data: typing.Optional[StrType] = None,
    ) -> None:
        """
        Holds the String results from HTTP Request

        Args:
            status_code: Status Code from the HTTP Request
            - 200 (OK) -> indicates that any operation requested by the Client was successfully performed.
            - 204 (no content) -> indicates that the server has successfully completed the request and there is no content to send in the response payload body.
            - 400 (Bad Request) -> Generic Client error state, used when there are no other 4xx error codes.
            - 404 (Not Found) -> The URI resource requested by the REST API could not be found.
            - 500 -> Server Internal Error

            data: Contains the Results from the REST Request.
            - Returns a String for 200 Status Code
            - Returns an empty String in case of 204/4xx/500 status code.
        """
        self.status_code: int = int(status_code)
        self.data: StrType = data if data else ""


combined_Result = list_Result | dict_Result | str_Result


##############################################################################################################
# Response Media Type
##############################################################################################################
class Response_Type(Enum):
    LIST_JSON = 1
    JSON = 1
    STR = 2
