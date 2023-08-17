from typing import Any, Callable, TypeVar, cast

from functools import wraps

F = TypeVar("F", bound=Callable[..., Any])
F0 = TypeVar("F0", bound=Callable[[Any], Any])


def editable(func: F) -> F:
    @wraps(func)
    def wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
        # Get the edit version of the method_name
        edit_method_name = f"override_{func.__name__}"
        # Check if the method exists
        edit_method = getattr(instance, edit_method_name, None)
        if callable(edit_method):
            return edit_method(*args, **kwargs)
        return func(instance, *args, **kwargs)

    wrapper.__name__ = func.__name__
    return cast(F, wrapper)


def yaml_editable(func: F0) -> F0:
    @wraps(func)
    def wrapper(instance: Any) -> Any:
        # Get the edit version of the method_name
        edit_method_name = f"_from_yaml_{func.__name__}"
        # Check if the method exists
        edit_method = getattr(instance, edit_method_name, None)
        if edit_method and not callable(edit_method):
            return edit_method
        return func(instance)

    wrapper.__name__ = func.__name__
    return cast(F0, wrapper)


__all__ = ["editable", "yaml_editable"]
