from typing import TYPE_CHECKING
from uuid import UUID

from clipped.utils.json import orjson_dumps

if TYPE_CHECKING:
    from clipped.compact.pydantic import CallableGenerator


class GenericStr(str):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value, **kwargs):
        base_types = (int, float, dict, list, tuple, set)
        if isinstance(value, base_types):
            return orjson_dumps(value)
        if isinstance(value, str):
            return value
        if isinstance(value, UUID):
            return value.hex
        if value is None:
            return value
        try:
            return str(value)
        except Exception as e:
            field = kwargs.get("field")
            raise TypeError(
                f"Field `{field.name}` value must be a valid str or a value that can be casted to a str, received `{value}` instead."
            ) from e
