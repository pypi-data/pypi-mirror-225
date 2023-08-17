from typing import TYPE_CHECKING

from pydantic.version import VERSION as PYDANTIC_VERSION

if PYDANTIC_VERSION.startswith("2."):
    from pydantic.v1 import (
        AnyUrl,
        BaseConfig,
        BaseModel,
        ByteSize,
        ConstrainedBytes,
        ConstrainedDate,
        ConstrainedDecimal,
        ConstrainedFloat,
        ConstrainedFrozenSet,
        ConstrainedInt,
        ConstrainedList,
        ConstrainedSet,
        ConstrainedStr,
        Extra,
        Field,
        FiniteFloat,
        FutureDate,
        Json,
        NegativeFloat,
        NegativeInt,
        NoneBytes,
        NoneStr,
        NoneStrBytes,
        NonNegativeFloat,
        NonNegativeInt,
        NonPositiveFloat,
        NonPositiveInt,
        PastDate,
        PaymentCardNumber,
        PositiveFloat,
        PositiveInt,
        PrivateAttr,
        PydanticTypeError,
        PydanticValueError,
        PyObject,
        SecretBytes,
        SecretField,
        SecretStr,
        StrBytes,
        StrictBool,
        StrictBytes,
        StrictFloat,
        StrictInt,
        StrictStr,
        ValidationError,
        constr,
        root_validator,
        validate_arguments,
        validator,
    )
    from pydantic.v1.datetime_parse import parse_date, parse_datetime, parse_duration
    from pydantic.v1.fields import ModelField
    from pydantic.v1.parse import Protocol, load_str_bytes
    from pydantic.v1.tools import NameFactory, _get_parsing_type
    from pydantic.v1.validators import strict_str_validator, uuid_validator

    if TYPE_CHECKING:
        from pydantic.v1.typing import CallableGenerator
else:
    from pydantic import (
        AnyUrl,
        BaseConfig,
        BaseModel,
        ByteSize,
        ConstrainedBytes,
        ConstrainedDate,
        ConstrainedDecimal,
        ConstrainedFloat,
        ConstrainedFrozenSet,
        ConstrainedInt,
        ConstrainedList,
        ConstrainedSet,
        ConstrainedStr,
        Extra,
        Field,
        FiniteFloat,
        FutureDate,
        Json,
        NegativeFloat,
        NegativeInt,
        NoneBytes,
        NoneStr,
        NoneStrBytes,
        NonNegativeFloat,
        NonNegativeInt,
        NonPositiveFloat,
        NonPositiveInt,
        PastDate,
        PaymentCardNumber,
        PositiveFloat,
        PositiveInt,
        PrivateAttr,
        PydanticTypeError,
        PydanticValueError,
        PyObject,
        SecretBytes,
        SecretField,
        SecretStr,
        StrBytes,
        StrictBool,
        StrictBytes,
        StrictFloat,
        StrictInt,
        StrictStr,
        ValidationError,
        constr,
        root_validator,
        validate_arguments,
        validator,
    )
    from pydantic.datetime_parse import parse_date, parse_datetime, parse_duration
    from pydantic.fields import ModelField
    from pydantic.parse import Protocol, load_str_bytes
    from pydantic.tools import NameFactory, _get_parsing_type
    from pydantic.validators import strict_str_validator, uuid_validator

    if TYPE_CHECKING:
        from pydantic.typing import CallableGenerator
