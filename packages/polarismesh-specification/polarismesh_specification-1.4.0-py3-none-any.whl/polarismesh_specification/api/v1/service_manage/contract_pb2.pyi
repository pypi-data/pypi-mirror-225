from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceContract(_message.Message):
    __slots__ = ["name", "namespace", "service", "protocol", "version", "revision", "content", "interfaces", "ctime", "mtime"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    INTERFACES_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    name: str
    namespace: str
    service: str
    protocol: str
    version: str
    revision: str
    content: str
    interfaces: _containers.RepeatedCompositeFieldContainer[InterfaceDescriptor]
    ctime: str
    mtime: str
    def __init__(self, name: _Optional[str] = ..., namespace: _Optional[str] = ..., service: _Optional[str] = ..., protocol: _Optional[str] = ..., version: _Optional[str] = ..., revision: _Optional[str] = ..., content: _Optional[str] = ..., interfaces: _Optional[_Iterable[_Union[InterfaceDescriptor, _Mapping]]] = ..., ctime: _Optional[str] = ..., mtime: _Optional[str] = ...) -> None: ...

class InterfaceDescriptor(_message.Message):
    __slots__ = ["method", "path", "content", "revision", "ctime", "mtime"]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    method: str
    path: str
    content: str
    revision: str
    ctime: str
    mtime: str
    def __init__(self, method: _Optional[str] = ..., path: _Optional[str] = ..., content: _Optional[str] = ..., revision: _Optional[str] = ..., ctime: _Optional[str] = ..., mtime: _Optional[str] = ...) -> None: ...
