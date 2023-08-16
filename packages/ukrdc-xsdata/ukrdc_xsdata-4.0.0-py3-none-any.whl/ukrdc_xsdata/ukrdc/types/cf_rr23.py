from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfRr23Code(Enum):
    """
    :cvar L: Litres
    :cvar DL: Decilitres
    :cvar ML: Mililitres
    :cvar G: Grams
    :cvar MG: Miligrams
    :cvar UG: Micrograms
    :cvar G_1: Micrograms
    :cvar NG: Nanograms
    :cvar TAB: Tablets
    :cvar UNITS: Units (i.e. for Epoetins)
    :cvar MMOL: Minimols
    :cvar OTHER: Other
    """
    L = "l"
    DL = "dl"
    ML = "ml"
    G = "g"
    MG = "mg"
    UG = "ug"
    G_1 = "μg"
    NG = "ng"
    TAB = "tab"
    UNITS = "units"
    MMOL = "mmol"
    OTHER = "other"


class CfRr23CodingStandard(Enum):
    CF_RR23 = "CF_RR23"


@dataclass
class CfRr23:
    class Meta:
        name = "CF_RR23"

    coding_standard: Optional[CfRr23CodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfRr23Code] = field(
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
