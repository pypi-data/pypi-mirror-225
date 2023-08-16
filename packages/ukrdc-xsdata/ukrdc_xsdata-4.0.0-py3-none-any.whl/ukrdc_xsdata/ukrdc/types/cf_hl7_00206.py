from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfHl700206Code(Enum):
    """
    :cvar SV: Severe
    :cvar MO: Moderate
    :cvar MI: Mild
    """
    SV = "SV"
    MO = "MO"
    MI = "MI"


class CfHl700206CodingStandard(Enum):
    HL7_00206 = "HL7_00206"


@dataclass
class CfHl700206:
    class Meta:
        name = "CF_HL7_00206"

    coding_standard: Optional[CfHl700206CodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfHl700206Code] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "",
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
