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


ArgsRequest = TypedDict("ArgsRequest", {
    "method": str,
    "params": Optional[str],
    "connection": Optional["Connection"]
})

ArgsWaitForTransaction = TypedDict("ArgsWaitForTransaction", {
    "txHash": str,
    "confirmations": int,
    "timeout": Optional[int],
    "connection": Optional["Connection"]
})

ArgsSignerAddress = TypedDict("ArgsSignerAddress", {
    "connection": Optional["Connection"]
})

ArgsSignMessage = TypedDict("ArgsSignMessage", {
    "message": bytes,
    "connection": Optional["Connection"]
})

ArgsSignTransaction = TypedDict("ArgsSignTransaction", {
    "rlp": bytes,
    "connection": Optional["Connection"]
})


class Module(Generic[TConfig], PluginModule[TConfig]):
    def __new__(cls, *args, **kwargs):
        # NOTE: This is used to dynamically add WRAP ABI compatible methods to the class
        instance = super().__new__(cls)
        setattr(instance, "request", instance.request)
        setattr(instance, "waitForTransaction", instance.wait_for_transaction)
        setattr(instance, "signerAddress", instance.signer_address)
        setattr(instance, "signMessage", instance.sign_message)
        setattr(instance, "signTransaction", instance.sign_transaction)
        return instance

    @abstractmethod
    def request(
        self,
        args: ArgsRequest,
        client: InvokerClient,
        env: None
    ) -> str:
        pass

    @abstractmethod
    def wait_for_transaction(
        self,
        args: ArgsWaitForTransaction,
        client: InvokerClient,
        env: None
    ) -> bool:
        pass

    @abstractmethod
    def signer_address(
        self,
        args: ArgsSignerAddress,
        client: InvokerClient,
        env: None
    ) -> Optional[str]:
        pass

    @abstractmethod
    def sign_message(
        self,
        args: ArgsSignMessage,
        client: InvokerClient,
        env: None
    ) -> str:
        pass

    @abstractmethod
    def sign_transaction(
        self,
        args: ArgsSignTransaction,
        client: InvokerClient,
        env: None
    ) -> str:
        pass

