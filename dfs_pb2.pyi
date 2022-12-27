from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BackwardMessage(_message.Message):
    __slots__ = ["child", "parent", "type"]
    CHILD_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    child: int
    parent: int
    type: int
    def __init__(self, type: _Optional[int] = ..., child: _Optional[int] = ..., parent: _Optional[int] = ...) -> None: ...

class BackwardReply(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class CallReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CallRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ForwardMessage(_message.Message):
    __slots__ = ["origin", "type"]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    origin: int
    type: int
    def __init__(self, type: _Optional[int] = ..., origin: _Optional[int] = ...) -> None: ...

class ForwardReply(_message.Message):
    __slots__ = ["origin", "type"]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    origin: int
    type: int
    def __init__(self, type: _Optional[int] = ..., origin: _Optional[int] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ["message"]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RootRequest(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    type: int
    def __init__(self, type: _Optional[int] = ...) -> None: ...

class TreeMessage(_message.Message):
    __slots__ = ["child", "parent", "type"]
    CHILD_FIELD_NUMBER: _ClassVar[int]
    PARENT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    child: _containers.RepeatedScalarFieldContainer[int]
    parent: _containers.RepeatedScalarFieldContainer[int]
    type: int
    def __init__(self, type: _Optional[int] = ..., child: _Optional[_Iterable[int]] = ..., parent: _Optional[_Iterable[int]] = ...) -> None: ...
