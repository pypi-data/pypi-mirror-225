from typing import TYPE_CHECKING, Any, Dict

from clipped.compact.pydantic import AnyUrl

if TYPE_CHECKING:
    from clipped.compact.pydantic import BaseConfig, ModelField


class Uri(AnyUrl):
    __slots__ = ()

    @classmethod
    def validate(
        cls, value: Any, field: "ModelField", config: "BaseConfig"
    ) -> "AnyUrl":
        if isinstance(value, Dict):
            _value = value.get("user")
            if not _value:
                raise ValueError("Received a wrong bucket definition: %s", value)
            password = value.get("password")
            if password:
                _value = "{}@{}".format(_value, password)
            host = value.get("host")
            if not host:
                raise ValueError("Received a wrong bucket definition: %s", value)
            _value = "{}/{}".format(_value, host)
            value = _value
        return super(Uri, cls).validate(value=value, field=field, config=config)

    def to_param(self):
        return str(self)

    @property
    def host_port(self):
        value = self.host
        if self.port:
            value = "{}:{}".format(value, self.port)
        if self.scheme:
            value = "{}://{}".format(self.scheme, value)
        return value


V1UriType = Uri
