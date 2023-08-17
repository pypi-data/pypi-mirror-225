# NOTE: This is an auto-generated file. All modifications will be overwritten.
# type: ignore
from __future__ import annotations

from typing import TypedDict, Optional
from enum import IntEnum

from polywrap_core import InvokerClient, Uri
from polywrap_msgpack import GenericMap


### Env START ###

Env = TypedDict("Env", {
    "connection": Optional["Connection"],
})

### Env END ###

### Objects START ###

Connection = TypedDict("Connection", {
    "node": Optional[str],
    "networkNameOrChainId": Optional[str],
})

### Objects END ###

### Enums START ###
### Enums END ###

### Imported Objects START ###

### Imported Objects END ###

### Imported Enums START ###


### Imported Enums END ###

### Imported Modules START ###

### Imported Modules END ###

### Interface START ###


### Interface END ###
