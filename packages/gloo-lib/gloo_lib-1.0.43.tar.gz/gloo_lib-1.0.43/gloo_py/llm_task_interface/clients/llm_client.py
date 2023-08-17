from abc import ABC, abstractmethod
from textwrap import indent
import time
import typing

from pydantic import BaseModel

import logging
from termcolor import colored

from ...env import msg


class LLMClientOptions(BaseModel):
    provider_name: str
    model_name: str
    model_config: typing.Dict[str, typing.Any]


class LLMResponseBase(BaseModel):
    success: bool
    latency_ms: int
    client_options: LLMClientOptions


class LLMFailureResponse(LLMResponseBase):
    success: bool = False
    error: str
    error_details: str


class LLMTokenUsage(typing.TypedDict):
    total: int
    prompt: int
    generated: int


class LLMMetadata(BaseModel):
    token_usage: typing.Optional[LLMTokenUsage]


class LLMResponse(LLMResponseBase):
    success: bool = True
    generated_text: str
    metadata: LLMMetadata


class LLMClient(ABC):
    def __init__(self, options: LLMClientOptions) -> None:
        super().__init__()
        self.__options = options

    @property
    def options(self) -> LLMClientOptions:
        return self.__options

    @abstractmethod
    async def _generate_impl(
        self, prompt: str
    ) -> typing.Tuple[str, LLMMetadata, LLMClientOptions]:
        raise NotImplementedError

    async def generate(self, prompt: str) -> LLMResponse | LLMFailureResponse:
        start = time.time()
        try:
            msg("[GLOO] Prompt\n" + colored(indent(prompt, "    "), 'blue'))
            [response, usage, options] = await self._generate_impl(prompt)
            msg("[GLOO] Response\n" + colored(indent(response, "    "), 'green'))
            return LLMResponse(
                client_options=options,
                success=True,
                generated_text=response,
                metadata=usage,
                latency_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            return LLMFailureResponse(
                client_options=self.options,
                success=False,
                error=str(type(e)),
                error_details=str(e),
                latency_ms=int((time.time() - start) * 1000),
            )


__all__ = [
    "LLMClientOptions",
    "LLMResponse",
    "LLMFailureResponse",
    "LLMClient",
    "LLMTokenUsage",
]
