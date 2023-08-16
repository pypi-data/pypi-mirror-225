from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class CodedField:
    coding_standard: Optional[str] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
            "max_length": 32000,
        }
    )
    code: Optional[str] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "",
            "max_length": 32000,
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "",
            "max_length": 32000,
        }
    )
