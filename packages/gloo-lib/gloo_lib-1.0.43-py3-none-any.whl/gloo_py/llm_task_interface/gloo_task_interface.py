import datetime
import json
import sys
from textwrap import dedent, indent
import typing
from pydantic import BaseModel
from .clients import LLMClient, default_llm_client, LLMResponse
from typing import Any
from ..logging.base_logger import logger
from .editable import editable, yaml_editable
from .vars_manager import VarsManager

T = typing.TypeVar("T", bound=BaseModel)
U = typing.TypeVar("U", bound=BaseModel)


def get_field_type(class_and_field_str) -> typing.Tuple[bool, Any]:
    # Split the input string into class name and field name
    class_name_str, field_name_str = class_and_field_str.split(".", maxsplit=1)
    class_name_str = class_name_str + "Model"

    # Check all loaded modules
    for module in sys.modules.values():
        try:
            cls = getattr(module, class_name_str)
            if issubclass(cls, BaseModel):
                field_info = cls.__fields__.get(field_name_str)
                if field_info:
                    field_type = field_info.outer_type_
                    if (
                        hasattr(field_type, "__origin__")
                        and field_type.__origin__ is list
                    ):
                        # Return the type inside the list
                        return True, typing.get_args(field_type)[0]
                    else:
                        return False, field_type

        except AttributeError:
            pass

    raise ValueError(
        f"Class {class_name_str}.{field_name_str} not found in loaded modules"
    )


class GlooLLMTaskInterface(VarsManager):
    @editable
    @yaml_editable
    def prompt(self) -> str:
        raise NotImplementedError(
            "Missing an override_prompt method or prompt field in yaml"
        )

    @editable
    def name(self) -> str:
        # Return the name of the class
        return self.__class__.__name__

    @editable
    def llm_client(self) -> LLMClient:
        return default_llm_client()

    @editable
    def parser(self, model: type[T], raw_llm_response: str) -> T:
        json_response = self.load_json_as_object(
            # in case the user prefixes the response with
            # a variable, be robust to it.
            self.replace_vars(raw_llm_response, loops=1)
        )
        unaliased_json_object = self.revert_alias_mappings(json_response)
        return model.parse_obj(unaliased_json_object)

    #
    # The remaining are internal method.
    #
    def load_json_as_object(self, json_str: str) -> typing.Dict[str, typing.Any]:
        """
        Loads a string as a dict, and ensures all keys are strings.
        """
        response = json.loads(json_str)
        if not isinstance(response, dict):
            raise Exception("Could not parse json response")

        # Force all keys to be strings just in case.
        response = {str(k): v for k, v in response.items()}
        return response

    async def run(self, input_data: U, output_model: type[T], **kwargs) -> T:
        # Get the prompt template
        prompt = dedent(self.prompt().lstrip("\n"))
        raw_prompt_template = prompt

        prompt, used_template_vars = self.replace_prompt_vars(
            prompt, input_data, loops=100
        )

        # Run the task
        start_date = datetime.datetime.utcnow()
        llm_response = await kwargs.get("llm_client", self.llm_client()).generate(
            prompt=prompt
        )
        if not isinstance(llm_response, LLMResponse):
            await logger.log_llm_task_fail(
                task_name=self.name(),
                input=input_data,
                details={
                    "model_name": llm_response.client_options.model_name,
                    "provider": llm_response.client_options.provider_name,
                    "input": {
                        "prompt": {
                            "template": raw_prompt_template,
                            "template_args": used_template_vars,
                        },
                        "invocation_params": llm_response.client_options.model_config,
                    },
                    "output": None,
                },
                start_date=start_date,
                error_code=2,
                error_message=llm_response.error_details,
            )
            raise Exception(f"LLM Failed: {llm_response.error_details}")

        prompt_tokens = None
        total_tokens = None
        output_tokens = None
        if llm_response.metadata.token_usage:
            if llm_response.metadata.token_usage["prompt"]:
                prompt_tokens = llm_response.metadata.token_usage["prompt"]
            if llm_response.metadata.token_usage["total"]:
                total_tokens = llm_response.metadata.token_usage["total"]
            if llm_response.metadata.token_usage["generated"]:
                output_tokens = llm_response.metadata.token_usage["generated"]

        try:
            model = self.parser(output_model, llm_response.generated_text)
            await logger.log_llm_task_success(
                task_name=self.name(),
                input=input_data,
                output=model,
                details={
                    "model_name": llm_response.client_options.model_name,
                    "provider": llm_response.client_options.provider_name,
                    "input": {
                        "prompt": {
                            "template": raw_prompt_template,
                            "template_args": used_template_vars,
                        },
                        "invocation_params": llm_response.client_options.model_config,
                    },
                    "output": {
                        "raw_text": llm_response.generated_text,
                        "metadata": {
                            "logprobs": None,
                            "prompt_tokens": prompt_tokens,
                            "output_tokens": output_tokens,
                            "total_tokens": total_tokens,
                        },
                    },
                },
                start_date=start_date,
            )
            return model
        except Exception as e:
            print("------------------")
            print("PROMT")
            print(indent(prompt, "    "))
            print("------------------")
            print("LLM RESPONSE")
            print(indent(llm_response.generated_text, "    "))
            print("------------------")
            await logger.log_llm_task_fail(
                task_name=self.name(),
                input=input_data,
                details={
                    "model_name": llm_response.client_options.model_name,
                    "provider": llm_response.client_options.provider_name,
                    "input": {
                        "prompt": {
                            "template": raw_prompt_template,
                            "template_args": used_template_vars,
                        },
                        "invocation_params": llm_response.client_options.model_config,
                    },
                    "output": {
                        "raw_text": llm_response.generated_text,
                        "metadata": {
                            "logprobs": None,
                            "prompt_tokens": prompt_tokens,
                            "output_tokens": output_tokens,
                            "total_tokens": total_tokens,
                        },
                    },
                },
                start_date=start_date,
                error_code=3,
                error_message=f"Parsing failed: {e}",
            )
            raise Exception(f"Response parsing failed: {e}")


__all__ = ["GlooLLMTaskInterface"]
