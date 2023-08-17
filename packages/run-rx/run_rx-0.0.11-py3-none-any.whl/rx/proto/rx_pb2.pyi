from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
INSUFFICIENT_FUNDS: StatusCode
INVALID: StatusCode
NOT_FOUND: StatusCode
OK: StatusCode
SUBSCRIPTION_REQUIRED: StatusCode
UNAUTHORIZED: StatusCode
UNKNOWN: StatusCode

class Delta(_message.Message):
    __slots__ = ["add_dir", "add_path", "remove_path"]
    ADD_DIR_FIELD_NUMBER: _ClassVar[int]
    ADD_PATH_FIELD_NUMBER: _ClassVar[int]
    REMOVE_PATH_FIELD_NUMBER: _ClassVar[int]
    add_dir: _containers.RepeatedScalarFieldContainer[str]
    add_path: _containers.RepeatedScalarFieldContainer[str]
    remove_path: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, add_path: _Optional[_Iterable[str]] = ..., add_dir: _Optional[_Iterable[str]] = ..., remove_path: _Optional[_Iterable[str]] = ...) -> None: ...

class DockerImagePullProgress(_message.Message):
    __slots__ = ["current", "id", "status", "total"]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    current: int
    id: str
    status: str
    total: int
    def __init__(self, id: _Optional[str] = ..., status: _Optional[str] = ..., total: _Optional[int] = ..., current: _Optional[int] = ...) -> None: ...

class Environment(_message.Message):
    __slots__ = ["alloc", "python", "sh"]
    ALLOC_FIELD_NUMBER: _ClassVar[int]
    PYTHON_FIELD_NUMBER: _ClassVar[int]
    SH_FIELD_NUMBER: _ClassVar[int]
    alloc: Remote
    python: Python
    sh: str
    def __init__(self, alloc: _Optional[_Union[Remote, _Mapping]] = ..., python: _Optional[_Union[Python, _Mapping]] = ..., sh: _Optional[str] = ...) -> None: ...

class ExecRequest(_message.Message):
    __slots__ = ["argv", "cwd", "rsync_source", "stdin", "workspace_id"]
    ARGV_FIELD_NUMBER: _ClassVar[int]
    CWD_FIELD_NUMBER: _ClassVar[int]
    RSYNC_SOURCE_FIELD_NUMBER: _ClassVar[int]
    STDIN_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    argv: _containers.RepeatedScalarFieldContainer[str]
    cwd: str
    rsync_source: RsyncSource
    stdin: bytes
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ..., argv: _Optional[_Iterable[str]] = ..., rsync_source: _Optional[_Union[RsyncSource, _Mapping]] = ..., cwd: _Optional[str] = ..., stdin: _Optional[bytes] = ...) -> None: ...

class ExecResponse(_message.Message):
    __slots__ = ["execution_id", "output_files", "result", "stderr", "stdout"]
    EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_FILES_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STDERR_FIELD_NUMBER: _ClassVar[int]
    STDOUT_FIELD_NUMBER: _ClassVar[int]
    execution_id: str
    output_files: _containers.RepeatedScalarFieldContainer[str]
    result: Result
    stderr: bytes
    stdout: bytes
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ..., execution_id: _Optional[str] = ..., stdout: _Optional[bytes] = ..., stderr: _Optional[bytes] = ..., output_files: _Optional[_Iterable[str]] = ...) -> None: ...

class GetUserResponse(_message.Message):
    __slots__ = ["result", "username"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    result: Result
    username: str
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ..., username: _Optional[str] = ...) -> None: ...

class Hardware(_message.Message):
    __slots__ = ["disks", "processor"]
    class Disks(_message.Message):
        __slots__ = ["other", "rxroot_size"]
        class DiskSpec(_message.Message):
            __slots__ = ["mount_point", "size", "source"]
            MOUNT_POINT_FIELD_NUMBER: _ClassVar[int]
            SIZE_FIELD_NUMBER: _ClassVar[int]
            SOURCE_FIELD_NUMBER: _ClassVar[int]
            mount_point: str
            size: str
            source: str
            def __init__(self, size: _Optional[str] = ..., mount_point: _Optional[str] = ..., source: _Optional[str] = ...) -> None: ...
        OTHER_FIELD_NUMBER: _ClassVar[int]
        RXROOT_SIZE_FIELD_NUMBER: _ClassVar[int]
        other: _containers.RepeatedCompositeFieldContainer[Hardware.Disks.DiskSpec]
        rxroot_size: str
        def __init__(self, rxroot_size: _Optional[str] = ..., other: _Optional[_Iterable[_Union[Hardware.Disks.DiskSpec, _Mapping]]] = ...) -> None: ...
    DISKS_FIELD_NUMBER: _ClassVar[int]
    PROCESSOR_FIELD_NUMBER: _ClassVar[int]
    disks: Hardware.Disks
    processor: str
    def __init__(self, processor: _Optional[str] = ..., disks: _Optional[_Union[Hardware.Disks, _Mapping]] = ...) -> None: ...

