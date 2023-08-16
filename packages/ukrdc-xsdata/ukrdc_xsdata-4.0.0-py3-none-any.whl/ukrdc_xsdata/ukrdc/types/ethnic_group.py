from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class EthnicGroupCode(Enum):
    """
    :cvar A: British
    :cvar B: Irish
    :cvar C: Any other White background
    :cvar D: White and Black Caribbean
    :cvar E: White and Black African
    :cvar F: White and Asian
    :cvar G: Any other mixed background
    :cvar H: Indian
    :cvar J: Pakistani
    :cvar K: Bangladeshi
    :cvar L: Any other Asian background
    :cvar M: Caribbean
    :cvar N: African
    :cvar P: Any other Black background
    :cvar R: Chinese
    :cvar S: Any other ethnic group
    :cvar Z: Not stated
    """
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    P = "P"
    R = "R"
    S = "S"
    Z = "Z"


class EthnicGroupCodingStandard(Enum):
    """
    :cvar NHS_DATA_DICTIONARY:
        https://datadictionary.nhs.uk/data_elements/ethnic_category.html
    """
    NHS_DATA_DICTIONARY = "NHS_DATA_DICTIONARY"


@dataclass
class EthnicGroup:
    coding_standard: Optional[EthnicGroupCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[EthnicGroupCode] = field(
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
