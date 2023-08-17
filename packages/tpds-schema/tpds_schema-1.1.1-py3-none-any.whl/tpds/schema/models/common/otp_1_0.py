from dataclasses import field
from enum import Enum
from typing import Optional

from pydantic.dataclasses import dataclass

from ..common.types import HexBytes


class OtpZoneMode(Enum):
    PUBLIC = "Public"


@dataclass
class OtpZone:
    """The OTP zone of 64 bytes (512 bits) is part of the EEPROM array
    and can be used for read-only storage.

    It is organized as two blocks of 32 bytes each.
    """

    data: Optional["OtpZone.Data"] = field(
        default=None,
        metadata={
            "name": "Data",
            "type": "Element",
            "required": True,
        },
    )
    mode: Optional[OtpZoneMode] = field(
        default=None,
        metadata={
            "name": "Mode",
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class Data:
        value: HexBytes = field(
            default="",
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){64}",
            },
        )
        size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Size",
                "type": "Attribute",
                "required": True,
            },
        )
