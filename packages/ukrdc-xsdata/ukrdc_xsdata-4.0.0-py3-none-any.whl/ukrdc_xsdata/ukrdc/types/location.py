from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class LocationCodingStandard(Enum):
    LOCAL = "LOCAL"
    ODS = "ODS"
    PV_UNITS = "PV_UNITS"
    RR1 = "RR1+"


@dataclass
class Location:
    coding_standard: Optional[LocationCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
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
