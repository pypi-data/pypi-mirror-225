from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class _GenerateApiTokenRequest(_message.Message):
    __slots__ = ["auth_token", "expires", "never", "permissions"]
    class CacheRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SuperUserPermissions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class TopicRole(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Expires(_message.Message):
        __slots__ = ["valid_for_seconds"]
        VALID_FOR_SECONDS_FIELD_NUMBER: _ClassVar[int]
        valid_for_seconds: int
        def __init__(self, valid_for_seconds: _Optional[int] = ...) -> None: ...
    class ExplicitPermissions(_message.Message):
        __slots__ = ["permissions"]
        PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
        permissions: _containers.RepeatedCompositeFieldContainer[_GenerateApiTokenRequest.PermissionsType]
        def __init__(self, permissions: _Optional[_Iterable[_Union[_GenerateApiTokenRequest.PermissionsType, _Mapping]]] = ...) -> None: ...
    class Never(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class Permissions(_message.Message):
        __slots__ = ["explicit", "super_user"]
        EXPLICIT_FIELD_NUMBER: _ClassVar[int]
        SUPER_USER_FIELD_NUMBER: _ClassVar[int]
        explicit: _GenerateApiTokenRequest.ExplicitPermissions
        super_user: _GenerateApiTokenRequest.SuperUserPermissions
        def __init__(self, super_user: _Optional[_Union[_GenerateApiTokenRequest.SuperUserPermissions, str]] = ..., explicit: _Optional[_Union[_GenerateApiTokenRequest.ExplicitPermissions, _Mapping]] = ...) -> None: ...
    class PermissionsType(_message.Message):
        __slots__ = ["cache_permissions", "topic_permissions"]
        class All(_message.Message):
            __slots__ = []
            def __init__(self) -> None: ...
        class CacheItemSelector(_message.Message):
            __slots__ = ["key", "key_prefix"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            KEY_PREFIX_FIELD_NUMBER: _ClassVar[int]
            key: bytes
            key_prefix: bytes
            def __init__(self, key: _Optional[bytes] = ..., key_prefix: _Optional[bytes] = ...) -> None: ...
        class CachePermissions(_message.Message):
            __slots__ = ["all_caches", "all_items", "cache_selector", "item_selector", "role"]
            ALL_CACHES_FIELD_NUMBER: _ClassVar[int]
            ALL_ITEMS_FIELD_NUMBER: _ClassVar[int]
            CACHE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
            ITEM_SELECTOR_FIELD_NUMBER: _ClassVar[int]
            ROLE_FIELD_NUMBER: _ClassVar[int]
            all_caches: _GenerateApiTokenRequest.PermissionsType.All
            all_items: _GenerateApiTokenRequest.PermissionsType.All
            cache_selector: _GenerateApiTokenRequest.PermissionsType.CacheSelector
            item_selector: _GenerateApiTokenRequest.PermissionsType.CacheItemSelector
            role: _GenerateApiTokenRequest.CacheRole
            def __init__(self, role: _Optional[_Union[_GenerateApiTokenRequest.CacheRole, str]] = ..., all_caches: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.All, _Mapping]] = ..., cache_selector: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.CacheSelector, _Mapping]] = ..., all_items: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.All, _Mapping]] = ..., item_selector: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.CacheItemSelector, _Mapping]] = ...) -> None: ...
        class CacheSelector(_message.Message):
            __slots__ = ["cache_name"]
            CACHE_NAME_FIELD_NUMBER: _ClassVar[int]
            cache_name: str
            def __init__(self, cache_name: _Optional[str] = ...) -> None: ...
        class TopicPermissions(_message.Message):
            __slots__ = ["all_caches", "all_topics", "cache_selector", "role", "topic_selector"]
            ALL_CACHES_FIELD_NUMBER: _ClassVar[int]
            ALL_TOPICS_FIELD_NUMBER: _ClassVar[int]
            CACHE_SELECTOR_FIELD_NUMBER: _ClassVar[int]
            ROLE_FIELD_NUMBER: _ClassVar[int]
            TOPIC_SELECTOR_FIELD_NUMBER: _ClassVar[int]
            all_caches: _GenerateApiTokenRequest.PermissionsType.All
            all_topics: _GenerateApiTokenRequest.PermissionsType.All
            cache_selector: _GenerateApiTokenRequest.PermissionsType.CacheSelector
            role: _GenerateApiTokenRequest.TopicRole
            topic_selector: _GenerateApiTokenRequest.PermissionsType.TopicSelector
            def __init__(self, role: _Optional[_Union[_GenerateApiTokenRequest.TopicRole, str]] = ..., all_caches: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.All, _Mapping]] = ..., cache_selector: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.CacheSelector, _Mapping]] = ..., all_topics: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.All, _Mapping]] = ..., topic_selector: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.TopicSelector, _Mapping]] = ...) -> None: ...
        class TopicSelector(_message.Message):
            __slots__ = ["topic_name"]
            TOPIC_NAME_FIELD_NUMBER: _ClassVar[int]
            topic_name: str
            def __init__(self, topic_name: _Optional[str] = ...) -> None: ...
        CACHE_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
        TOPIC_PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
        cache_permissions: _GenerateApiTokenRequest.PermissionsType.CachePermissions
        topic_permissions: _GenerateApiTokenRequest.PermissionsType.TopicPermissions
        def __init__(self, cache_permissions: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.CachePermissions, _Mapping]] = ..., topic_permissions: _Optional[_Union[_GenerateApiTokenRequest.PermissionsType.TopicPermissions, _Mapping]] = ...) -> None: ...
    AUTH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    CachePermitNone: _GenerateApiTokenRequest.CacheRole
    CacheReadOnly: _GenerateApiTokenRequest.CacheRole
    CacheReadWrite: _GenerateApiTokenRequest.CacheRole
    CacheWriteOnly: _GenerateApiTokenRequest.CacheRole
    EXPIRES_FIELD_NUMBER: _ClassVar[int]
    NEVER_FIELD_NUMBER: _ClassVar[int]
    PERMISSIONS_FIELD_NUMBER: _ClassVar[int]
    SuperUser: _GenerateApiTokenRequest.SuperUserPermissions
    TopicPermitNone: _GenerateApiTokenRequest.TopicRole
    TopicReadOnly: _GenerateApiTokenRequest.TopicRole
    TopicReadWrite: _GenerateApiTokenRequest.TopicRole
    TopicWriteOnly: _GenerateApiTokenRequest.TopicRole
    auth_token: str
    expires: _GenerateApiTokenRequest.Expires
    never: _GenerateApiTokenRequest.Never
    permissions: _GenerateApiTokenRequest.Permissions
    def __init__(self, never: _Optional[_Union[_GenerateApiTokenRequest.Never, _Mapping]] = ..., expires: _Optional[_Union[_GenerateApiTokenRequest.Expires, _Mapping]] = ..., auth_token: _Optional[str] = ..., permissions: _Optional[_Union[_GenerateApiTokenRequest.Permissions, _Mapping]] = ...) -> None: ...

