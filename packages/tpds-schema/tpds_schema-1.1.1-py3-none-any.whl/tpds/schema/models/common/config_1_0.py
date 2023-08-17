from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass

from ..common.cert_def_1_0 import CompressedCerts
from ..common.data_1_0 import DataZone
from ..common.extension_1_0 import Extensions
from ..common.otp_1_0 import OtpZone
from ..common.types import HexBytes


@dataclass
class Reserved:
    value: HexBytes = field(
        default=None,
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*)+",
        },
    )
    address: Optional[int] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Attribute",
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
class Counter:
    value: HexBytes = field(
        default=None,
        metadata={
            "required": True,
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){8}",
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
class SlotConfigurations:
    slot_configuration: List["SlotConfigurations.SlotConfiguration"] = field(
        default_factory=list,
        metadata={
            "name": "SlotConfiguration",
            "type": "Element",
            "min_occurs": 1,
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

    @dataclass
    class SlotConfiguration:
        value: HexBytes = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
            },
        )
        index: Optional[str] = field(
            default=None,
            metadata={
                "name": "Index",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass
class KeyConfigurations:
    key_configuration: List["KeyConfigurations.KeyConfiguration"] = field(
        default_factory=list,
        metadata={
            "name": "KeyConfiguration",
            "type": "Element",
            "min_occurs": 1,
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

    @dataclass
    class KeyConfiguration:
        value: HexBytes = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
            },
        )
        index: Optional[str] = field(
            default=None,
            metadata={
                "name": "Index",
                "type": "Attribute",
                "required": True,
                "pattern": r"[0-9a-fA-F]{1}",
            },
        )


@dataclass
class ConfigurationZoneBase:
    pass


@dataclass
class DeviceBase:
    """
    :ivar configuration_zone: Configuration zone contents are
        specified in this element.
    :ivar data_zone:
    :ivar otpzone:
    """

    configuration_zone: Optional[ConfigurationZoneBase] = field(
        default=None,
        metadata={
            "name": "ConfigurationZone",
            "type": "Element",
            "required": True,
            "sequence": 1,
        },
    )
    data_zone: Optional[DataZone] = field(
        default=None,
        metadata={
            "name": "DataZone",
            "type": "Element",
            "required": True,
            "sequence": 2,
        },
    )
    otpzone: Optional[OtpZone] = field(
        default=None,
        metadata={
            "name": "OTPZone",
            "type": "Element",
            "required": True,
            "sequence": 3,
        },
    )


@dataclass
class ConfigBase:
    """
    :ivar xmlversion:
    :ivar part_number: Personalization config file format version
    :ivar device: Part number for this configuration
    :ivar compressed_certs:
    :ivar extensions:
    """

    xmlversion: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "XMLVersion",
            "type": "Element",
            "required": True,
            "sequence": 1,
        },
    )
    part_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PartNumber",
            "type": "Element",
            "required": True,
            "sequence": 2,
        },
    )
    device: Optional[DeviceBase] = field(
        default=None,
        metadata={
            "name": "Device",
            "type": "Element",
            "required": True,
            "sequence": 3,
        },
    )
    compressed_certs: Optional[CompressedCerts] = field(
        default=None,
        metadata={
            "name": "CompressedCerts",
            "type": "Element",
            "sequence": 4,
        },
    )
    extensions: Optional[Extensions] = field(
        default=None,
        metadata={
            "name": "Extensions",
            "type": "Element",
            "sequence": 5,
        },
    )
