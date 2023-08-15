from enum import StrEnum
from typing import Optional

from pydantic import BaseModel


class PackageType(StrEnum):
    SERVER_INFO = "server_info"
    LOGIN_INFO = "login_info"
    LOGIN_RESPONSE = "login_response"
    RECONNECT = "reconnect"
    RECONNECT_RESPONSE = "reconnect_response"
    MESSAGE_HEADER = "message_header"
    SEGMENT = "segment"
    ACK = "ack"
    CLIENT_END_CONNECTION = "client_end_connection"
    SERVER_END_CONNECTION = "server_end_connection"


class ContentType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    WEB = "web"
    JSON = "json"
    CODE = "code"


class MessageReceiver(StrEnum):
    AGENT = "agent"
    USER = "user"


class _BasePackage(BaseModel):

    class Config:
        extra = "allow"


class ServerInfo(_BasePackage):
    package_type: Optional[PackageType] = PackageType.SERVER_INFO
    automatic_closing_time: Optional[int] = None  # connection closing time before login
    ver: Optional[str] = None  # MSTP version number


class Ack(_BasePackage):
    package_type: Optional[PackageType] = PackageType.ACK
    package_id: Optional[str] = None


class LoginInfo(_BasePackage):
    package_type: Optional[PackageType] = PackageType.LOGIN_INFO
    secret: Optional[str] = None  # a pre-defined 32-chars


class LoginResponse(_BasePackage):
    package_type: Optional[PackageType] = PackageType.LOGIN_RESPONSE
    status: Optional[bool] = None  # login status, success or fail
    connection_interval: Optional[int] = None  # connection closing time
    session_alive_time: Optional[int] = None  # session automatic closing time
    session_id: Optional[str] = None  # session ID, a random 32-chars sequence originate by server to indicate this session
    reason: Optional[str] = None  # login fail reason: invalid secret/too many attampts/...


class Reconnect(_BasePackage):
    package_type: Optional[PackageType] = PackageType.RECONNECT
    session_id: Optional[str] = None


class ReconnectResponse(_BasePackage):
    package_type: Optional[PackageType] = PackageType.RECONNECT_RESPONSE
    status: Optional[bool] = None  # reconnect status, success or fail
    reason: Optional[str] = None  # reconnect fail reason: this channel is not expired/invalid session id/...


class MessageHeader(_BasePackage):
    package_type: Optional[PackageType] = PackageType.MESSAGE_HEADER
    package_id: str
    message_index: Optional[int] = None  # indicate the index of this message
    receiver: Optional[MessageReceiver] = None  # agent/user


class Segment(_BasePackage):
    package_type: Optional[PackageType] = PackageType.SEGMENT
    package_id: Optional[str] = None
    message_index: Optional[int] = None  # indicate the index of this message
    segment_index: Optional[int] = None  # indicate the order of this segment in the current message
    is_end: Optional[bool] = None  # indicate if this segment is the end of the current message
    content_type: Optional[ContentType] = None  # segment content_type
    content: Optional[str] = None  # text, http address for image audio video and web


class ClientEndConnection(_BasePackage):
    package_type: Optional[PackageType] = PackageType.CLIENT_END_CONNECTION
    reason: Optional[str] = None  # user logout/not appropriate answer/...


class ServerEndConnection(_BasePackage):
    package_type: Optional[PackageType] = PackageType.SERVER_END_CONNECTION
    reason: Optional[str] = None  # server will close/session expired/...
