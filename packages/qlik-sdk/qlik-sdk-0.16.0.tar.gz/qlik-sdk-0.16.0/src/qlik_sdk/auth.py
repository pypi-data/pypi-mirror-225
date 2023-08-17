from urllib.parse import parse_qs, urlparse

from .auth_type import AuthType
from .config import Config
from .errors import AuthorizeException, CustomException
from .oauth_utils import _generate_authorization_url
from .rest import RestClient, RestClientInstance
from .rpc import RpcClient, RpcClientInstance


class Auth:
    """
    Auth can be used to make rest and rpc calls

    Parameters
    ----------
    config: Config
        the required configuration object

    Examples
    --------
    >>> from qlik_sdk import Auth, AuthType, Config
    ...
    ... clients = Auth(Config(host=base_url, auth_type=AuthType.APIKey, api_key=api_key))
    ... get_users_res = clients.rest(path="/users/me")
    """

    config: Config
    rest: RestClientInstance
    """
    rest method can be used to make raw calls against Qlik Cloud

    Parameters
    ----------
    method: str, default GET
        string HTTP verb
    path: str
        representing the api endpoint ex: `/users/me`
    data: dict, optional
        Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
    params: dict, optional
        Dictionary, list of tuples or bytes to send in the query string for the Request.
    files: dict, optional
        Dictionary of {filename: fileobject} files to multipart upload.
    headers: dict, optional
        Dictionary of HTTP Headers to send with the Request
    stream: bool, optional, default True
        if False, the response content will be immediately downloaded.
    timeout: int optional, default 10
        How many seconds to wait for the server to send data before giving up

    Attributes
    ----------
    interceptors: Interceptors

    Examples
    ----------
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... user_me = auth.rest(path="/users/me")
    ...
    # And with interceptors.
    >>> auth = Auth(Config(host=self.base_url, auth_type=AuthType.APIKey, api_key=self.api_key))
    ... def log_req(req: requests.Request) -> requests.Request:
    ...     print(req)
    ...     return req
    ...
    ... auth.rpc.interceptors["request"].use(log_req)
    ... app_list = auth.rest(path="/items", params={"resourceType":"app", "limit": 100})
    """

    rpc: RpcClientInstance
    """
    rpc returns an RpcClient that can be used to
    connect to the engine for a specific app

    Parameters
    ----------
    app_id: str

    Attributes
    ----------
    interceptors: Interceptors

    Examples
    ----------
    >>> rpc_session = auth.rpc(app_id=session_app_id)
    ... with rpc_session.opn() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    ...
    # And with interceptors.
    >>> auth.rpc.interceptors["request"].use(log_req)
    ... rpc_session = auth.rpc(app_id=session_app_id)
    ...
    ... with rpc_session.open() as rpc_client:
    ...     app = rpc_client.send("OpenDoc", -1, session_app_id)
    """

    code_verifier: str = None
    """oauth code verifier"""
    state: str = None
    """oauth state"""

    def __init__(self, config: Config):
        config.validate()
        self.config = config
        self.rest = RestClientInstance(RestClient(config))
        self.rpc_client = RpcClient(self.config)
        self.rpc = RpcClientInstance(self.rpc_client)

    def generate_authorization_url(self, state: str = None) -> str:
        """
        method helper for generating the authorization url in OAuth flows based on the Config

        Parameters
        ----------
        state: str, optional
            the state parameter is a random generated string used for validating against
            potential CSRF attacks

        Examples
        ----------
        >>> auth = Auth(Config(
        ...     host=host,
        ...     auth_type = AuthType.OAuth2,
        ...     client_id = <...>,
        ...     client_secret = <...>,
        ...     redirect_url = <...>))
        ...
        ... auth_url = auth.generate_authorization_url()
        ... webbrowser.get('chrome').open(url)
        """
        data = _generate_authorization_url(self.config, state, True)
        self.code_verifier = data["code_verifier"]
        self.state = data["state"]
        return data["url"]

    def authorize(self, url: str = None) -> None:
        """
        exchange credentials with token against the authorization server

        Parameters
        ----------
        url: str, optional
            The callback url with query parameters
        """
        code = None
        state = None
        error = None
        query = None
        if url is not None:
            try:
                query = parse_qs(urlparse(url).query)
            except:
                pass
        if query is not None:
            if "code" in query and len(query["code"]) > 0:
                code = query["code"][0]
            if "state" in query and len(query["state"]) > 0:
                state = query["state"][0]
            if "error" in query and len(query["error"]) > 0:
                error = query["error"][0]

        if error is not None:
            error_dict = {}
            for key in [
                "error",
                "error_code",
                "error_description",
                "error_detail",
                "error_uri",
            ]:
                val = query.get(key, None)
                if val is not None:
                    error_dict[key] = val[0]
                else:
                    error_dict[key] = None
            raise AuthorizeException(error_dict)
        if self.state is not None and state != self.state:
            raise CustomException(
                "The received state parameter does not match the original state value"
            )
        params = {
            "grant_type": "client_credentials",
            "scope": " ".join(self.config.scope),
        }
        if code is not None:
            params["code"] = code
            params["grant_type"] = "authorization_code"
            params["code_verifier"] = self.code_verifier
            params["client_id"] = self.config.client_id
        if self.config.redirect_url is not None and self.config.redirect_url != "":
            params["redirect_uri"] = self.config.redirect_url
        resp = self.rest(path="/oauth/token", method="post", data=params)
        resp = resp.json()
        self.config.api_key = resp["access_token"]
        if "refresh_token" in resp:
            self.config.refresh_token = resp["refresh_token"]
        # return response from /oauth/token
        return resp

    def refresh_token(self) -> None:
        """
        Requesting new access_token using refresh token on expiry of current access_token
        """
        if (
            self.config.auth_type != AuthType.OAuth2
            or "offline_access" not in self.config.scope
            or not self.config.refresh_token
        ):
            raise CustomException(
                "Method only available for AuthType OAuth2, that have offline_access scope"
            )
        params = {
            "grant_type": "refresh_token",
            "refresh_token": self.config.refresh_token,
        }
        resp = self.rest(path="/oauth/token", method="post", data=params, headers={})
        resp = resp.json()
        self.config.api_key = resp["access_token"]
        self.config.refresh_token = resp["refresh_token"]

    def deauthorize(self) -> None:
        """
        deauthorize
        revokes the Auth instance oauth token
        """
        body = {"token": self.config.api_key, "token_type_hint": "access_token"}
        self.rest(path="/oauth/revoke", method="post", data=body)
        self.config.api_key = ""
        self.config.refresh_token = ""
