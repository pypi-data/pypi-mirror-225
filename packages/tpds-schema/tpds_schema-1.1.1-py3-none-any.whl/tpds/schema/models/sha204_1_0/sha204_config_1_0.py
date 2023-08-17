from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

__NAMESPACE__ = "https://www.microchip.com/schema/ATSHA204_Config_1.0"


class ComMode(Enum):
    TWI = "TWI"
    SWI = "SWI"


class OtpMode(Enum):
    SECRET = "Secret"
    PUBLIC = "Public"
    DERIVED = "Derived"


class SlotMode(Enum):
    PRIVATE = "Private"
    PUBLIC = "Public"
    RANDOM = "Random"
    SECRET = "Secret"
    DERIVED = "Derived"


@dataclass
class Sha204Config:
    class Meta:
        name = "SHA204_Format"
        # namespace = "https://www.microchip.com/schema/ATSHA204_Config_1.0"

    version: Optional[str] = field(
        default=None,
        metadata={
            "name": "Version",
            "type": "Element",
        },
    )
    part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartNumber",
            "type": "Element",
            "required": True,
        },
    )
    comm_method: Optional[ComMode] = field(
        default=None,
        metadata={
            "name": "Comm_Method",
            "type": "Element",
            "required": True,
        },
    )
    session_key_slot: Optional[str] = field(
        default=None,
        metadata={
            "name": "Session_Key_Slot",
            "type": "Element",
            "required": True,
            "pattern": r"[0-9a-fA-F]{1}",
        },
    )
    configuration: Optional["Sha204Config.Configuration"] = field(
        default=None,
        metadata={
            "name": "Configuration",
            "type": "Element",
            "required": True,
        },
    )
    slots: Optional["Sha204Config.Slots"] = field(
        default=None,
        metadata={
            "name": "Slots",
            "type": "Element",
            "required": True,
        },
    )
    otp: Optional["Sha204Config.Otp"] = field(
        default=None,
        metadata={
            "name": "OTP",
            "type": "Element",
            "required": True,
        },
    )

    @dataclass
    class Configuration:
        twi_address: Optional[str] = field(
            default=None,
            metadata={
                "name": "TWI_Address",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
            },
        )
        temp_offset: Optional[str] = field(
            default=None,
            metadata={
                "name": "Temp_Offset",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
            },
        )
        selector_mode: Optional[str] = field(
            default=None,
            metadata={
                "name": "SelectorMode",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
            },
        )
        user_extra: Optional[str] = field(
            default=None,
            metadata={
                "name": "UserExtra",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
            },
        )
        selector: Optional[str] = field(
            default=None,
            metadata={
                "name": "Selector",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
            },
        )

    @dataclass
    class Slots:
        slot: List["Sha204Config.Slots.Slot"] = field(
            default_factory=list,
            metadata={
                "name": "Slot",
                "type": "Element",
            },
        )

        @dataclass
        class Slot:
            number: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Number",
                    "type": "Element",
                    "required": True,
                    "pattern": r"[0-9a-fA-F]{1}",
                },
            )
            config: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Config",
                    "type": "Element",
                    "required": True,
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
                },
            )
            use_flag: Optional[str] = field(
                default=None,
                metadata={
                    "name": "UseFlag",
                    "type": "Element",
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
                },
            )
            update_count: Optional[str] = field(
                default=None,
                metadata={
                    "name": "UpdateCount",
                    "type": "Element",
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
                },
            )
            mode: Optional[SlotMode] = field(
                default=None,
                metadata={
                    "name": "Mode",
                    "type": "Element",
                    "required": True,
                },
            )
            host_target_key: Optional[str] = field(
                default=None,
                metadata={
                    "name": "HostTargetKey",
                    "type": "Element",
                    "required": True,
                },
            )
            sn_pad: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SnPad",
                    "type": "Element",
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*)+",
                },
            )
            data: Optional[str] = field(
                default=None,
                metadata={
                    "name": "Data",
                    "type": "Element",
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){32}|\s*([0-9a-fA-F]{2}\s*){64}|\s*",
                },
            )
            last_key_use: Optional[str] = field(
                default=None,
                metadata={
                    "name": "LastKeyUse",
                    "type": "Element",
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){16}",
                },
            )

    @dataclass
    class Otp:
        mode: Optional[OtpMode] = field(
            default=None,
            metadata={
                "name": "Mode",
                "type": "Element",
                "required": True,
            },
        )
        otp_mode: Optional[str] = field(
            default=None,
            metadata={
                "name": "OTP_Mode",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
            },
        )
        data: Optional[str] = field(
            default=None,
            metadata={
                "name": "Data",
                "type": "Element",
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){32}|\s*([0-9a-fA-F]{2}\s*){64}|\s*",
            },
        )