class InitRequest(_message.Message):
    __slots__ = ["project_name", "rsync_source", "target_env"]
    PROJECT_NAME_FIELD_NUMBER: _ClassVar[int]
    RSYNC_SOURCE_FIELD_NUMBER: _ClassVar[int]
    TARGET_ENV_FIELD_NUMBER: _ClassVar[int]
    project_name: str
    rsync_source: RsyncSource
    target_env: Environment
    def __init__(self, project_name: _Optional[str] = ..., rsync_source: _Optional[_Union[RsyncSource, _Mapping]] = ..., target_env: _Optional[_Union[Environment, _Mapping]] = ...) -> None: ...

class InitResponse(_message.Message):
    __slots__ = ["payment", "result", "rsync_dest", "worker_addr", "workspace_id"]
    class PaymentRequired(_message.Message):
        __slots__ = ["needs_metered", "needs_subscription"]
        NEEDS_METERED_FIELD_NUMBER: _ClassVar[int]
        NEEDS_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
        needs_metered: float
        needs_subscription: bool
        def __init__(self, needs_subscription: bool = ..., needs_metered: _Optional[float] = ...) -> None: ...
    PAYMENT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RSYNC_DEST_FIELD_NUMBER: _ClassVar[int]
    WORKER_ADDR_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    payment: InitResponse.PaymentRequired
    result: Result
    rsync_dest: RsyncDestination
    worker_addr: str
    workspace_id: str
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ..., rsync_dest: _Optional[_Union[RsyncDestination, _Mapping]] = ..., worker_addr: _Optional[str] = ..., workspace_id: _Optional[str] = ..., payment: _Optional[_Union[InitResponse.PaymentRequired, _Mapping]] = ...) -> None: ...

class InstallDepsRequest(_message.Message):
    __slots__ = ["workspace_id"]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ...) -> None: ...

class InstallDepsResponse(_message.Message):
    __slots__ = ["result", "stdout"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    STDOUT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    stdout: bytes
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ..., stdout: _Optional[bytes] = ...) -> None: ...

class KillRequest(_message.Message):
    __slots__ = ["execution_id", "workspace_id"]
    EXECUTION_ID_FIELD_NUMBER: _ClassVar[int]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    execution_id: str
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ..., execution_id: _Optional[str] = ...) -> None: ...

class Python(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Remote(_message.Message):
    __slots__ = ["hardware", "image", "ports"]
    class Image(_message.Message):
        __slots__ = ["docker", "tag"]
        DOCKER_FIELD_NUMBER: _ClassVar[int]
        TAG_FIELD_NUMBER: _ClassVar[int]
        docker: str
        tag: str
        def __init__(self, docker: _Optional[str] = ..., tag: _Optional[str] = ...) -> None: ...
    HARDWARE_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    PORTS_FIELD_NUMBER: _ClassVar[int]
    hardware: Hardware
    image: Remote.Image
    ports: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, image: _Optional[_Union[Remote.Image, _Mapping]] = ..., hardware: _Optional[_Union[Hardware, _Mapping]] = ..., ports: _Optional[_Iterable[int]] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["code", "message"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: StatusCode
    message: str
    def __init__(self, code: _Optional[_Union[StatusCode, str]] = ..., message: _Optional[str] = ...) -> None: ...

class RsyncDestination(_message.Message):
    __slots__ = ["daemon_module"]
    DAEMON_MODULE_FIELD_NUMBER: _ClassVar[int]
    daemon_module: str
    def __init__(self, daemon_module: _Optional[str] = ...) -> None: ...

class RsyncSource(_message.Message):
    __slots__ = ["directory", "machine_id", "public_key"]
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    MACHINE_ID_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
    directory: str
    machine_id: int
    public_key: bytes
    def __init__(self, machine_id: _Optional[int] = ..., directory: _Optional[str] = ..., public_key: _Optional[bytes] = ...) -> None: ...

class SetUsernameRequest(_message.Message):
    __slots__ = ["username"]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class SetUsernameResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ...) -> None: ...

class StopRequest(_message.Message):
    __slots__ = ["workspace_id"]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ...) -> None: ...

class StopResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ...) -> None: ...

class WorkerInitRequest(_message.Message):
    __slots__ = ["workspace_id"]
    WORKSPACE_ID_FIELD_NUMBER: _ClassVar[int]
    workspace_id: str
    def __init__(self, workspace_id: _Optional[str] = ...) -> None: ...

class WorkerInitResponse(_message.Message):
    __slots__ = ["pull_progress", "result"]
    PULL_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    pull_progress: DockerImagePullProgress
    result: Result
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ..., pull_progress: _Optional[_Union[DockerImagePullProgress, _Mapping]] = ...) -> None: ...

class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
