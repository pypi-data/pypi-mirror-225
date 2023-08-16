from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class PatientNumberNumberType(Enum):
    """
    :cvar MRN: Primary Identifier for that Organisation
    :cvar NI: For 3rd-Party Identifiers such as NHS Numbers
    """
    MRN = "MRN"
    NI = "NI"


class PatientNumberOrganization(Enum):
    """
    :cvar NHS: NHS Number (England and Wales)
    :cvar CHI: NHS Number (Scotland)
    :cvar HSC: NHS Number (Ireland)
    :cvar UKRR: UK Renal Registry
    :cvar SRR: Scottish Renal Registry
    :cvar NHSBT: NHS Blood and Transplant
    :cvar RADAR: Rare Disease Registry
    :cvar BAPN: British Association For Paediatric Nephrology
    :cvar LOCALHOSP: Local Hospital Number
    :cvar UKRR_UID: UKRR Unique Identifier for Refused Consent Patients
    :cvar STUDYNO: Study ID (SendingFacility = Study)
    """
    NHS = "NHS"
    CHI = "CHI"
    HSC = "HSC"
    UKRR = "UKRR"
    SRR = "SRR"
    NHSBT = "NHSBT"
    RADAR = "RADAR"
    BAPN = "BAPN"
    LOCALHOSP = "LOCALHOSP"
    UKRR_UID = "UKRR_UID"
    STUDYNO = "STUDYNO"


@dataclass
class PatientNumber:
    """
    :ivar number: Patient Identification Number
    :ivar organization: Organisation that issued the number
    :ivar number_type:
    """
    number: Optional[str] = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Element",
            "namespace": "",
            "required": True,
            "min_length": 1,
            "max_length": 50,
        }
    )
    organization: Optional[PatientNumberOrganization] = field(
        default=None,
        metadata={
            "name": "Organization",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    number_type: Optional[PatientNumberNumberType] = field(
        default=None,
        metadata={
            "name": "NumberType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )


@dataclass
class PatientNumbers:
    patient_number: List[PatientNumber] = field(
        default_factory=list,
        metadata={
            "name": "PatientNumber",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        }
    )
