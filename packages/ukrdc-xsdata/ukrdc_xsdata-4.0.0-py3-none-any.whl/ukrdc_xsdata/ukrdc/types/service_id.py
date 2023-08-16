from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class ServiceIdCodingStandard(Enum):
    """
    :cvar SNOMED: SNOMED
    :cvar LOINC: LOINC
    :cvar UKRR: UKRR
    :cvar PV: PatientView
    :cvar LOCAL: Local
    """
    SNOMED = "SNOMED"
    LOINC = "LOINC"
    UKRR = "UKRR"
    PV = "PV"
    LOCAL = "LOCAL"


@dataclass
class ServiceId:
    coding_standard: Optional[ServiceIdCodingStandard] = field(
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
