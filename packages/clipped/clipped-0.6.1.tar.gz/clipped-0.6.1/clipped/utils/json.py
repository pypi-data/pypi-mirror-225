from typing import Any, Callable, Optional

import orjson


def orjson_dumps(
    obj: Any,
    *,
    option: Optional[int] = orjson.OPT_SERIALIZE_NUMPY,
    default: Optional[Callable[[Any], Any]] = None,
) -> str:
    return orjson.dumps(obj, default=default, option=option).decode()


orjson_loads = orjson.loads
orjson_pprint_option = (
    orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
)
