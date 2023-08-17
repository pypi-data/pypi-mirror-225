from typing import Any

from xsdata.formats.converter import Converter, converter


class HexInt(int):
    """
    Wraps int to indicate that it is represented as a hex byte - Uppercase
    """


class HexIntLower(HexInt):
    """
    Wraps int to indicate that it is represented as a hex byte - Lowercase
    """


class HexIntConverter(Converter):
    def deserialize(self, value: Any, **kwargs: Any) -> Any:
        return HexIntLower(int(value, 16)) if value.islower() else HexInt(int(value, 16))

    def serialize(self, value: Any, **kwargs: Any) -> str:
        return f"{value:02x}" if isinstance(value, HexIntLower) else f"{value:02X}"


converter.register_converter(HexInt, HexIntConverter())


class HexBytes(bytes):
    """
    Wraps bytes to indicate that they are represented as a hex string - Uppercase
    """


class HexBytesLower(HexBytes):
    """
    Wraps bytes to indicate that they are represented as a hex string - Lowercase
    """


class HexBytesConverter(Converter):
    def deserialize(self, value: Any, **kwargs: Any) -> Any:
        return (
            HexBytesLower(bytes.fromhex(value))
            if value.islower()
            else HexBytes(bytes.fromhex(value))
        )

    def serialize(self, value: Any, **kwargs: Any) -> str:
        step = 16

        def make_hex_string(data):
            result = " ".join([f"{v:02X}" for v in data])
            return result.lower() if isinstance(value, HexBytesLower) else result

        if len(value) > 16:
            return (
                "\n"
                + "\n".join(
                    [make_hex_string(value[i : i + step]) for i in range(0, len(value), step)]
                )
                + "\n"
            )
        else:
            return make_hex_string(value)


converter.register_converter(HexBytes, HexBytesConverter())

__all__ = ["HexInt", "HexBytes"]
