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
class Ecc608ConfigZone(ConfigurationZoneBase):
    """
    :ivar sn01: Part of the serial number value.
    :ivar sn8: Part of the serial number value.
    :ivar aesenable: 0 = The AES command and AES mode of the KDF
        command are disabled. 1 = The AES operations are
        enabled.
    :ivar i2_cenable: 0 = The device operates in Single-Wire
        Interface mode. 1 = The device operates in I2C interface
        mode.
    :ivar i2_caddress: When I2C_Enable is one, this field is the
        I2C_Address with a default value of 0xC0. When I2C_Enabl
        is zero the chip operates in single wire mode and this
        field controls the GPIO function.
    :ivar reserved: Set by Microchip
    :ivar count_match: The counter match function in the
        ATECC608A provides a mechanism of altering the limit to
        which the first monotonic counter (Counter 0) can be
        incremented. Key usage can be connected to Counter [0]
        (See Section 4.4.5 High Endurance Monotonic Counters) to
        prevent use of that key when the counter is at its
        limit.
    :ivar chip_mode: This byte controls some of the basic timing
        and I/O function of the device.
    :ivar slot_configurations: The 16 SlotConfig elements are
        used to configure the access protections for each of the
        16 slots within the ATECC608A device. Each configuration
        element consists of 16 bits, which control the usage and
        access for that particular slot or key.
    :ivar counter0: Monotonic counter that can optionally be
        connected to keys via the SlotConfig.
    :ivar counter1: Second monotonic counter, not connected to
        any keys.
    :ivar use_lock: Configuration for transport locking.
    :ivar volatile_key_permission: This byte controls the
        volatile permission function of the ATECC608A. When this
        function is enabled for a particular key slot, general
        purpose use of that slot will be prohibited until
        cryptographically enabled. The permission status is
        stored in the persistent latch and is retained during
        sleep, idle and active modes.
    :ivar secure_boot: This byte controls the special secure
        boot functionality of the device.
    :ivar kdf_iv_loc: Index within the KDF(HKDF) input string
        where the two bytes stored below (KdfIvStr) should be
        found.
    :ivar kdf_iv_str: Two byte KDF IV string that must be found
        in the KDF message for the KDF(HKDF) special IV mode.
    :ivar user_extra: One byte value that can be modified via
        the UpdateExtra command after the Data zone has been
        locked. Can be written via UpdateExtra only if it has a
        value of zero.
    :ivar user_extra_add: This byte will be the I2C address of
        the device, if I2C_Enable is one, ChipMode is one and
        the value of this byte is != 0x00. If the value is 0x00,
        then this value can be written via the UpdateExtra
        command. If the ChipMode is zero, then this byte will
        have no effect on the I2C address if modified.
    :ivar slot_locked: A single bit for each slot. If the bit
        corresponding to a particular slot is zero, the contents
        of the slot cannot be modified under any circumstances.
    :ivar chip_options:
    :ivar x509format: X.509 certificate validation formatting.
    :ivar key_configurations: Two bytes of additional access and
        usage permissions and controls for each slot of the Data
        zone
    """

    sn01: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "SN01",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
        },
    )
    sn8: Optional[str] = field(
        default=None,
        metadata={
            "name": "SN8",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    aes_enable: Optional[str] = field(
        default=None,
        metadata={
            "name": "AESEnable",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    i2c_enable: Optional[str] = field(
        default=None,
        metadata={
            "name": "I2CEnable",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    i2c_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "I2CAddress",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    reserved: list[Reserved] = field(
        default_factory=list,
        metadata={
            "name": "Reserved",
        },
    )
    count_match: Optional[str] = field(
        default=None,
        metadata={
            "name": "CountMatch",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    chip_mode: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChipMode",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    slot_configurations: List[SlotConfigurations] = field(
        default_factory=list,
        metadata={
            "name": "SlotConfigurations",
        },
    )
    counter0: Optional[Counter] = field(
        default_factory=list,
        metadata={
            "name": "Counter0",
        },
    )
    counter1: List[Counter] = field(
        default_factory=list,
        metadata={
            "name": "Counter1",
        },
    )
    use_lock: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "UseLock",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    volatile_key_permission: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "VolatileKeyPermission",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    secure_boot: Optional["Ecc608ConfigZone.SecureBoot"] = field(
        default=None,
        metadata={
            "name": "SecureBoot",
        },
    )
    kdf_iv_loc: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "KdfIvLoc",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    kdf_iv_str: Optional["Ecc608ConfigZone.KdfIvStr"] = field(
        default=None,
        metadata={
            "name": "KdfIvStr",
        },
    )
    user_extra: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "UserExtra",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    user_extra_add: Optional[HexInt] = field(
        default=None,
        metadata={
            "name": "UserExtraAdd",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){1}",
        },
    )
    slot_locked: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "SlotLocked",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
        },
    )
    chip_options: Optional["Ecc608ConfigZone.ChipOptions"] = field(
        default=None,
        metadata={
            "name": "ChipOptions",
        },
    )
    x509format: Optional[HexBytes] = field(
        default=None,
        metadata={
            "name": "X509format",
            "pattern": r"\s*([0-9a-fA-F]{2}\s*){4}",
        },
    )
    key_configurations: List[KeyConfigurations] = field(
        default_factory=list,
        metadata={
            "name": "KeyConfigurations",
        },
    )

    @dataclass
    class SecureBoot:
        value: str = field(
            default="",
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
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
    class KdfIvStr:
        value: HexBytes = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
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
    class ChipOptions:
        value: HexBytes = field(
            default=None,
            metadata={
                "required": True,
                "pattern": r"\s*([0-9a-fA-F]{2}\s*){2}",
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
class Ecc608Device(DeviceBase):
    configuration_zone: Optional[Ecc608ConfigZone] = field(
        default=None,
        metadata={
            "name": "ConfigurationZone",
            "type": "Elements",
            "required": True,
            "sequence": 1,
        },
    )


@dataclass
class Ecc608Config(ConfigBase):
    class Meta:
        name = "ATECC608"

    device: Optional[Ecc608Device] = field(
        default=None,
        metadata={
            "name": "Device",
            "type": "Element",
            "required": True,
            "sequence": 3,
        },
    )
