import json
from asyncio import Future
from typing import Any, Awaitable, Callable, cast, Dict, List, Optional, Union

from tornado import httpclient, httputil
from tornado.ioloop import IOLoop
from tornado.netutil import Resolver
from tornado.websocket import WebSocketClientConnection

from .schema import (
    ContentType,
    MessageHeader,
    MessageReceiver,
    LoginInfo,
    LoginResponse,
    PackageType,
    ReconnectResponse,
    Segment,
    ServerEndConnection
)


class MstpSocketClientConnection(WebSocketClientConnection):

    def __init__(
        self,
        request: httpclient.HTTPRequest,
        secret: str,
        on_message_callback: Optional[
            Callable[[Union[None, str, bytes]], None]] = None,
        compression_options: Optional[Dict[str, Any]] = None,
        ping_interval: Optional[float] = None,
        ping_timeout: Optional[float] = None,
        max_message_size: int = 10 * 1024 * 1024,
        subprotocols: Optional[List[str]] = [],
        resolver: Optional[Resolver] = None,
    ) -> None:
        super().__init__(
            request,
            on_message_callback=on_message_callback,
            compression_options=compression_options,
            ping_interval=ping_interval,
            ping_timeout=ping_timeout,
            max_message_size=max_message_size,
            subprotocols=subprotocols,
            resolver=resolver
        )
        self.secret = secret

    async def on_message(self, message: Union[str, bytes]) -> Optional[Awaitable[None]]:
        print(message)
        pkg = json.loads(message)
        package_type = pkg.get("package_type")
        match package_type:
            case PackageType.SERVER_INFO:
                await self.write_message(
                    LoginInfo(
                        secret=self.secret
                    ).model_dump_json(exclude_none=True)
                )
            case PackageType.LOGIN_RESPONSE:
                login_response = LoginResponse(**pkg)
                await self.handle_login_response(
                    status=login_response.status,
                    connection_interval=login_response.connection_interval,
                    session_alive_time=login_response.session_alive_time,
                    session_id=login_response.session_id,
                    reason=login_response.reason
                )
            case PackageType.RECONNECT_RESPONSE:
                reconnect_response = ReconnectResponse(**pkg)
                await self.handle_reconnect_response(
                    status=reconnect_response.status,
                    reason=reconnect_response.reason
                )
            case PackageType.MESSAGE_HEADER:
                message_header = MessageHeader(**pkg)
                await self.handle_message_header(
                    package_id=message_header.package_id,
                    message_index=message_header.message_index,
                    receiver=message_header.receiver
                )
            case PackageType.SEGMENT:
                segment = Segment(**pkg)
                await self.handle_segment(
                    package_id=segment.package_id,
                    message_index=segment.message_index,
                    segment_index=segment.segment_index,
                    is_end=segment.is_end,
                    content_type=segment.content_type,
                    content=segment.content
                )
            case PackageType.SERVER_END_CONNECTION:
                server_end = ServerEndConnection(**pkg)
                await self.handle_server_end_connection(reason=server_end.reason)
            case _:
                pass  # Do nothing
        return super().on_message(message)  # TODO: check if it's necessary

    async def handle_login_response(
        self,
        *,
        status: Optional[bool] = None,
        connection_interval: Optional[int] = None,
        session_alive_time: Optional[int] = None,
        session_id: Optional[str] = None,
        reason: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    async def handle_reconnect_response(
        self,
        *,
        status: Optional[bool] = None,
        reason: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    async def handle_message_header(
        self,
        *,
        package_id: Optional[str] = None,
        message_index: Optional[int] = None,
        receiver: Optional[MessageReceiver] = None
    ) -> None:
        raise NotImplementedError

    async def handle_segment(
        self,
        package_id: Optional[str] = None,
        message_index: Optional[int] = None,
        segment_index: Optional[int] = None,
        is_end: Optional[bool] = None,
        content_type: Optional[ContentType] = None,
        content: Optional[str] = None
    ) -> None:
        raise NotImplementedError

    async def handle_server_end_connection(
        self,
        *,
        reason: Optional[str] = None
    ) -> None:
        raise NotImplementedError


def mstpsocket_connect(
    url: Union[str, httpclient.HTTPRequest],
    secret: str,
    connection_class: Optional[type[MstpSocketClientConnection]] = None,
    callback: Optional[Callable[["Future[WebSocketClientConnection]"], None]] = None,
    connect_timeout: Optional[float] = None,
    on_message_callback: Optional[Callable[[Union[None, str, bytes]], None]] = None,
    compression_options: Optional[Dict[str, Any]] = None,
    ping_interval: Optional[float] = None,
    ping_timeout: Optional[float] = None,
    max_message_size: int = 10 * 1024 * 1024,
    subprotocols: Optional[List[str]] = None,
    resolver: Optional[Resolver] = None,
) -> "Awaitable[WebSocketClientConnection]":
    scheme, sep, rest = url.partition(":")
    scheme = {"mstp": "ws", "mstps": "wss"}[scheme]
    ws_url = scheme + sep + rest

    if isinstance(ws_url, httpclient.HTTPRequest):
        assert connect_timeout is None
        request = ws_url
        # Copy and convert the headers dict/object (see comments in
        # AsyncHTTPClient.fetch)
        request.headers = httputil.HTTPHeaders(request.headers)
    else:
        request = httpclient.HTTPRequest(ws_url, connect_timeout=connect_timeout)
    request = cast(
        httpclient.HTTPRequest,
        httpclient._RequestProxy(request, httpclient.HTTPRequest._DEFAULTS),
    )
    conn = connection_class(
        request,
        secret,
        on_message_callback=on_message_callback,
        compression_options=compression_options,
        ping_interval=ping_interval,
        ping_timeout=ping_timeout,
        max_message_size=max_message_size,
        subprotocols=subprotocols,
        resolver=resolver,
    )
    if callback is not None:
        IOLoop.current().add_future(conn.connect_future, callback)
    return conn.connect_future
