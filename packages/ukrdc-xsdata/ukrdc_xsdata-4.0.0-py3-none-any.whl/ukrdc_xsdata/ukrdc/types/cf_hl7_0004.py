from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfHl70004Code(Enum):
    """
    :cvar E: Emergency
    :cvar I: Inpatient
    :cvar O: Outpatient
    :cvar P: Preadmit
    :cvar R: Recurring Patient
    :cvar B: Obstetrics
    :cvar D: Day Hospital
    :cvar W: Week Hospital
    :cvar S: Psychiatric
    :cvar K: Newborn
    """
    E = "E"
    I = "I"
    O = "O"
    P = "P"
    R = "R"
    B = "B"
    D = "D"
    W = "W"
    S = "S"
    K = "K"


class CfHl70004CodingStandard(Enum):
    HL7_0004 = "HL7_0004"


@dataclass
class CfHl70004:
    class Meta:
        name = "CF_HL7_0004"

    coding_standard: Optional[CfHl70004CodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfHl70004Code] = field(
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
