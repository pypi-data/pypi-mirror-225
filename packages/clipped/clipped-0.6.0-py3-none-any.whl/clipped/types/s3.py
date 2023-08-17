from typing import TYPE_CHECKING, Any, Dict

from clipped.compact.pydantic import AnyUrl

if TYPE_CHECKING:
    from clipped.compact.pydantic import BaseConfig, ModelField


class S3Path(AnyUrl):
    allowed_schemes = {"s3"}

    __slots__ = ()

    @classmethod
    def validate(
        cls, value: Any, field: "ModelField", config: "BaseConfig"
    ) -> "AnyUrl":
        if isinstance(value, Dict):
            _value = value.get("bucket")
            if not _value:
                raise ValueError("Received a wrong bucket definition: %s", value)
            if "://" not in _value:
                _value = "s3://{}".format(_value)
            key = value.get("key")
            if key:
                _value = "{}/{}".format(_value, key)
            value = _value
        return super(S3Path, cls).validate(value=value, field=field, config=config)

    def to_param(self):
        return str(self)

    @property
    def structured(self):
        return dict(bucket=self.host, key=self.path.strip("/"))
