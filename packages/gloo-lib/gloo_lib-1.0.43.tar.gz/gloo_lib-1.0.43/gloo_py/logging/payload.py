from enum import StrEnum
import typing

from ..env import GlooContext


class GlooTestContext(typing.TypedDict):
    test_cycle_id: str
    test_dataset_name: str
    test_case_name: str
    test_case_arg_name: str


class EventType(StrEnum):
    Log = "log"
    TaskLLM = "task_llm"
    TaskModel = "task_model"


class GlooTaskDescription(typing.TypedDict):
    created_at: str  # ISO8601
    tags: typing.List[str]
    chain_ids: typing.List[str]
    event_name: str
    event_type: EventType
    input: typing.Optional[typing.Any]
    input_type: typing.Optional[typing.Any]


class GlooTaskOutput(typing.TypedDict):
    latency_ms: int
    error_code: int
    error_metadata: typing.Optional[str]
    output: typing.Optional[typing.Any]
    output_type: typing.Optional[typing.Any]


#
# LLM Task
#
class GlooLLMTaskOutputMetadata(typing.TypedDict):
    logprobs: typing.Any
    prompt_tokens: typing.Optional[int]
    output_tokens: typing.Optional[int]
    total_tokens: typing.Optional[int]


class GlooLLMTaskOutput(typing.TypedDict):
    raw_text: str
    metadata: GlooLLMTaskOutputMetadata


class GlooLLMTaskInputPrompt(typing.TypedDict):
    template: str
    template_args: typing.Dict[str, typing.Any]


class GlooLLMTaskInput(typing.TypedDict):
    prompt: GlooLLMTaskInputPrompt
    invocation_params: typing.Dict[str, typing.Any]


class GlooLLMTaskDetails(typing.TypedDict):
    model_name: str
    provider: str
    output: typing.Optional[GlooLLMTaskOutput]
    input: GlooLLMTaskInput


#
# Common Payload
#


class GlooLoggerPayload(GlooTaskOutput, GlooContext, GlooTaskDescription):
    event_id: str
    task_llm: typing.Optional[GlooLLMTaskDetails]
    task_model: typing.Optional[typing.Any]
