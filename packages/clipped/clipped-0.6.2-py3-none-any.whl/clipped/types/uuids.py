from typing import TYPE_CHECKING
from uuid import UUID

from clipped.compact.pydantic import StrictStr

if TYPE_CHECKING:
    from clipped.compact.pydantic import CallableGenerator


class UUIDStr(StrictStr):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value, **kwargs):
        if isinstance(value, str):
            return UUID(value).hex
        if isinstance(value, UUID):
            return value.hex
        if not value:
            return value

        field = kwargs.get("field")
        raise TypeError(
            f"Field `{field.name}` value must be a valid UUID, received `{value}` instead."
        )
