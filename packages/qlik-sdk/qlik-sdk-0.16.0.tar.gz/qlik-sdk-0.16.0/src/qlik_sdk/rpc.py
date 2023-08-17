import json
import struct
from dataclasses import dataclass
from functools import reduce
from threading import Condition, Lock, Thread
from typing import Callable, Dict, List, Literal
from urllib.parse import urlparse

import websocket

from ._version import __version__
from .config import Config
from .errors import EngineClosedException
from .interceptors.types import InterceptorHandler, Interceptors


def _get_json_data(x: any):
    """
    Get all the properties of a class as plain data.
    Similar to the asdict function but including dynamic properties.
    Excludes _session property
    """
    dict_data = None
    try:
        # get the __dict__ of the object
        # includes named and dynamic properties
        dict_data = x.__dict__
    except:
        if type(x) is dict:
            dict_data = x
    if dict_data is not None:
        dct = {}
        for k, v in dict_data.items():
            # exclude the private _session property
            if k != "_session":
                dct[k] = _get_json_data(v)
        return dct
    elif type(x) is list:
        return [_get_json_data(e) for e in x]
    return x


@dataclass
class RequestObject:
    # Identifier established by the initiator of the request
    id: int
    # name of the engine method.
    method: str
    # target of the method.
    handle: int
    # the parameters can be provided by name through an object or by position through an array
    params: any
    # version of JSON-RPC defaults to 2.0
    jsonrpc: str = "2.0"


@dataclass
class ResponseObject:
    # id of the backend object.
    id: int
    #  QIX type of the backend object. Can for example be "Doc" or "GenericVariable".
    type: str
    # Custom type of the backend object, if defined in qInfo.
    genericType: str
    # Handle of the backend object.
    handle: int
    # represents the returned value from engine
    result: dict


RequestInterceptor = Callable[[RequestObject], RequestObject]
""" RPC Request interceptor """
ResponseInterceptor = Callable[[dict], dict]
""" RPC Request interceptor """


class FailedToConnect(Exception):
    pass


