import base64
import enum
import platform
from dataclasses import dataclass
from functools import reduce
from typing import Callable

import requests

from ._version import __version__
from .auth_type import AuthType
from .config import Config
from .interceptors.types import InterceptorHandler, Interceptors


class HTTPMethods(enum.Enum):
    "GET",
    "OPTIONS",
    "HEAD",
    "POST",
    "PUT",
    "PATCH",
    "DELETE"


class NoUrlException(Exception):
    """
    NoUrlException represents a missing URL
    """


class ConnectionException(Exception):
    """
    ConnectionException represents a failure in the request
    The request raised an exception
    ConnectionException is not a 4xx response
    """


class AuthenticationException(Exception):
    """
    AuthenticationException represents a failure to authenticate
    """


def _get_dict(o: any) -> dict:
    """
    get_dict attempts to convert objects to dict, nested
    """
    try:
        if isinstance(o, dict):
            d = o
        else:
            d = o.__dict__
        d2 = {}
        for k in d:
            if d[k] is not None:
                d2[k] = _get_dict(d[k])
        return d2
    except Exception:
        return o


RequestInterceptor = Callable[[requests.Request], requests.Request]
""" REST Request interceptor """
ResponseInterceptor = Callable[[requests.Response], requests.Response]
""" REST Request interceptor """


@dataclass
class RestClient:
    """
    RestClient represents a rest client for making api calls
    """

    config: Config
    base_url: str
    _interceptors: Interceptors[ResponseInterceptor, RequestInterceptor] = None

    def __init__(self, config) -> None:
        self.config = config
        self.base_url = config.host
        self._interceptors = dict(
            request=InterceptorHandler[RequestInterceptor](),
            response=InterceptorHandler[ResponseInterceptor](),
        )

    def rest(
        self,
        path: str,
        method: HTTPMethods = "GET",
        data=None,
        files=None,
        params: dict = None,
        headers: dict = None,
        stream: bool = False,
        timeout: int = 10,
    ) -> requests.Response:
        """
        rest sends a request
        """
        if not self.base_url:
            raise NoUrlException("Caller has no 'base_url'")
        if not path.lower().startswith("http://") and not path.lower().startswith(
            "https://"
        ):
            exclude_v1_api_list = [
                "/api/v1",
                "/login/jwt-session",
                "/oauth/token",
                "/oauth/authorize",
                "/oauth/revoke",
            ]
            should_add_prefix = any(
                path.lower().startswith(value) for value in exclude_v1_api_list
            )
            path = f"{ '/api/v1' if not should_add_prefix else ''}{path}"
        else:
            path = path.split(self.base_url)[1]
        if headers is None:
            headers = {}
        # Add authorization depending upon type of auth flow
        if self.config.auth_type == AuthType.APIKey:
            headers["authorization"] = "Bearer " + self.config.api_key
        elif self.config.auth_type == AuthType.OAuth2:
            if self.config.client_secret and path == "/oauth/token":
                client_str = self.config.client_id + ":" + self.config.client_secret
                b64Val = base64.b64encode(bytes(client_str, "utf-8"))
                headers["authorization"] = "Basic " + b64Val.decode("utf-8")
            elif self.config.client_secret:
                headers["authorization"] = "Bearer " + self.config.api_key
        # Add user-agent
        # version without v in user-agent
        # consistent with format of version in qlik-cli-user-agent
        version = __version__[1:]
        os_name = platform.system()
        headers["User-Agent"] = f"qlik-sdk-python/{version} ({os_name})"
        # If the data can be converted to a dict then send
        # it as json, otherwise send it as data.
        json_data = None
        if data and not isinstance(data, bytes):
            json_data = _get_dict(data)
            if json_data:
                data = None
        if params:
            params = _get_dict(params)
        # Create request.
        req = requests.Request(
            method,
            self.base_url.strip("/") + path,
            data=data,
            json=json_data,
            files=files,
            headers=headers,
            params=params,
        )

        req = reduce(lambda d, f: f(d), self._interceptors["request"].handlers, req)
        with requests.Session() as session:
            prepared = req.prepare()
            try:
                res = session.send(
                    prepared,
                    timeout=timeout,
                    stream=stream,
                )
            except requests.exceptions.Timeout:
                raise ConnectionException("Connection Timeout: " + self.base_url)
            except requests.exceptions.RequestException as exc:
                raise ConnectionException("Connection Error: " + self.base_url) from exc

            res = reduce(
                lambda r, f: f(r), self._interceptors["response"].handlers, res
            )

            try:
                res.raise_for_status()
            except Exception as e:
                res.close()
                if res.status_code == 401:
                    error = "Failed to authenticate"
                    try:
                        error = res.json()["errors"][0]["title"]
                    except Exception:
                        pass
                    raise AuthenticationException(error)
                raise e

            return res


class RestClientInstance:
    interceptors: Interceptors[ResponseInterceptor, RequestInterceptor]

    def __init__(self, restClient: RestClient) -> None:
        self._restClient = restClient
        self.interceptors = restClient._interceptors

    def __call__(self, **all: requests.Request) -> requests.Response:
        return self._restClient.rest(**all)