class _GenerateApiTokenResponse(_message.Message):
    __slots__ = ["api_key", "endpoint", "refresh_token", "valid_until"]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    VALID_UNTIL_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    endpoint: str
    refresh_token: str
    valid_until: int
    def __init__(self, api_key: _Optional[str] = ..., refresh_token: _Optional[str] = ..., endpoint: _Optional[str] = ..., valid_until: _Optional[int] = ...) -> None: ...

class _LoginRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class _LoginResponse(_message.Message):
    __slots__ = ["direct_browser", "error", "logged_in", "message"]
    class DirectBrowser(_message.Message):
        __slots__ = ["url"]
        URL_FIELD_NUMBER: _ClassVar[int]
        url: str
        def __init__(self, url: _Optional[str] = ...) -> None: ...
    class Error(_message.Message):
        __slots__ = ["description"]
        DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
        description: str
        def __init__(self, description: _Optional[str] = ...) -> None: ...
    class LoggedIn(_message.Message):
        __slots__ = ["session_token", "valid_for_seconds"]
        SESSION_TOKEN_FIELD_NUMBER: _ClassVar[int]
        VALID_FOR_SECONDS_FIELD_NUMBER: _ClassVar[int]
        session_token: str
        valid_for_seconds: int
        def __init__(self, session_token: _Optional[str] = ..., valid_for_seconds: _Optional[int] = ...) -> None: ...
    class Message(_message.Message):
        __slots__ = ["text"]
        TEXT_FIELD_NUMBER: _ClassVar[int]
        text: str
        def __init__(self, text: _Optional[str] = ...) -> None: ...
    DIRECT_BROWSER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    LOGGED_IN_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    direct_browser: _LoginResponse.DirectBrowser
    error: _LoginResponse.Error
    logged_in: _LoginResponse.LoggedIn
    message: _LoginResponse.Message
    def __init__(self, direct_browser: _Optional[_Union[_LoginResponse.DirectBrowser, _Mapping]] = ..., logged_in: _Optional[_Union[_LoginResponse.LoggedIn, _Mapping]] = ..., message: _Optional[_Union[_LoginResponse.Message, _Mapping]] = ..., error: _Optional[_Union[_LoginResponse.Error, _Mapping]] = ...) -> None: ...

class _RefreshApiTokenRequest(_message.Message):
    __slots__ = ["api_key", "refresh_token"]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    refresh_token: str
    def __init__(self, api_key: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...

class _RefreshApiTokenResponse(_message.Message):
    __slots__ = ["api_key", "endpoint", "refresh_token", "valid_until"]
    API_KEY_FIELD_NUMBER: _ClassVar[int]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    VALID_UNTIL_FIELD_NUMBER: _ClassVar[int]
    api_key: str
    endpoint: str
    refresh_token: str
    valid_until: int
    def __init__(self, api_key: _Optional[str] = ..., refresh_token: _Optional[str] = ..., endpoint: _Optional[str] = ..., valid_until: _Optional[int] = ...) -> None: ...
