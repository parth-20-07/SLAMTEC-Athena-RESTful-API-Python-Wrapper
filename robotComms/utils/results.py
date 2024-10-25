import typing


class Result:
    def __init__(
        self,
        status_code: int,
        data: typing.Optional[typing.List[typing.Dict[str, str]]] = None,
    ) -> None:
        """
        Holds the results from HTTP Request

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
        self.status_code = int(status_code)
        self.data = data if data else []
