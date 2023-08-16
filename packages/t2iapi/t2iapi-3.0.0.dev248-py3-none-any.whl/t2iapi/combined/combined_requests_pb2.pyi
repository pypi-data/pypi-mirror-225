from t2iapi.context import types_pb2 as _types_pb2
from t2iapi.operation import types_pb2 as _types_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateContextStateWithAssociationAndSetOperatingModeRequest(_message.Message):
    __slots__ = ["context_association", "context_descriptor_handle", "operating_mode", "operation_descriptor_handle"]
    CONTEXT_ASSOCIATION_FIELD_NUMBER: _ClassVar[int]
    CONTEXT_DESCRIPTOR_HANDLE_FIELD_NUMBER: _ClassVar[int]
    OPERATING_MODE_FIELD_NUMBER: _ClassVar[int]
    OPERATION_DESCRIPTOR_HANDLE_FIELD_NUMBER: _ClassVar[int]
    context_association: _types_pb2.ContextAssociation
    context_descriptor_handle: str
    operating_mode: _types_pb2_1.OperatingMode
    operation_descriptor_handle: str
    def __init__(self, context_descriptor_handle: _Optional[str] = ..., context_association: _Optional[_Union[_types_pb2.ContextAssociation, str]] = ..., operation_descriptor_handle: _Optional[str] = ..., operating_mode: _Optional[_Union[_types_pb2_1.OperatingMode, str]] = ...) -> None: ...
