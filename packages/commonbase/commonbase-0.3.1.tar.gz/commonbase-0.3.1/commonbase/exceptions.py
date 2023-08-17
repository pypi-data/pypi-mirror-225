class CommonbaseApiException(Exception):
    def __init__(self, json: dict) -> None:
        self.response = json
        super().__init__(json["error"] if "error" in json else "Commonbase Error")


class CommonbaseException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
