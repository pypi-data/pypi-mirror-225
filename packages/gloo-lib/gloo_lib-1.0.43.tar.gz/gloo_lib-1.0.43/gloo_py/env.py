import os
from typing import Optional, Dict
import typing
import uuid

from termcolor import colored


class GlooContext(typing.TypedDict):
    project_id: str
    session_id: str
    hostname: str
    stage: str


__context: typing.Optional[GlooContext] = None


def clear_context():
    global __context
    __context = None


def base_context() -> GlooContext:
    global __context
    if __context is None:
        __context = {
            "project_id": global_project_id(),
            "stage": global_stage(),
            "session_id": str(uuid.uuid4()),
            "hostname": os.uname().nodename,
        }
    return __context


class GlooConfig:
    _config_data: Dict[str, Optional[str]]

    def __init__(self):
        self._config_data = {
            "gloo_project_id": os.environ.get("gloo_project_id", None),
            "gloo_api_key": None,
            "gloo_stage": "dev",
            # "gloo_service": "http://localhost:3000/api",
            "gloo_service": "https://app.trygloo.com/api",
            "openai_api_key": None,
            "log_level": "silent",
        }

    def get(self, key: str) -> str:
        value = self._config_data.get(key)
        if value is None:
            raise ValueError(f"{key} has not been set!")
        return value

    def set(self, key: str, value: Optional[str]) -> None:
        if key in self._config_data:
            self._config_data[key] = value


_default_config = GlooConfig()


def msg(msg: str, color: Optional[str] = None) -> None:
    if _default_config.get("log_level") == "silent":
        return
    if color:
        msg = colored(msg, color)
    print(msg)


def init_gloo(
    gloo_project_id: Optional[str] = None,
    gloo_api_key: Optional[str] = None,
    gloo_stage: Optional[str] = None,
    gloo_service: Optional[str] = None,
    openai_api_key: Optional[str] = None,
    log_level: Optional[str] = None,
) -> None:
    """
    Initialize Gloo settings.
    """
    updates = {
        "gloo_project_id": gloo_project_id,
        "gloo_api_key": gloo_api_key,
        "gloo_stage": gloo_stage,
        "gloo_service": gloo_service,
        "openai_api_key": openai_api_key,
        "log_level": log_level,
    }
    for key, value in updates.items():
        if value:
            _default_config.set(key, value)
    clear_context()


def global_project_id() -> str:
    return _default_config.get("gloo_project_id")


def global_openai_api_key() -> str:
    return _default_config.get("openai_api_key")


def global_api_key() -> str:
    return _default_config.get("gloo_api_key")


def global_stage() -> str:
    return _default_config.get("gloo_stage")


def global_gloo_service() -> str:
    return _default_config.get("gloo_service")


__all__ = ["init_gloo", "global_project_id", "global_api_key", "global_openai_api_key"]
