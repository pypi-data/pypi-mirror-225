from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PipelineReq(_message.Message):
    __slots__ = ["app_id"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    def __init__(self, app_id: _Optional[str] = ...) -> None: ...

class PipelineRes(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class InferenceReq(_message.Message):
    __slots__ = ["app_id", "stream_id", "uri", "settings", "name", "offset"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    URI_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    stream_id: str
    uri: str
    settings: str
    name: str
    offset: int
    def __init__(self, app_id: _Optional[str] = ..., stream_id: _Optional[str] = ..., uri: _Optional[str] = ..., settings: _Optional[str] = ..., name: _Optional[str] = ..., offset: _Optional[int] = ...) -> None: ...

class InferenceRes(_message.Message):
    __slots__ = ["count", "status", "eos", "err", "meta", "snapshot", "app_id", "stream_id"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    EOS_FIELD_NUMBER: _ClassVar[int]
    ERR_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    count: int
    status: int
    eos: bool
    err: bool
    meta: str
    snapshot: bytes
    app_id: str
    stream_id: str
    def __init__(self, count: _Optional[int] = ..., status: _Optional[int] = ..., eos: bool = ..., err: bool = ..., meta: _Optional[str] = ..., snapshot: _Optional[bytes] = ..., app_id: _Optional[str] = ..., stream_id: _Optional[str] = ...) -> None: ...

class AppReq(_message.Message):
    __slots__ = ["app_id", "chunk"]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    app_id: str
    chunk: bytes
    def __init__(self, app_id: _Optional[str] = ..., chunk: _Optional[bytes] = ...) -> None: ...

class AppRes(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class AppList(_message.Message):
    __slots__ = ["app"]
    APP_FIELD_NUMBER: _ClassVar[int]
    app: _containers.RepeatedCompositeFieldContainer[App]
    def __init__(self, app: _Optional[_Iterable[_Union[App, _Mapping]]] = ...) -> None: ...

class InferenceList(_message.Message):
    __slots__ = ["inference"]
    INFERENCE_FIELD_NUMBER: _ClassVar[int]
    inference: _containers.RepeatedCompositeFieldContainer[InferenceReq]
    def __init__(self, inference: _Optional[_Iterable[_Union[InferenceReq, _Mapping]]] = ...) -> None: ...

class InferenceResList(_message.Message):
    __slots__ = ["inference"]
    INFERENCE_FIELD_NUMBER: _ClassVar[int]
    inference: _containers.RepeatedCompositeFieldContainer[InferenceRes]
    def __init__(self, inference: _Optional[_Iterable[_Union[InferenceRes, _Mapping]]] = ...) -> None: ...

class LicReq(_message.Message):
    __slots__ = ["key", "hash_code"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    HASH_CODE_FIELD_NUMBER: _ClassVar[int]
    key: str
    hash_code: str
    def __init__(self, key: _Optional[str] = ..., hash_code: _Optional[str] = ...) -> None: ...

class LicRes(_message.Message):
    __slots__ = ["result", "hash_code"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    HASH_CODE_FIELD_NUMBER: _ClassVar[int]
    result: bool
    hash_code: str
    def __init__(self, result: bool = ..., hash_code: _Optional[str] = ...) -> None: ...

class StreamingReq(_message.Message):
    __slots__ = ["uri", "session_id"]
    URI_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    uri: str
    session_id: str
    def __init__(self, uri: _Optional[str] = ..., session_id: _Optional[str] = ...) -> None: ...

class StreamingRes(_message.Message):
    __slots__ = ["location", "ts_start", "session_id"]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    TS_START_FIELD_NUMBER: _ClassVar[int]
    SESSION_ID_FIELD_NUMBER: _ClassVar[int]
    location: str
    ts_start: int
    session_id: str
    def __init__(self, location: _Optional[str] = ..., ts_start: _Optional[int] = ..., session_id: _Optional[str] = ...) -> None: ...

class Model(_message.Message):
    __slots__ = ["id", "name", "version", "platform", "framework", "capacity", "precision", "desc", "path", "compute_capa", "ref_count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    PRECISION_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    COMPUTE_CAPA_FIELD_NUMBER: _ClassVar[int]
    REF_COUNT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    version: str
    platform: str
    framework: str
    capacity: int
    precision: str
    desc: str
    path: str
    compute_capa: str
    ref_count: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., version: _Optional[str] = ..., platform: _Optional[str] = ..., framework: _Optional[str] = ..., capacity: _Optional[int] = ..., precision: _Optional[str] = ..., desc: _Optional[str] = ..., path: _Optional[str] = ..., compute_capa: _Optional[str] = ..., ref_count: _Optional[int] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ["category_id", "category_name", "targets"]
    class Target(_message.Message):
        __slots__ = ["event_name", "event_id", "classes"]
        EVENT_NAME_FIELD_NUMBER: _ClassVar[int]
        EVENT_ID_FIELD_NUMBER: _ClassVar[int]
        CLASSES_FIELD_NUMBER: _ClassVar[int]
        event_name: str
        event_id: str
        classes: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, event_name: _Optional[str] = ..., event_id: _Optional[str] = ..., classes: _Optional[_Iterable[str]] = ...) -> None: ...
    CATEGORY_ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    category_id: str
    category_name: str
    targets: _containers.RepeatedCompositeFieldContainer[Event.Target]
    def __init__(self, category_id: _Optional[str] = ..., category_name: _Optional[str] = ..., targets: _Optional[_Iterable[_Union[Event.Target, _Mapping]]] = ...) -> None: ...

class Pipeline(_message.Message):
    __slots__ = ["name", "plugin", "model_id", "classes"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PLUGIN_FIELD_NUMBER: _ClassVar[int]
    MODEL_ID_FIELD_NUMBER: _ClassVar[int]
    CLASSES_FIELD_NUMBER: _ClassVar[int]
    name: str
    plugin: str
    model_id: str
    classes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., plugin: _Optional[str] = ..., model_id: _Optional[str] = ..., classes: _Optional[_Iterable[str]] = ...) -> None: ...

class App(_message.Message):
    __slots__ = ["id", "name", "evgen_path", "models", "events", "pipelines", "cover_path", "desc", "memory_usage", "version", "framework", "outputs"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EVGEN_PATH_FIELD_NUMBER: _ClassVar[int]
    MODELS_FIELD_NUMBER: _ClassVar[int]
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    PIPELINES_FIELD_NUMBER: _ClassVar[int]
    COVER_PATH_FIELD_NUMBER: _ClassVar[int]
    DESC_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USAGE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    evgen_path: str
    models: _containers.RepeatedCompositeFieldContainer[Model]
    events: str
    pipelines: str
    cover_path: str
    desc: str
    memory_usage: int
    version: str
    framework: str
    outputs: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., evgen_path: _Optional[str] = ..., models: _Optional[_Iterable[_Union[Model, _Mapping]]] = ..., events: _Optional[str] = ..., pipelines: _Optional[str] = ..., cover_path: _Optional[str] = ..., desc: _Optional[str] = ..., memory_usage: _Optional[int] = ..., version: _Optional[str] = ..., framework: _Optional[str] = ..., outputs: _Optional[str] = ...) -> None: ...

class Dx(_message.Message):
    __slots__ = ["id", "name", "address", "capacity", "activated", "version", "framework", "lic_type", "lic_end_date", "lic_key"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    ACTIVATED_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    LIC_TYPE_FIELD_NUMBER: _ClassVar[int]
    LIC_END_DATE_FIELD_NUMBER: _ClassVar[int]
    LIC_KEY_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    address: str
    capacity: int
    activated: int
    version: str
    framework: str
    lic_type: str
    lic_end_date: str
    lic_key: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., address: _Optional[str] = ..., capacity: _Optional[int] = ..., activated: _Optional[int] = ..., version: _Optional[str] = ..., framework: _Optional[str] = ..., lic_type: _Optional[str] = ..., lic_end_date: _Optional[str] = ..., lic_key: _Optional[str] = ...) -> None: ...