class RpcSession:
    _interceptors: Interceptors[ResponseInterceptor, RequestInterceptor]

    _ws_url: str
    _headers: List[str]
    _recv_error: Exception
    _socket = None
    _watch_recv_thread = None

    def __init__(
        self, ws_url: str, headers: List[str] = None, interceptors: Interceptors = None
    ):
        if headers is None:
            headers = []
        if not ws_url:
            raise Exception("Empty url")
        self._headers = headers
        self._ws_url = ws_url
        self._interceptors = interceptors
        self.lock = Lock()
        self._listeners = {}
        self._id_listeners = {}
        self._recv_error = None

    def _emit(self, event, *args):
        if event in self._listeners:
            self._listeners[event](*args)
        if event == "closed":
            # call all the event closed listeners on all objects of session
            for handle in self._id_listeners:
                if "closed" in self._id_listeners[handle]:
                    for closed_listener in self._id_listeners[handle]["closed"]:
                        closed_listener(*args)
            # clear all listeners if session is closed
            self._listeners = {}
            self._id_listeners = {}

    def _emit_handle(self, handle, event, *args):
        if handle in self._id_listeners and event in self._id_listeners[handle]:
            for event_listener in self._id_listeners[handle][event]:
                event_listener(*args)
        if event == "closed":
            # clear all listeners if handle is closed
            self._clear_listeners(handle)

    def _emit_handles(self, handles, event, *args):
        for id in handles:
            self._emit_handle(id, event, *args)

    def _watch_recv(self):
        """
        _watch_recv watches for socket responses.
        Adds the response to _received.
        """

        while True:
            if not self.is_connected():
                return
            try:
                # Using code from the websocket-library documentation for receiving connection close status code
                # https://websocket-client.readthedocs.io/en/latest/examples.html#receiving-connection-close-status-codes
                resp_opcode, msg = self._socket.recv_data()
                if resp_opcode == 8 and len(msg) >= 2:
                    close_code = str(struct.unpack("!H", msg[0:2])[0])
                    close_msg = str(msg[2:])
                    self._socket = None
                    msg = False
                    # Assume that only close code >= 4000 is error
                    if int(close_code) >= 4000:
                        # Setting socket to None signals not connected which will close this thread
                        # The error will be thrown in the close function not in this thread because then
                        # it will not reach the caller
                        self._recv_error = EngineClosedException(
                            {"close_code": close_code, "close_msg": close_msg}
                        )
            except Exception as err:
                self._socket = None
                msg = False
                self._recv_error = err
            with self._received_added:
                if msg:
                    msg = json.loads(msg)
                    self._emit("traffic:*", "received", msg)
                    self._emit("traffic:received", msg)
                    # add response to _received and notify waiting
                    if "id" in msg:
                        self._received[msg["id"]] = msg
                        self._emit("message", msg)
                        self._emit_handle(msg["id"], "traffic:*", "received", msg)
                        self._emit_handle(msg["id"], "traffic:received", msg)
                        self._received_added.notify_all()
                    else:
                        self._emit(
                            "notification" if "params" in msg else "message", msg
                        )
                    if "change" in msg:
                        self._emit_handles(msg["change"], "changed")
                    if "close" in msg:
                        self._emit_handles(msg["close"], "closed")
                else:
                    # notify waiting receivers so that
                    # the not connected error can be raised
                    # if the error is raised from here then the
                    # wait_response will never finish
                    self._received_added.notify_all()

    def on(
        self,
        event_name: Literal[
            "traffic:*",
            "traffic:received",
            "traffic:sent",
            "closed",
            "opened",
            "notification",
            "message",
        ],
        listener: Callable[[any], None],
    ):
        """
        the on function handles the various states and communication events

        Parameters
        ----------
        event_name: str
            can be one of
            'traffic', 'traffic:received','traffic:sent',
            'closed', 'opened',
            'notification', 'message'

        Examples
        --------
        >>> from qlik_sdk import Auth, AuthType, Config
        ...
        ... rpc_session.on("closed", closed_listener)
        ... rpc_session.on("opened", opened_listener)
        ... with rpc_session.open() as rpc_client:
        ...     # ...
        """
        self._listeners[event_name] = listener

    def on_handle(self, handle, event_name, listener):
        if handle not in self._id_listeners:
            self._id_listeners[handle] = {event_name: [listener]}
        else:
            if event_name not in self._id_listeners[handle]:
                self._id_listeners[handle][event_name] = [listener]
            else:
                self._id_listeners[handle][event_name].append(listener)

    def _clear_listeners(self, handle):
        if handle in self._id_listeners:
            self._id_listeners[handle] = {}

    def open(self):
        """
        connect establishes a connection to provided url
        using the specified headers.

        If the client is already connected an exception will
        be raised.
        """
        if self.is_connected():
            raise Exception("Client already connected")
        socket = websocket.WebSocket()
        try:
            socket.connect(self._ws_url, header=self._headers, suppress_origin=True)
        except Exception as exc:
            raise FailedToConnect() from exc

        self._socket = socket
        self._received = {}
        self._id = -1
        self._received_added = Condition()

        self._watch_recv_thread = Thread(target=self._watch_recv)
        self._watch_recv_thread.start()
        self._emit("opened")
        return self

    def is_connected(self):
        """
        return connected state
        """
        return self._socket and self._socket.connected

    def close(self):
        """
        close closes the socket (if it's open).
        """

        if self.is_connected():
            self._socket.send_close()
            self._emit("closed")
        if self._watch_recv_thread is not None and self._watch_recv_thread.is_alive():
            self._watch_recv_thread.join()

        # Raise closed connection error here
        if self._recv_error:
            raise self._recv_error

    def __enter__(self):
        """
        __enter__ is called when client is used in a 'with' statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        __exit__ is called when the 'with' scope is exited. This will call
        the client's close method.
        """

        self.close()

    def send(self, method: str, handle: int, *args, **kwargs):
        """
        send is a thread-safe method that sends a websocket-message with the
        specified method, handle and parameters.
        The resulting response is returned.

        If the client isn't connected an exception is raised.

        Parameters
        ----------
        method: str
            engine method name for the request
        handle: int
            the associated handle
        args: tuple
            parameters by position in an array
        kwargs: dict
            parameters provided by name in an object
        """

        if not self.is_connected():
            raise Exception("Client not connected")

        self.lock.acquire()
        self._id += 1
        id_ = self._id
        self.lock.release()

        data = RequestObject(
            id=self._id,
            method=method,
            handle=handle,
            params=args if not kwargs else kwargs,
        )

        # send and wait respons
        data = reduce(lambda d, f: f(d), self._interceptors["request"].handlers, data)
        json_data = json.dumps(_get_json_data(data))
        self._socket.send(json_data)
        self._emit("traffic:*", "sent", data)
        self._emit("traffic:sent", data)
        self._emit_handle(handle, "traffic:*", "sent", data)
        self._emit_handle(handle, "traffic:sent", data)
        res = self._wait_response(id_)
        res["request_data"] = data
        res = reduce(lambda r, f: f(r), self._interceptors["response"].handlers, res)
        return_value = None
        if "result" in res:
            return_value = res["result"]
        elif "error" in res:
            raise Exception(res["error"]["message"])
        else:
            return_value = res
        return return_value

    def _wait_response(self, id_):
        """
        _wait_response waits (blocking) for a message with the specified id.
        Internal method that should only be called from send
        """

        with self._received_added:
            while id_ not in self._received:
                if not self.is_connected():
                    if self._recv_error:
                        raise self._recv_error
                    else:
                        raise Exception("not connected")
                self._received_added.wait()
            res = self._received[id_]
            del self._received[id_]
            return res


class RpcClient:
    __config: Config
    # property for storing the interceptors
    interceptors: Interceptors[ResponseInterceptor, RequestInterceptor]

    sessions: Dict[str, RpcSession] = {}

    def __init__(self, config) -> None:
        self.__config = config
        # initiating the interceptors
        self.interceptors = dict(
            request=InterceptorHandler[RequestInterceptor](),
            response=InterceptorHandler[ResponseInterceptor](),
        )

    def rpc(self, app_id: str) -> RpcSession:
        hostname = urlparse(self.__config.host).hostname
        ws_url = "wss://" + hostname.strip("/") + "/app/" + app_id
        version = __version__[1:]
        headers = [
            "Authorization: Bearer %s" % self.__config.api_key,
            f"User-Agent: qlik-sdk-python/{version}",
        ]
        if ws_url not in self.sessions:
            self.sessions[ws_url] = RpcSession(ws_url, headers, self.interceptors)
        return self.sessions[ws_url]


class RpcClientInstance:
    interceptors: Interceptors

    def __init__(self, rpcClient: RpcClient) -> None:
        self._rpcClient = rpcClient
        self.interceptors = rpcClient.interceptors

    def __call__(self, app_id: str) -> RpcSession:
        return self._rpcClient.rpc(app_id)
