from typing import TYPE_CHECKING

from clipped.utils.lists import to_list

if TYPE_CHECKING:
    from clipped.compact.pydantic import CallableGenerator


class ListStr(list):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value, **kwargs):
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return to_list(value, check_none=True, check_str=True)
        if not value:
            return value

        field = kwargs.get("field")
        raise TypeError(
            f"Field `{field.name}` value must be a valid List, received `{value}` instead."
        )
