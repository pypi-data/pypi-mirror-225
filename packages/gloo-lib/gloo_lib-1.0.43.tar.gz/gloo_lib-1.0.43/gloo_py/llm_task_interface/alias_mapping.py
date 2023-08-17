from enum import StrEnum
import sys
import typing

from pydantic import BaseModel


class FieldTypeDefinition(BaseModel):
    is_list: bool
    type: typing.Type


def is_object_str_any(obj: typing.Any) -> bool:
    """
    Checks if an object is a valid json object.
    """
    return isinstance(obj, dict) and all(isinstance(k, str) for k in obj.keys())


def get_field_type(class_and_field_str: str) -> FieldTypeDefinition:
    """
    Returns the type of a field in a class.

    Returns:
        A tuple of (is_list, type). If is_list is True, then type is the type inside the list.
    """

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
                        return FieldTypeDefinition(
                            is_list=True, type=typing.get_args(field_type)[0]
                        )
                    else:
                        return FieldTypeDefinition(is_list=False, type=field_type)

        except AttributeError:
            pass

    raise ValueError(f"Not found in loaded modules: {class_and_field_str}")


class AliasMapper:
    def __init__(
        self,
        *,
        _alias_replacer: typing.Dict[str, str],
        _field_types: typing.Dict[str, FieldTypeDefinition],
    ) -> None:
        self._alias_replacer = _alias_replacer
        self._field_types = _field_types

    def _updated_key(
        self, k: str, v: typing.Any
    ) -> None | typing.Tuple[str, typing.Any]:
        if k not in self._alias_replacer:
            # TODO: Log that we ignored this key.
            # likely a hallucination.
            return None
        updated_field = self._alias_replacer[k]
        # update v to use the new key
        types = self._field_types[updated_field]

        list_types = (list, set, tuple)
        if issubclass(types.type, StrEnum):
            if not isinstance(v, list_types):
                v = [v]
            # TODO: This will throw an error if the value is not valid.
            # Make this respect aliases too.
            v = [
                types.type(self._alias_replacer.get(_v, _v).split(".")[-1]) for _v in v
            ]

        if types.is_list:
            if not isinstance(v, list_types):
                v = [v]
            return updated_field, [
                self.update_alias(_v) if is_object_str_any(_v) else _v for _v in v
            ]
        else:
            if isinstance(v, list_types):
                unused: typing.List[typing.Any] = []
                next_v = None
                for _v in v:
                    if next_v is not None:
                        unused.append(_v)
                        continue
                    next_v = _v
                # TODO: Log that we dropped some values.
                # Likely a hallucination.
                # print(f"Unused values: {unused}")
                v = next_v
            return updated_field, self.update_alias(v) if is_object_str_any(v) else v

    def update_alias(
        self, o: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        new_object = {}
        for _k, v in o.items():
            kv = self._updated_key(_k, v)
            if kv is None:
                continue
            k, v = kv
            new_object[k.split(".")[-1]] = v
        return new_object
