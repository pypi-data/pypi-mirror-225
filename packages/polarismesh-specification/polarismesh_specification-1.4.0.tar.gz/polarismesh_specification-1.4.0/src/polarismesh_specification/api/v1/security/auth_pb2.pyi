from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AuthAction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ONLY_READ: _ClassVar[AuthAction]
    READ_WRITE: _ClassVar[AuthAction]

class ResourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    Namespaces: _ClassVar[ResourceType]
    Services: _ClassVar[ResourceType]
    ConfigGroups: _ClassVar[ResourceType]
ONLY_READ: AuthAction
READ_WRITE: AuthAction
Namespaces: ResourceType
Services: ResourceType
ConfigGroups: ResourceType

class LoginRequest(_message.Message):
    __slots__ = ["owner", "name", "password"]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    owner: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    password: _wrappers_pb2.StringValue
    def __init__(self, owner: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., password: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class LoginResponse(_message.Message):
    __slots__ = ["user_id", "name", "role", "owner_id", "token"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    OWNER_ID_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    user_id: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    role: _wrappers_pb2.StringValue
    owner_id: _wrappers_pb2.StringValue
    token: _wrappers_pb2.StringValue
    def __init__(self, user_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., role: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., owner_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., token: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ["id", "name", "password", "owner", "source", "auth_token", "token_enable", "comment", "ctime", "mtime", "user_type", "mobile", "email"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    USER_TYPE_FIELD_NUMBER: _ClassVar[int]
    MOBILE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    password: _wrappers_pb2.StringValue
    owner: _wrappers_pb2.StringValue
    source: _wrappers_pb2.StringValue
    auth_token: _wrappers_pb2.StringValue
    token_enable: _wrappers_pb2.BoolValue
    comment: _wrappers_pb2.StringValue
    ctime: _wrappers_pb2.StringValue
    mtime: _wrappers_pb2.StringValue
    user_type: _wrappers_pb2.StringValue
    mobile: _wrappers_pb2.StringValue
    email: _wrappers_pb2.StringValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., password: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., owner: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., source: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., auth_token: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., token_enable: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., comment: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ctime: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., mtime: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., user_type: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., mobile: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., email: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class ModifyUserPassword(_message.Message):
    __slots__ = ["id", "old_password", "new_password"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OLD_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    NEW_PASSWORD_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    old_password: _wrappers_pb2.StringValue
    new_password: _wrappers_pb2.StringValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., old_password: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., new_password: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class UserGroupRelation(_message.Message):
    __slots__ = ["group_id", "users"]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    USERS_FIELD_NUMBER: _ClassVar[int]
    group_id: _wrappers_pb2.StringValue
    users: _containers.RepeatedCompositeFieldContainer[User]
    def __init__(self, group_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., users: _Optional[_Iterable[_Union[User, _Mapping]]] = ...) -> None: ...

class UserGroup(_message.Message):
    __slots__ = ["id", "name", "owner", "auth_token", "token_enable", "comment", "ctime", "mtime", "relation", "user_count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    RELATION_FIELD_NUMBER: _ClassVar[int]
    USER_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    owner: _wrappers_pb2.StringValue
    auth_token: _wrappers_pb2.StringValue
    token_enable: _wrappers_pb2.BoolValue
    comment: _wrappers_pb2.StringValue
    ctime: _wrappers_pb2.StringValue
    mtime: _wrappers_pb2.StringValue
    relation: UserGroupRelation
    user_count: _wrappers_pb2.UInt32Value
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., owner: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., auth_token: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., token_enable: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., comment: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ctime: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., mtime: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., relation: _Optional[_Union[UserGroupRelation, _Mapping]] = ..., user_count: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ...) -> None: ...

class ModifyUserGroup(_message.Message):
    __slots__ = ["id", "owner", "name", "auth_token", "token_enable", "comment", "add_relations", "remove_relations"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ADD_RELATIONS_FIELD_NUMBER: _ClassVar[int]
    REMOVE_RELATIONS_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    owner: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    auth_token: _wrappers_pb2.StringValue
    token_enable: _wrappers_pb2.BoolValue
    comment: _wrappers_pb2.StringValue
    add_relations: UserGroupRelation
    remove_relations: UserGroupRelation
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., owner: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., auth_token: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., token_enable: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., comment: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., add_relations: _Optional[_Union[UserGroupRelation, _Mapping]] = ..., remove_relations: _Optional[_Union[UserGroupRelation, _Mapping]] = ...) -> None: ...

class Principal(_message.Message):
    __slots__ = ["id", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class Principals(_message.Message):
    __slots__ = ["users", "groups"]
    USERS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    users: _containers.RepeatedCompositeFieldContainer[Principal]
    groups: _containers.RepeatedCompositeFieldContainer[Principal]
    def __init__(self, users: _Optional[_Iterable[_Union[Principal, _Mapping]]] = ..., groups: _Optional[_Iterable[_Union[Principal, _Mapping]]] = ...) -> None: ...

class StrategyResourceEntry(_message.Message):
    __slots__ = ["id", "namespace", "name"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    namespace: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., namespace: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...

class StrategyResources(_message.Message):
    __slots__ = ["strategy_id", "namespaces", "services", "config_groups"]
    STRATEGY_ID_FIELD_NUMBER: _ClassVar[int]
    NAMESPACES_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    CONFIG_GROUPS_FIELD_NUMBER: _ClassVar[int]
    strategy_id: _wrappers_pb2.StringValue
    namespaces: _containers.RepeatedCompositeFieldContainer[StrategyResourceEntry]
    services: _containers.RepeatedCompositeFieldContainer[StrategyResourceEntry]
    config_groups: _containers.RepeatedCompositeFieldContainer[StrategyResourceEntry]
    def __init__(self, strategy_id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., namespaces: _Optional[_Iterable[_Union[StrategyResourceEntry, _Mapping]]] = ..., services: _Optional[_Iterable[_Union[StrategyResourceEntry, _Mapping]]] = ..., config_groups: _Optional[_Iterable[_Union[StrategyResourceEntry, _Mapping]]] = ...) -> None: ...

class AuthStrategy(_message.Message):
    __slots__ = ["id", "name", "principals", "resources", "action", "comment", "owner", "ctime", "mtime", "auth_token", "default_strategy"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRINCIPALS_FIELD_NUMBER: _ClassVar[int]
    RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    CTIME_FIELD_NUMBER: _ClassVar[int]
    MTIME_FIELD_NUMBER: _ClassVar[int]
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_STRATEGY_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    principals: Principals
    resources: StrategyResources
    action: AuthAction
    comment: _wrappers_pb2.StringValue
    owner: _wrappers_pb2.StringValue
    ctime: _wrappers_pb2.StringValue
    mtime: _wrappers_pb2.StringValue
    auth_token: _wrappers_pb2.StringValue
    default_strategy: _wrappers_pb2.BoolValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., principals: _Optional[_Union[Principals, _Mapping]] = ..., resources: _Optional[_Union[StrategyResources, _Mapping]] = ..., action: _Optional[_Union[AuthAction, str]] = ..., comment: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., owner: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., ctime: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., mtime: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., auth_token: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., default_strategy: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class ModifyAuthStrategy(_message.Message):
    __slots__ = ["id", "name", "add_principals", "remove_principals", "add_resources", "remove_resources", "action", "comment", "owner"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADD_PRINCIPALS_FIELD_NUMBER: _ClassVar[int]
    REMOVE_PRINCIPALS_FIELD_NUMBER: _ClassVar[int]
    ADD_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    REMOVE_RESOURCES_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    id: _wrappers_pb2.StringValue
    name: _wrappers_pb2.StringValue
    add_principals: Principals
    remove_principals: Principals
    add_resources: StrategyResources
    remove_resources: StrategyResources
    action: AuthAction
    comment: _wrappers_pb2.StringValue
    owner: _wrappers_pb2.StringValue
    def __init__(self, id: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., name: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., add_principals: _Optional[_Union[Principals, _Mapping]] = ..., remove_principals: _Optional[_Union[Principals, _Mapping]] = ..., add_resources: _Optional[_Union[StrategyResources, _Mapping]] = ..., remove_resources: _Optional[_Union[StrategyResources, _Mapping]] = ..., action: _Optional[_Union[AuthAction, str]] = ..., comment: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., owner: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ...) -> None: ...
