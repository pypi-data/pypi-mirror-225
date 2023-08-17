import typing
from .llm_client import (
    LLMClientOptions,
    LLMResponse,
    LLMFailureResponse,
    LLMClient,
    LLMTokenUsage,
)
from .openai_llm_client import OpenAILLMClient
from .azure_openai_llm_client import AzureOpenAILLMClient


_default_client: LLMClient = OpenAILLMClient(
    model_name="gpt-3.5-turbo", temperature=0.0
)

T = typing.TypeVar("T", bound=LLMClient)


def default_llm_client() -> LLMClient:
    return _default_client


def set_default_llm_client(client: T):
    global _default_client
    _default_client = client


__all__ = [
    "LLMClient",
    "OpenAILLMClient",
    "default_llm_client",
    "set_default_llm_client",
]
