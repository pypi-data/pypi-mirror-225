import google.protobuf.message
import modal._resolver
import modal.client
import typing
import typing_extensions

H = typing.TypeVar("H", bound="_Handle")

_BLOCKING_H = typing.TypeVar("_BLOCKING_H", bound="Handle")

class _Handle:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _object_id: str
    _client: modal.client._Client
    _is_hydrated: bool

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None):
        ...

    def __init__(self):
        ...

    def _init(self):
        ...

    @classmethod
    def _new(cls: typing.Type[H]) -> H:
        ...

    def _initialize_from_empty(self):
        ...

    def _hydrate(self, object_id: str, client: modal.client._Client, metadata: typing.Union[google.protobuf.message.Message, None]):
        ...

    def _hydrate_from_other(self, other: _Handle):
        ...

    def is_hydrated(self) -> bool:
        ...

    def _hydrate_metadata(self, metadata: google.protobuf.message.Message):
        ...

    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]:
        ...

    @classmethod
    def _new_hydrated(cls: typing.Type[H], object_id: str, client: modal.client._Client, handle_metadata: typing.Union[google.protobuf.message.Message, None]) -> H:
        ...

    @classmethod
    async def from_id(cls: typing.Type[H], object_id: str, client: typing.Union[modal.client._Client, None] = None) -> H:
        ...

    @property
    def object_id(self) -> str:
        ...

    async def _hydrate_from_app(self, app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None):
        ...


class Handle:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _object_id: str
    _client: modal.client.Client
    _is_hydrated: bool

    def __init__(self):
        ...

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None):
        ...

    def _init(self):
        ...

    @classmethod
    def _new(cls: typing.Type[_BLOCKING_H]) -> _BLOCKING_H:
        ...

    def _initialize_from_empty(self):
        ...

    def _hydrate(self, object_id: str, client: modal.client.Client, metadata: typing.Union[google.protobuf.message.Message, None]):
        ...

    def _hydrate_from_other(self, other: Handle):
        ...

    def is_hydrated(self) -> bool:
        ...

    def _hydrate_metadata(self, metadata: google.protobuf.message.Message):
        ...

    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]:
        ...

    @classmethod
    def _new_hydrated(cls: typing.Type[_BLOCKING_H], object_id: str, client: modal.client.Client, handle_metadata: typing.Union[google.protobuf.message.Message, None]) -> _BLOCKING_H:
        ...

    @classmethod
    def from_id(cls: typing.Type[_BLOCKING_H], object_id: str, client: typing.Union[modal.client.Client, None] = None) -> _BLOCKING_H:
        ...

    @property
    def object_id(self) -> str:
        ...

    class ___hydrate_from_app_spec(typing_extensions.Protocol):
        def __call__(self, app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None):
            ...

        async def aio(self, *args, **kwargs):
            ...

    _hydrate_from_app: ___hydrate_from_app_spec


P = typing.TypeVar("P", bound="_Provider")

_BLOCKING_P = typing.TypeVar("_BLOCKING_P", bound="Provider")

class _Provider:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _load: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], _Handle], typing.Awaitable[None]], None]
    _preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], _Handle], typing.Awaitable[None]], None]
    _handle: _Handle

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None):
        ...

    def __init__(self):
        ...

    @classmethod
    def _get_handle_cls(cls) -> typing.Type[_Handle]:
        ...

    def _init(self, rep: str, load: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], _Handle], typing.Awaitable[None]], None] = None, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], _Handle], typing.Awaitable[None]], None] = None, handle: typing.Union[_Handle, None] = None):
        ...

    def _init_from_other(self, other: _Provider):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], _Handle], typing.Awaitable[None]], rep: str, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], _Handle], typing.Awaitable[None]], None] = None):
        ...

    @classmethod
    def _new_hydrated(cls: typing.Type[P], object_id: str, client: modal.client._Client, handle_metadata: typing.Union[google.protobuf.message.Message, None]) -> P:
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    @property
    def object_id(self):
        ...

    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]:
        ...

    def is_hydrated(self) -> bool:
        ...

    @property
    def _client(self) -> modal.client._Client:
        ...

    async def _deploy(self, label: str, namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None) -> None:
        ...

    def persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    def _persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    @classmethod
    def from_name(cls: typing.Type[P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, environment_name: typing.Union[str, None] = None) -> P:
        ...

    @classmethod
    async def lookup(cls: typing.Type[P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None, environment_name: typing.Union[str, None] = None) -> P:
        ...

    @classmethod
    async def _exists(cls: typing.Type[P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client._Client, None] = None) -> bool:
        ...


class Provider:
    _type_prefix: typing.ClassVar[typing.Union[str, None]]
    _prefix_to_type: typing.ClassVar[typing.Dict[str, type]]
    _load: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], None], None]
    _preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], None], None]
    _handle: Handle

    def __init__(self):
        ...

    @classmethod
    def __init_subclass__(cls, type_prefix: typing.Union[str, None] = None):
        ...

    @classmethod
    def _get_handle_cls(cls) -> typing.Type[Handle]:
        ...

    class ___init_spec(typing_extensions.Protocol):
        def __call__(self, rep: str, load: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], None], None] = None, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], None], None] = None, handle: typing.Union[Handle, None] = None):
            ...

        def aio(self, rep: str, load: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], typing.Awaitable[None]], None] = None, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], typing.Awaitable[None]], None] = None, handle: typing.Union[Handle, None] = None):
            ...

    _init: ___init_spec

    def _init_from_other(self, other: Provider):
        ...

    @classmethod
    def _from_loader(cls, load: typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], None], rep: str, is_persisted_ref: bool = False, preload: typing.Union[typing.Callable[[modal._resolver.Resolver, typing.Union[str, None], Handle], None], None] = None):
        ...

    @classmethod
    def _new_hydrated(cls: typing.Type[_BLOCKING_P], object_id: str, client: modal.client.Client, handle_metadata: typing.Union[google.protobuf.message.Message, None]) -> _BLOCKING_P:
        ...

    def __repr__(self):
        ...

    @property
    def local_uuid(self):
        ...

    @property
    def object_id(self):
        ...

    def _get_metadata(self) -> typing.Union[google.protobuf.message.Message, None]:
        ...

    def is_hydrated(self) -> bool:
        ...

    @property
    def _client(self) -> modal.client.Client:
        ...

    class ___deploy_spec(typing_extensions.Protocol):
        def __call__(self, label: str, namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None) -> None:
            ...

        async def aio(self, *args, **kwargs) -> None:
            ...

    _deploy: ___deploy_spec

    def persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    def _persist(self, label: str, namespace=1, environment_name: typing.Union[str, None] = None):
        ...

    @classmethod
    def from_name(cls: typing.Type[_BLOCKING_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, environment_name: typing.Union[str, None] = None) -> _BLOCKING_P:
        ...

    @classmethod
    def lookup(cls: typing.Type[_BLOCKING_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None, environment_name: typing.Union[str, None] = None) -> _BLOCKING_P:
        ...

    @classmethod
    def _exists(cls: typing.Type[_BLOCKING_P], app_name: str, tag: typing.Union[str, None] = None, namespace=1, client: typing.Union[modal.client.Client, None] = None) -> bool:
        ...
