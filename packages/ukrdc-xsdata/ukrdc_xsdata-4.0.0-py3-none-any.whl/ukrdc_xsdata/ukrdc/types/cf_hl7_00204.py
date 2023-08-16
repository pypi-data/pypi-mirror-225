from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfHl700204Code(Enum):
    """
    :cvar DA: Drug Allergy
    :cvar FA: Food Allergy
    :cvar MA: Miscellaneous Allergy
    :cvar MC: Miscellaneous Contraindication
    """
    DA = "DA"
    FA = "FA"
    MA = "MA"
    MC = "MC"


class CfHl700204CodingStandard(Enum):
    HL7_00204 = "HL7_00204"


@dataclass
class CfHl700204:
    class Meta:
        name = "CF_HL7_00204"

    coding_standard: Optional[CfHl700204CodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfHl700204Code] = field(
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
