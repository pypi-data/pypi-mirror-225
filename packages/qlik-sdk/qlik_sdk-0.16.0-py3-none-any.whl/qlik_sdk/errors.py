from enum import Enum


class CustomException(Exception):
    """
    CustomException represents a custom exception
    """


class CustomExceptionMsg(Enum):
    """
    CustomExceptionMsg - messages for custom exceptions
    """

    EMPTY_HOST = "Empty host in config"
    MISSING_CONFIG_PROPERTY = "Missing config property"
    UNSUPPORTED_AUTH_TYPE = "Unsupported authType"
    UNSUPPORTED_PROPERTY = "Unsupported property"
    NOT_IMPLEMENTED = "Not implemented"


class AuthorizeException(CustomException):
    error: str
    error_code: str
    error_description: str
    error_detail: str
    error_uri: str

    def __init__(self, *args: object) -> None:
        self.error = None
        self.error_code = None
        self.error_description = None
        self.error_detail = None
        self.error_uri = None
        super().__init__(*args)
        for a in args:
            for key in self.__dict__.keys():
                if key in a:
                    setattr(self, key, a[key])


class EngineClosedException(Exception):
    close_code: str
    close_msg: str

    def __init__(self, *args: object) -> None:
        self.close_code = None
        self.close_msg = None
        super().__init__(*args)
        for a in args:
            for key in self.__dict__.keys():
                if key in a:
                    setattr(self, key, a[key])
