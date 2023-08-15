# NOTE: This is an auto-generated file. All modifications will be overwritten.
# type: ignore
from __future__ import annotations

from typing import TypedDict, Optional
from enum import IntEnum

from polywrap_core import InvokerClient, Uri
from polywrap_msgpack import GenericMap


### Env START ###

### Env END ###

### Objects START ###

### Objects END ###

### Enums START ###
### Enums END ###

### Imported Objects START ###

### Imported Objects END ###

### Imported Enums START ###

# URI: "wrap://ens/wraps.eth:file-system@1.0.0" #
class FileSystemEncoding(IntEnum):
    ASCII = 0, "0", "ASCII"
    UTF8 = 1, "1", "UTF8"
    UTF16LE = 2, "2", "UTF16LE"
    UCS2 = 3, "3", "UCS2"
    BASE64 = 4, "4", "BASE64"
    BASE64URL = 5, "5", "BASE64URL"
    LATIN1 = 6, "6", "LATIN1"
    BINARY = 7, "7", "BINARY"
    HEX = 8, "8", "HEX"

    def __new__(cls, value: int, *aliases: str):
        obj = int.__new__(cls)
        obj._value_ = value
        for alias in aliases:
            cls._value2member_map_[alias] = obj
        return obj


### Imported Enums END ###

### Imported Modules START ###

### Imported Modules END ###

### Interface START ###


### Interface END ###
