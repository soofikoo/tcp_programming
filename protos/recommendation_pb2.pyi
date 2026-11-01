from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RecommendationRequest(_message.Message):
    __slots__ = ("user_id", "limit")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    user_id: int
    limit: int
    def __init__(self, user_id: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class RecommendedTrack(_message.Message):
    __slots__ = ("track_id", "score", "reason")
    TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    track_id: int
    score: float
    reason: str
    def __init__(self, track_id: _Optional[int] = ..., score: _Optional[float] = ..., reason: _Optional[str] = ...) -> None: ...

class RecommendationResponse(_message.Message):
    __slots__ = ("tracks", "cold_start")
    TRACKS_FIELD_NUMBER: _ClassVar[int]
    COLD_START_FIELD_NUMBER: _ClassVar[int]
    tracks: _containers.RepeatedCompositeFieldContainer[RecommendedTrack]
    cold_start: bool
    def __init__(self, tracks: _Optional[_Iterable[_Union[RecommendedTrack, _Mapping]]] = ..., cold_start: _Optional[bool] = ...) -> None: ...
