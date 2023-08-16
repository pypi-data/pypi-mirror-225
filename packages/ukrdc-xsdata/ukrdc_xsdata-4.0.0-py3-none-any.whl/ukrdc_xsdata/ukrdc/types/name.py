from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class NameUse(Enum):
    """
    :cvar B: Birth Name
    :cvar D: Usual
    :cvar L: Official
    """
    B = "B"
    D = "D"
    L = "L"


@dataclass
class Name:
    """
    :ivar prefix: Prefix or title e.g. Mr, Mrs etc
    :ivar family: Surname or family name. Mandatory on Usual name
    :ivar given: Given name. Mandatory for a Usual name.
    :ivar other_given_names: 2nd and other given name
    :ivar suffix: Suffix e.g. Jnr, Snr etc.
    :ivar use: https://www.hl7.org/fhir/v2/0200/index.html
    """
    prefix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Prefix",
            "type": "Element",
            "namespace": "",
            "max_length": 10,
        }
    )
    family: Optional[str] = field(
        default=None,
        metadata={
            "name": "Family",
            "type": "Element",
            "namespace": "",
            "min_length": 2,
            "max_length": 60,
        }
    )
    given: Optional[str] = field(
        default=None,
        metadata={
            "name": "Given",
            "type": "Element",
            "namespace": "",
            "min_length": 2,
            "max_length": 60,
        }
    )
    other_given_names: Optional[str] = field(
        default=None,
        metadata={
            "name": "OtherGivenNames",
            "type": "Element",
            "namespace": "",
            "max_length": 60,
        }
    )
    suffix: Optional[str] = field(
        default=None,
        metadata={
            "name": "Suffix",
            "type": "Element",
            "namespace": "",
            "max_length": 10,
        }
    )
    use: Optional[NameUse] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
