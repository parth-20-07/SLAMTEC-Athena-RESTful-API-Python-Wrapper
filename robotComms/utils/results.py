import typing


class Result:
    def __init__(
        self,
        status_code: int,
        data: typing.Optional[typing.List[typing.Dict[str, str]]] = None,
    ) -> None:
        self.status_code = int(status_code)
        self.data = data if data else []
