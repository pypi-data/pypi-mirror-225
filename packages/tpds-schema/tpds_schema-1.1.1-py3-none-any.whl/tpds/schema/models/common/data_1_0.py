from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass

from .algo_1_0 import DataSlotAlgorithms
from .types import HexBytes


class DataZoneSlotMode(Enum):
    PRIV_WRITE = "PrivWrite"
    RANDOM = "Random"
    PRIVATE = "Private"
    PUBLIC = "Public"
    GEN_KEY = "GenKey"
    SIG_DATA = "SigData"
    SECRET = "Secret"
    DEVICE_PUB_KEY = "DevicePubKey"
    SIGNER_PUB_KEY = "SignerPubKey"
    SIGNER_SIG = "SignerSig"
    DEVICE_SIG = "DeviceSig"
    DERIVED = "Derived"
    SIGNER_SIG_DEVICE_SIG_SIG_DATA = "SignerSig DeviceSig SigData"
    SIGNER_PUB_KEY_SIGNER_SIG_SIG_DATA = "SignerPubKey SignerSig SigData"
    SIGNER_PUB_KEY_DEVICE_SIG_SIGNER_SIG = "SignerPubKey DeviceSig SignerSig"
    HKDF_EXPAND_SHA256 = "HKDF-Expand-SHA256"
    SKIP = "Skip"


@dataclass
class DataZone:
    """The Data zone is broken into 16 slots, for which access
    restrictions are individually programmable.

    While all slots can be used for private or secret keys or
    user data, only Slots 8 through 15 are large enough to store
    an ECC public key or ECDSA certificate/signature
    """

    slot: List["DataZone.Slot"] = field(
        default_factory=list,
        metadata={
            "name": "Slot",
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
    class Slot:
        data: Optional["DataZone.Slot.Data"] = field(
            default=None,
            metadata={
                "name": "Data",
                "type": "Element",
            },
        )
        info: Optional["DataZone.Slot.Info"] = field(
            default=None,
            metadata={
                "name": "Info",
                "type": "Element",
            },
        )
        snpad: Optional["DataZone.Slot.Snpad"] = field(
            default=None,
            metadata={
                "name": "SNPad",
                "type": "Element",
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
        mode: Optional[DataZoneSlotMode] = field(
            default=None,
            metadata={
                "name": "Mode",
                "type": "Attribute",
                "required": True,
            },
        )
        host_target_key: Optional[str] = field(
            default=None,
            metadata={
                "name": "HostTargetKey",
                "type": "Attribute",
                "pattern": r"[0-9a-fA-F]{1}",
            },
        )
        pub_slot: Optional[str] = field(
            default=None,
            metadata={
                "name": "PubSlot",
                "type": "Attribute",
                "pattern": r"[0-9a-fA-F]{1}|\s*([0-9a-fA-F]{1}\s*){2}",
            },
        )
        compressed_cert: Optional[str] = field(
            default=None,
            metadata={
                "name": "CompressedCert",
                "type": "Attribute",
                "pattern": r"[0-9a-fA-F]{1}|\s*([0-9a-fA-F]{1}\s*){2}",
            },
        )
        priv_slot: Optional[str] = field(
            default=None,
            metadata={
                "name": "PrivSlot",
                "type": "Attribute",
                "pattern": r"[0-9a-fA-F]{1}",
            },
        )

        @dataclass
        class Data:
            value: HexBytes = field(
                default="",
                metadata={
                    "required": True,
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*){32}|\s*([0-9a-fA-F]{2}\s*){36}|\s*([0-9a-fA-F]{2}\s*){72}|\s*([0-9a-fA-F]{2}\s*){416}",
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
            algorithm: Optional[DataSlotAlgorithms] = field(
                default=None,
                metadata={
                    "name": "Algorithm",
                    "type": "Attribute",
                },
            )

        @dataclass
        class Snpad:
            value: HexBytes = field(
                default=None,
                metadata={
                    "required": True,
                    "pattern": r"\s*([0-9a-fA-F]{2}\s*)+",
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
        class Info:
            """
            :ivar device_data: SN[0:3] SN[0:3] SN[0:3]
            :ivar static_data: SN[4:8] SN[4:8] SN[4:8]
            """

            device_data: List["DataZone.Slot.Info.DeviceData"] = field(
                default_factory=list,
                metadata={
                    "name": "DeviceData",
                    "type": "Element",
                },
            )
            static_data: List["DataZone.Slot.Info.StaticData"] = field(
                default_factory=list,
                metadata={
                    "name": "StaticData",
                    "type": "Element",
                },
            )

            @dataclass
            class DeviceData:
                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                    },
                )
                device_loc: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "DeviceLoc",
                        "type": "Attribute",
                    },
                )
                offset: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "Offset",
                        "type": "Attribute",
                    },
                )
                num_bytes: Optional[int] = field(
                    default=None,
                    metadata={
                        "name": "NumBytes",
                        "type": "Attribute",
                    },
                )

            @dataclass
            class StaticData:
                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                        "pattern": r"\s*([0-9a-fA-F]{2}\s*)+",
                    },
                )
