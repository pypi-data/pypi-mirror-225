from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from ..common.config_1_0 import (
    ConfigBase,
    ConfigurationZoneBase,
    DeviceBase,
    KeyConfigurations,
    Reserved,
    SlotConfigurations,
)
from ..common.types import HexBytes, HexInt


@dataclass
class Ecc108ConfigZone(ConfigurationZoneBase):
    sn01: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "SN01",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
        },
    )
    sn8: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "SN8",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    i2c_enable: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "I2CEnable",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    i2c_address: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "I2CAddress",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    reserved: List[Reserved] = field(
        default_factory=list,
        metadata={
            "name": "Reserved",
            "type": "Element",
        },
    )
    otpmode: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "OTPMode",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    chip_mode: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "ChipMode",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    slot_configurations: Optional[SlotConfigurations] = field(
        default=None,
        metadata={
            "name": "SlotConfigurations",
            "type": "Element",
        },
    )
    use_flags: Optional["Ecc108ConfigZone.UseFlags"] = field(
        default=None,
        metadata={
            "name": "UseFlags",
            "type": "Element",
        },
    )
    update_counts: Optional["Ecc108ConfigZone.UpdateCounts"] = field(
        default=None,
        metadata={
            "name": "UpdateCounts",
            "type": "Element",
        },
    )
    last_key_use: Optional["Ecc108ConfigZone.LastKeyUse"] = field(
        default=None,
        metadata={
            "name": "LastKeyUse",
            "type": "Element",
        },
    )
    user_extra: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "UserExtra",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    selector: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "Selector",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    slot_locked: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "SlotLocked",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
        },
    )
    x509format: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "X509format",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){4}",
        },
    )
    key_configurations: Optional[KeyConfigurations] = field(
        default=None,
        metadata={
            "name": "KeyConfigurations",
            "type": "Element",
        },
    )

    @dataclass
    class UseFlags:
        use_flag: List["Ecc108ConfigZone.UseFlags.UseFlag"] = field(
            default_factory=list,
            metadata={
                "name": "UseFlag",
                "type": "Element",
            },
        )
        size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Size",
                "type": "Attribute",
            },
        )

        @dataclass
        class UseFlag:
            value: HexInt = field(
                default=None,
                metadata={
                    "required": True,
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
                },
            )
            index: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Index",
                    "type": "Attribute",
                },
            )

    @dataclass
    class UpdateCounts:
        update_count: List["Ecc108ConfigZone.UpdateCounts.UpdateCount"] = field(
            default_factory=list,
            metadata={
                "name": "UpdateCount",
                "type": "Element",
            },
        )
        size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Size",
                "type": "Attribute",
            },
        )

        @dataclass
        class UpdateCount:
            value: Optional[HexInt] = field(
                default=None,
                metadata={
                    "required": True,
                },
            )
            index: Optional[int] = field(
                default=None,
                metadata={
                    "name": "Index",
                    "type": "Attribute",
                },
            )

    @dataclass
    class LastKeyUse:
        value: HexBytes = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){16}",
            },
        )
        size: Optional[int] = field(
            default=None,
            metadata={
                "name": "Size",
                "type": "Attribute",
            },
        )


@dataclass
class Ecc108Device(DeviceBase):
    configuration_zone: Optional[Ecc108ConfigZone] = field(
        default=None,
        metadata={
            "name": "ConfigurationZone",
            "type": "Elements",
            "required": True,
            "sequence": 1,
        },
    )


@dataclass
class Ecc108Config(ConfigBase):
    class Meta:
        name = "ATECC108A"

    device: Optional[Ecc108Device] = field(
        default=None,
        metadata={
            "name": "Device",
            "type": "Element",
        },
    )
