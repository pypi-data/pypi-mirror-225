from dataclasses import field
from typing import List, Optional

from pydantic.dataclasses import dataclass


@dataclass
class Extension:
    config: Optional[str] = field(
        default=None,
        metadata={
            "name": "Config",
            "type": "Element",
            "required": True,
        },
    )
    output: Optional["Extension.Output"] = field(
        default=None,
        metadata={
            "name": "Output",
            "type": "Element",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Attribute",
        },
    )

    @dataclass
    class Output:
        value: str = field(
            default="",
            metadata={
                "required": True,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "name": "Name",
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


@dataclass
class Extensions:
    extensions: List[Extension] = field(
        default_factory=list,
        metadata={
            "name": "Extension",
            "type": "Element",
            "required": True,
        },
    )
