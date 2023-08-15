# NOTE: This is an auto-generated file. All modifications will be overwritten.
# type: ignore
from __future__ import annotations

from abc import abstractmethod
from typing import TypeVar, Generic, TypedDict, Optional

from .types import *

from polywrap_core import InvokerClient
from polywrap_plugin import PluginModule
from polywrap_msgpack import GenericMap

TConfig = TypeVar("TConfig")


ArgsReadFile = TypedDict("ArgsReadFile", {
    "path": str
})

ArgsReadFileAsString = TypedDict("ArgsReadFileAsString", {
    "path": str,
    "encoding": Optional["FileSystemEncoding"]
})

ArgsExists = TypedDict("ArgsExists", {
    "path": str
})

ArgsWriteFile = TypedDict("ArgsWriteFile", {
    "path": str,
    "data": bytes
})

ArgsMkdir = TypedDict("ArgsMkdir", {
    "path": str,
    "recursive": Optional[bool]
})

ArgsRm = TypedDict("ArgsRm", {
    "path": str,
    "recursive": Optional[bool],
    "force": Optional[bool]
})

ArgsRmdir = TypedDict("ArgsRmdir", {
    "path": str
})


class Module(Generic[TConfig], PluginModule[TConfig]):
    def __new__(cls, *args, **kwargs):
        # NOTE: This is used to dynamically add WRAP ABI compatible methods to the class
        instance = super().__new__(cls)
        setattr(instance, "readFile", instance.read_file)
        setattr(instance, "readFileAsString", instance.read_file_as_string)
        setattr(instance, "exists", instance.exists)
        setattr(instance, "writeFile", instance.write_file)
        setattr(instance, "mkdir", instance.mkdir)
        setattr(instance, "rm", instance.rm)
        setattr(instance, "rmdir", instance.rmdir)
        return instance

    @abstractmethod
    def read_file(
        self,
        args: ArgsReadFile,
        client: InvokerClient,
        env: None
    ) -> bytes:
        pass

    @abstractmethod
    def read_file_as_string(
        self,
        args: ArgsReadFileAsString,
        client: InvokerClient,
        env: None
    ) -> str:
        pass

    @abstractmethod
    def exists(
        self,
        args: ArgsExists,
        client: InvokerClient,
        env: None
    ) -> bool:
        pass

    @abstractmethod
    def write_file(
        self,
        args: ArgsWriteFile,
        client: InvokerClient,
        env: None
    ) -> Optional[bool]:
        pass

    @abstractmethod
    def mkdir(
        self,
        args: ArgsMkdir,
        client: InvokerClient,
        env: None
    ) -> Optional[bool]:
        pass

    @abstractmethod
    def rm(
        self,
        args: ArgsRm,
        client: InvokerClient,
        env: None
    ) -> Optional[bool]:
        pass

    @abstractmethod
    def rmdir(
        self,
        args: ArgsRmdir,
        client: InvokerClient,
        env: None
    ) -> Optional[bool]:
        pass

