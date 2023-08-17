from enum import StrEnum
import json
import re
import sys
import typing

from pydantic import BaseModel

from flatten_json import flatten
from gloo_py.llm_task_interface.alias_mapping import (
    AliasMapper,
    FieldTypeDefinition,
    get_field_type,
)
from .editable import editable, yaml_editable


class FieldVars:
    def __init__(self, name: str):
        self.__name = f"{{{name}.alias}}"
        self.desc = f"{{{name}.dfn}}"

    def __str__(self) -> str:
        return self.__name


class FieldDefinition(typing.TypedDict):
    alias: str
    definition: str


class EnumFieldDefinition(FieldDefinition):
    case_name_formatter: typing.Callable[[str], str]
    case_formatter: typing.Callable[[str, str], str]
    cases: typing.Any


TaskDescription = typing.Dict[str, typing.Dict[str, FieldDefinition]]
T = typing.TypeVar("T", bound=BaseModel)


class VarsManager:
    @editable
    @yaml_editable
    def output_definitions(self) -> TaskDescription:
        raise NotImplementedError("Missing an override_output_definitions method")

    @editable
    @yaml_editable
    def static_vars(self) -> typing.Dict[str, str]:
        return dict()

    @editable
    def input_vars(self, obj: T) -> typing.Dict[str, str]:
        return flatten(obj.dict(), separator=".")

    def replace_prompt_vars(
        self,
        string: str,
        input: T,
        loops: int,
    ) -> typing.Tuple[str, typing.Dict[str, str]]:
        """
        Replaces all variables in a string with their values.
        """
        _vars, orig_vars, prev_used_vars = self._all_vars()
        _input_vars = self.input_vars(input)
        used_vars = set()

        # inform if any _input_vars would overwrite _vars
        overlapping_vars = set(_input_vars.keys()).intersection(set(_vars.keys()))
        if overlapping_vars:
            raise ValueError(
                f"Some variables are being overwritten. Consider renaming them: {overlapping_vars}"
            )

        all_vars = {
            **_vars,
            **self.input_vars(input),
        }

        def update_string(s: str) -> typing.Tuple[str, bool]:
            # First detect all vars in the string
            required_vars = set(re.findall(r"\{([a-zA-Z0-9_\.]+)\}", s))

            if not required_vars:
                return s, False

            # See which vars not in our list of vars
            missing_vars = required_vars - set(all_vars.keys())
            if missing_vars:
                raise ValueError(
                    f"Using variables that are not defined: {missing_vars}"
                )

            for _r in required_vars:
                used_vars.add(_r)
                r = f"{{{_r}}}"
                s = s.replace(r, all_vars[_r])
            return s, True

        updated_string, vars_left = update_string(string)
        while vars_left and loops > 0:
            updated_string, vars_left = update_string(updated_string)
            loops -= 1

        if vars_left:
            remaining_vars = set(re.findall(r"\{([a-zA-Z0-9_\.]+)\}", updated_string))
            if remaining_vars:
                raise ValueError(
                    f"Could not resolve all variables in string: {remaining_vars}"
                )

        # used_vars should recursively include all prev used vars.
        all_used_vars = set()
        for k in used_vars:
            all_used_vars.add(k)
            all_used_vars.update(prev_used_vars.get(k, set()))

        return updated_string, {k: orig_vars.get(k, all_vars[k]) for k in all_used_vars}

    def replace_vars(self, string: str, loops: int) -> str:
        all_vars, _, _ = self._all_vars()

        def update_string(s: str) -> typing.Tuple[str, bool]:
            # First detect all vars in the string
            required_vars = set(re.findall(r"\{([a-zA-Z0-9_\.]+)\}", s))

            if not required_vars:
                return s, False

            # See which vars not in our list of vars
            missing_vars = required_vars - set(all_vars.keys())
            if missing_vars:
                raise ValueError(
                    f"Using variables that are not defined: {missing_vars}"
                )

            for _r in required_vars:
                r = f"{{{_r}}}"
                s = s.replace(r, all_vars[_r])
            return s, True

        updated_string, vars_left = update_string(string)
        while vars_left and loops > 0:
            updated_string, vars_left = update_string(updated_string)
            loops -= 1

        if vars_left:
            remaining_vars = set(re.findall(r"\{([a-zA-Z0-9_\.]+)\}", updated_string))
            if remaining_vars:
                raise ValueError(
                    f"Could not resolve all variables in string: {remaining_vars}"
                )

        return updated_string

    def revert_alias_mappings(
        self, obj: typing.Dict[str, typing.Any]
    ) -> typing.Dict[str, typing.Any]:
        """
        Replaces all key aliases with their original names.
        """
        return AliasMapper(
            _alias_replacer=self._replacer_alias_to_field(),
            _field_types=self._field_types(),
        ).update_alias(obj)

    def _all_vars(
        self,
    ) -> typing.Tuple[
        typing.Dict[str, str], typing.Dict[str, str], typing.Dict[str, typing.Set[str]]
    ]:
        all_vars = {
            **self._replacer_field_alias(),
            **self._replacer_field_description(),
            **self._replacer_object_json(),
            **self._replacer_cases(),
            **self.static_vars(),
        }

        static_vars = {k: v for k, v in all_vars.items()}
        used_vars: typing.Dict[str, typing.Set[str]] = {
            k: set() for k in static_vars.keys()
        }

        def update_string(s: str) -> typing.Tuple[str, typing.Set[str]]:
            # First detect all vars in the string
            required_vars = set(re.findall(r"\{([a-zA-Z0-9_\.]+)\}", s))
            # only look for vars which are keys in all_vars
            # Just in case you use the input in some value.
            required_vars = required_vars.intersection(all_vars.keys())

            if not required_vars:
                return s, required_vars

            for r in required_vars:
                s = s.replace(f"{{{r}}}", all_vars[r])
            return s, required_vars

        requires_mapping = {k: True for k in all_vars.keys()}
        max_loops = 100
        while any(requires_mapping.values()) and max_loops > 0:
            for k, v in requires_mapping.items():
                if v:
                    all_vars[k], used = update_string(all_vars[k])
                    used_vars[k].update(used)
                    requires_mapping[k] = bool(used)
            max_loops -= 1

        if max_loops == 0 and any(requires_mapping.values()):
            missing_values = "\n".join(
                map(
                    lambda kv: f"{kv[0]}: {all_vars[kv[0]]}",
                    filter(lambda kv: kv[1], requires_mapping.items()),
                )
            )
            raise ValueError(
                f"Some variables could not be resolved and may be recursively defined: {missing_values}"
            )
        return all_vars, static_vars, used_vars

    def _replacer_cases(self) -> typing.Dict[str, str]:
        """
        Returns a dict of field aliases.
        """
        cases = {
            f"{k}.cases": "\n".join(
                [f"{{{k}.{_v}.alias}}: {{{k}.{_v}.dfn}}" for _v in v["cases"].keys()]
            )
            for k, v in self._enum_defs
        }
        cases.update(
            {
                f"{k}.case_names": ", ".join(
                    [f"{{{k}.{_v}.alias}}" for _v in v["cases"].keys()]
                )
                for k, v in self._enum_defs
            }
        )

        return cases

    def _replacer_alias_to_field(self) -> typing.Dict[str, str]:
        field_to_alias = self._replacer_field_alias()

        # Reverse the field_names dict. If there are any duplicates, warn the user.
        alias_to_name = {}
        duplicate_aliases = set()
        for _k, v in field_to_alias.items():
            if not _k.endswith(".alias"):
                raise ValueError(f"Expected key to end with '.alias': {_k}")
            k = _k[: -len(".alias")]

            if v in alias_to_name:
                duplicate_aliases.add(k)

            # For deeply nested objects, only gets the last part of the key
            alias_to_name[v] = k
        return alias_to_name

    @property
    def _object_defs(self):
        target_keys = set(
            ["cases", "case_name_formatter", "case_formatter", "alias", "definition"]
        )
        for k, v in self.output_definitions().items():
            # Check if v is EnumFieldDefinition
            if isinstance(v, dict) and set(v.keys()) == target_keys:
                continue
            yield k, typing.cast(typing.Dict[str, FieldDefinition], v)

    @property
    def _enum_defs(self):
        target_keys = set(
            ["cases", "case_name_formatter", "case_formatter", "alias", "definition"]
        )
        for k, v in self.output_definitions().items():
            # Check if v is EnumFieldDefinition
            if isinstance(v, dict) and set(v.keys()) == target_keys:
                yield k, typing.cast(EnumFieldDefinition, v)

    def _replacer_field_alias(self) -> typing.Dict[str, str]:
        """
        Returns a dict of field aliases.
        """
        aliases = {
            f"{k}.{_k}.alias": _v["alias"]
            for k, v in self._object_defs
            for _k, _v in v.items()
        }
        aliases.update({f"{k}.alias": v["alias"] for k, v in self._enum_defs})
        aliases.update(
            {
                f"{k}.{_v}.alias": df["alias"]
                for k, v in self._enum_defs
                for _v, df in v["cases"].items()
            }
        )

        return aliases

    def _field_types(self) -> typing.Dict[str, FieldTypeDefinition]:
        return {
            f"{k}.{_k}": get_field_type(f"{k}.{_k}")
            for k, v in self._object_defs
            for _k in v.keys()
        }

    def _replacer_field_description(self) -> typing.Dict[str, str]:
        """
        Returns a dict of field aliases.
        """
        dfns = {
            f"{k}.{_k}.dfn": _v["definition"]
            for k, v in self._object_defs
            for _k, _v in v.items()
        }
        dfns.update({f"{k}.dfn": v["definition"] for k, v in self._enum_defs})
        dfns.update(
            {
                f"{k}.{_v}.dfn": df["definition"]
                for k, v in self._enum_defs
                for _v, df in v["cases"].items()
            }
        )
        return dfns

    def _replacer_object_json(self) -> typing.Dict[str, str]:
        """
        Returns a dict of field aliases.
        """
        return {
            f"{k}.json": json.dumps(
                {f"{{{k}.{_k}.alias}}": f"{{{k}.{_k}.dfn}}" for _k in v.keys()}
            )
            for k, v in self._object_defs
        }
