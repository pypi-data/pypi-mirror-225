from ..service_manage import service_pb2 as _service_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiscoverRequest(_message.Message):
    __slots__ = ["type", "service"]
    class DiscoverRequestType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[DiscoverRequest.DiscoverRequestType]
        INSTANCE: _ClassVar[DiscoverRequest.DiscoverRequestType]
        CLUSTER: _ClassVar[DiscoverRequest.DiscoverRequestType]
        ROUTING: _ClassVar[DiscoverRequest.DiscoverRequestType]
        RATE_LIMIT: _ClassVar[DiscoverRequest.DiscoverRequestType]
        CIRCUIT_BREAKER: _ClassVar[DiscoverRequest.DiscoverRequestType]
        SERVICES: _ClassVar[DiscoverRequest.DiscoverRequestType]
        NAMESPACES: _ClassVar[DiscoverRequest.DiscoverRequestType]
        FAULT_DETECTOR: _ClassVar[DiscoverRequest.DiscoverRequestType]
    UNKNOWN: DiscoverRequest.DiscoverRequestType
    INSTANCE: DiscoverRequest.DiscoverRequestType
    CLUSTER: DiscoverRequest.DiscoverRequestType
    ROUTING: DiscoverRequest.DiscoverRequestType
    RATE_LIMIT: DiscoverRequest.DiscoverRequestType
    CIRCUIT_BREAKER: DiscoverRequest.DiscoverRequestType
    SERVICES: DiscoverRequest.DiscoverRequestType
    NAMESPACES: DiscoverRequest.DiscoverRequestType
    FAULT_DETECTOR: DiscoverRequest.DiscoverRequestType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    type: DiscoverRequest.DiscoverRequestType
    service: _service_pb2.Service
    def __init__(self, type: _Optional[_Union[DiscoverRequest.DiscoverRequestType, str]] = ..., service: _Optional[_Union[_service_pb2.Service, _Mapping]] = ...) -> None: ...
