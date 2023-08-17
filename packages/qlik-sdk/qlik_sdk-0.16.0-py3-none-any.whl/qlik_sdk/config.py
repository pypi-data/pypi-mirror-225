from dataclasses import dataclass, field
from typing import List

from .auth_type import AuthType
from .errors import CustomException, CustomExceptionMsg


@dataclass
class Config:
    """Config object"""

    host: str
    """host adress of your tenant"""
    auth_type: AuthType
    """the authentication type"""
    client_id: str = None
    """oauth clientId"""
    client_secret: str = None
    """oauth clientSecret"""
    scope: List[str] = field(default_factory=list)
    """oauth scopes, always includes 'user_default'"""
    redirect_url: str = None
    """oauth redirect destination after successful authorization"""
    api_key: str = None
    """token representing a user in your tenant"""
    refresh_token: str = None
    """token required to fetch new access_token when current access_token expires"""

    def __post_init__(self):
        # Call validate after init
        self.validate()

    def validate(self):
        """
        Validate that the config is correct,
        raises error for incorrect config
        """
        if not self.host:
            raise CustomException(CustomExceptionMsg.EMPTY_HOST.value)
        if not self.auth_type:
            raise CustomException(
                CustomExceptionMsg.MISSING_CONFIG_PROPERTY.value + ": auth_type"
            )
        if self.auth_type == AuthType.APIKey:
            if not self.api_key:
                raise CustomException(
                    CustomExceptionMsg.MISSING_CONFIG_PROPERTY.value + ": api_key"
                )
            allowed_keys = {
                "host",
                "auth_type",
                "api_key",
                "scope",
            }  # scope has default
            for k in self.__dict__.keys():
                if k not in allowed_keys and self.__dict__[k] is not None:
                    raise CustomException(
                        CustomExceptionMsg.UNSUPPORTED_PROPERTY.value + ": " + k
                    )
        elif self.auth_type == AuthType.OAuth2:
            allowed_keys = {
                "host",
                "auth_type",
                "api_key",
                "client_id",
                "client_secret",
                "scope",
                "redirect_url",
                "refresh_token",
            }
            for k in self.__dict__.keys():
                if k not in allowed_keys and self.__dict__[k] is not None:
                    raise CustomException(
                        CustomExceptionMsg.UNSUPPORTED_PROPERTY.value + ": " + k
                    )
            # ensure scopes includes user_default
            if "user_default" not in self.scope:
                self.scope.append("user_default")
            if self.api_key is not None:
                raise CustomException(
                    CustomExceptionMsg.UNSUPPORTED_PROPERTY.value
                    + ": api_key cannot be used with oauth"
                )
            if not self.client_secret and not self.redirect_url:
                raise CustomException(
                    CustomExceptionMsg.MISSING_CONFIG_PROPERTY.value
                    + ": clientSecret or redirectUri"
                )

        else:
            raise CustomException(
                CustomExceptionMsg.UNSUPPORTED_AUTH_TYPE.value
                + ": "
                + str(self.auth_type)
            )
