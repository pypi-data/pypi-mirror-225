from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from ..common.config_1_0 import (
    ConfigBase,
    ConfigurationZoneBase,
    Counter,
    DeviceBase,
    KeyConfigurations,
    Reserved,
    SlotConfigurations,
)
from ..common.types import HexBytes, HexInt


@dataclass
class Ecc508ConfigZone(ConfigurationZoneBase):
    """
    :ivar sn01:
    :ivar sn8:
    :ivar i2_cenable: Serial number byte 8. Also called the
        manufacturer ID.
    :ivar i2_caddress: Set to 01 for I2C mode or 00 for Single
        Wire (SWI) mode.
    :ivar reserved: Set by Microchip
    :ivar otpmode:
    :ivar chip_mode:
    :ivar slot_configurations:
    :ivar counter0:
    :ivar counter1:
    :ivar last_key_use:
    :ivar user_extra:
    :ivar selector:
    :ivar slot_locked: LockValue and LockConfig are not
        specified.
    :ivar x509format:
    :ivar key_configurations:
    """

    sn01: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "SN01",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
        },
    )
    sn8: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "SN8",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    i2c_enable: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "I2CEnable",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    i2c_address: List[HexInt] = field(
        default_factory=list,
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
    otpmode: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "OTPMode",
            "type": "Element",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    chip_mode: Optional[HexInt] = field(
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
    counter0: Optional[Counter] = field(
        default=None,
        metadata={
            "name": "Counter0",
            "type": "Element",
        },
    )
    counter1: Optional[Counter] = field(
        default=None,
        metadata={
            "name": "Counter1",
            "type": "Element",
        },
    )
    last_key_use: Optional["Ecc508ConfigZone.LastKeyUse"] = field(
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
    class LastKeyUse:
        value: str = field(
            default="",
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
class Ecc508Device(DeviceBase):
    configuration_zone: Optional[Ecc508ConfigZone] = field(
        default=None,
        metadata={
            "name": "ConfigurationZone",
            "type": "Element",
            "required": True,
            "sequence": 1,
        },
    )


@dataclass
class Ecc508Config(ConfigBase):
    """
    :ivar xmlversion:
    :ivar part_number: Personalization config file format version
    :ivar device: Part number for this configuration
    :ivar compressed_certs:
    :ivar extensions:
    """

    class Meta:
        name = "ATECC508A"

    device: Optional[Ecc508Device] = field(
        default=None,
        metadata={
            "name": "Device",
            "type": "Element",
            "required": True,
            "sequence": 3,
        },
    )
