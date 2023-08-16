from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Item(_message.Message):
    __slots__ = ["id", "metadata", "vector"]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    VECTOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _containers.RepeatedCompositeFieldContainer[Metadata]
    vector: Vector
    def __init__(self, id: _Optional[str] = ..., vector: _Optional[_Union[Vector, _Mapping]] = ..., metadata: _Optional[_Iterable[_Union[Metadata, _Mapping]]] = ...) -> None: ...

class Metadata(_message.Message):
    __slots__ = ["field", "string_value"]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    field: str
    string_value: str
    def __init__(self, field: _Optional[str] = ..., string_value: _Optional[str] = ...) -> None: ...

class MetadataRequest(_message.Message):
    __slots__ = ["some"]
    class All(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    class Some(_message.Message):
        __slots__ = ["fields"]
        FIELDS_FIELD_NUMBER: _ClassVar[int]
        fields: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, fields: _Optional[_Iterable[str]] = ...) -> None: ...
    SOME_FIELD_NUMBER: _ClassVar[int]
    some: MetadataRequest.Some
    def __init__(self, some: _Optional[_Union[MetadataRequest.Some, _Mapping]] = ...) -> None: ...

class SearchHit(_message.Message):
    __slots__ = ["distance", "id", "metadata"]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    distance: float
    id: str
    metadata: _containers.RepeatedCompositeFieldContainer[Metadata]
    def __init__(self, id: _Optional[str] = ..., distance: _Optional[float] = ..., metadata: _Optional[_Iterable[_Union[Metadata, _Mapping]]] = ...) -> None: ...

class SearchRequest(_message.Message):
    __slots__ = ["index_name", "metadata_fields", "query_vector", "top_k"]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELDS_FIELD_NUMBER: _ClassVar[int]
    QUERY_VECTOR_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    index_name: str
    metadata_fields: MetadataRequest
    query_vector: Vector
    top_k: int
    def __init__(self, index_name: _Optional[str] = ..., top_k: _Optional[int] = ..., query_vector: _Optional[_Union[Vector, _Mapping]] = ..., metadata_fields: _Optional[_Union[MetadataRequest, _Mapping]] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ["hits"]
    HITS_FIELD_NUMBER: _ClassVar[int]
    hits: _containers.RepeatedCompositeFieldContainer[SearchHit]
    def __init__(self, hits: _Optional[_Iterable[_Union[SearchHit, _Mapping]]] = ...) -> None: ...

class UpsertItemBatchRequest(_message.Message):
    __slots__ = ["index_name", "items"]
    INDEX_NAME_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    index_name: str
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, index_name: _Optional[str] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class UpsertItemBatchResponse(_message.Message):
    __slots__ = ["error_indices"]
    ERROR_INDICES_FIELD_NUMBER: _ClassVar[int]
    error_indices: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, error_indices: _Optional[_Iterable[int]] = ...) -> None: ...

class Vector(_message.Message):
    __slots__ = ["elements"]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    elements: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, elements: _Optional[_Iterable[float]] = ...) -> None: ...
