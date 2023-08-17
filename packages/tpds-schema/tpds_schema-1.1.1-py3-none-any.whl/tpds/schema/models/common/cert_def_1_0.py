from dataclasses import field
from enum import Enum
from typing import List, Optional

from pydantic.dataclasses import dataclass


class CompressedCertType(Enum):
    CUSTOM = "Custom"
    X509 = "X509"


@dataclass
class CompressedCert:
    element: List["CompressedCert.Element"] = field(
        default_factory=list,
        metadata={
            "name": "Element",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    template_data: Optional["CompressedCert.TemplateData"] = field(
        default=None,
        metadata={
            "name": "TemplateData",
            "type": "Element",
        },
    )
    capublic_key: Optional[str] = field(
        default=None,
        metadata={
            "name": "CAPublicKey",
            "type": "Element",
        },
    )
    index: Optional[int] = field(
        default=None,
        metadata={
            "name": "Index",
            "type": "Attribute",
        },
    )
    type: Optional[CompressedCertType] = field(
        default=None,
        metadata={
            "name": "Type",
            "type": "Attribute",
        },
    )
    template_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "TemplateID",
            "type": "Attribute",
            "pattern": r"[0-9a-fA-F]{1}",
        },
    )
    chain_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ChainID",
            "type": "Attribute",
            "pattern": r"[0-9a-fA-F]{1}",
        },
    )
    snsource: Optional[str] = field(
        default=None,
        metadata={
            "name": "SNSource",
            "type": "Attribute",
            "pattern": r"[0-9a-fA-F]{1}",
        },
    )
    chain_level: Optional[int] = field(
        default=None,
        metadata={
            "name": "ChainLevel",
            "type": "Attribute",
        },
    )
    tbs_size: Optional[int] = field(
        default=None,
        metadata={
            "name": "TbsSize",
            "type": "Attribute",
        },
    )
    tbs_loc: Optional[int] = field(
        default=None,
        metadata={
            "name": "TbsLoc",
            "type": "Attribute",
        },
    )
    valid_years: Optional[int] = field(
        default=None,
        metadata={
            "name": "ValidYears",
            "type": "Attribute",
        },
    )
    single_signer_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SingleSignerID",
            "type": "Attribute",
        },
    )

    @dataclass
    class Element:
        name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Name",
                "type": "Attribute",
            },
        )
        data_loc: Optional[int] = field(
            default=None,
            metadata={
                "name": "DataLoc",
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
        date_format: Optional[str] = field(
            default=None,
            metadata={
                "name": "DateFormat",
                "type": "Attribute",
            },
        )
        format: Optional[str] = field(
            default=None,
            metadata={
                "name": "Format",
                "type": "Attribute",
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
        transforms: Optional[str] = field(
            default=None,
            metadata={
                "name": "Transforms",
                "type": "Attribute",
            },
        )
        counter_start: Optional[str] = field(
            default=None,
            metadata={
                "name": "CounterStart",
                "type": "Attribute",
            },
        )
        counter_stop: Optional[str] = field(
            default=None,
            metadata={
                "name": "CounterStop",
                "type": "Attribute",
            },
        )
        counter_step: Optional[str] = field(
            default=None,
            metadata={
                "name": "CounterStep",
                "type": "Attribute",
            },
        )
        counter_format: Optional[str] = field(
            default=None,
            metadata={
                "name": "CounterFormat",
                "type": "Attribute",
            },
        )
        full_date: Optional[bool] = field(
            default=None,
            metadata={
                "name": "FullDate",
                "type": "Attribute",
            },
        )

    @dataclass
    class TemplateData:
        value: str = field(
            default="",
            metadata={
                "pattern": r"\s*([0-9a-fA-F]{2}\s*)+",
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
class CompressedCerts:
    compressed_cert: List[CompressedCert] = field(
        default_factory=list,
        metadata={
            "name": "CompressedCert",
        },
    )
    compressed_certs: Optional[int] = field(
        default=None,
        metadata={
            "name": "CompressedCerts",
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
