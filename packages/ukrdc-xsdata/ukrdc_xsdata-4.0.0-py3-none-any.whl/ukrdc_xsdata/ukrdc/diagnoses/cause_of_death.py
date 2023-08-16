from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_edta_cod import CfEdtaCod

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CauseOfDeathDiagnosisType(Enum):
    """
    :cvar PRIMARY: Primary
    :cvar SECONDARY: Secondary
    :cvar OTHER: Other
    """
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    OTHER = "OTHER"


class CauseOfDeathVerificationStatus(Enum):
    """
    :cvar UNCONFIRMED: Unconfirmed
    :cvar PROVISIONAL: Provisional
    :cvar DIFFERENTIAL: Differential
    :cvar CONFIRMED: Confirmed
    :cvar REFUTED: Refuted
    :cvar ENTERED_IN_ERROR: Entered in Error
    """
    UNCONFIRMED = "unconfirmed"
    PROVISIONAL = "provisional"
    DIFFERENTIAL = "differential"
    CONFIRMED = "confirmed"
    REFUTED = "refuted"
    ENTERED_IN_ERROR = "entered-in-error"


@dataclass
class CauseOfDeath:
    """
    :ivar diagnosis_type:
    :ivar diagnosis: Coded Caused of Death (EDTA)
    :ivar comments: Free text about the Diagnosis
    :ivar verification_status: The verification status to support or
        decline the clinical status of the condition or diagnosis.
    :ivar entered_on: The date the COD was recorded in the medical
        record.
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    diagnosis_type: Optional[CauseOfDeathDiagnosisType] = field(
        default=None,
        metadata={
            "name": "DiagnosisType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    diagnosis: Optional[CfEdtaCod] = field(
        default=None,
        metadata={
            "name": "Diagnosis",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "",
        }
    )
    verification_status: Optional[CauseOfDeathVerificationStatus] = field(
        default=None,
        metadata={
            "name": "VerificationStatus",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EnteredOn",
            "type": "Element",
            "namespace": "",
        }
    )
    updated_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "UpdatedOn",
            "type": "Element",
            "namespace": "",
        }
    )
    external_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "ExternalId",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
