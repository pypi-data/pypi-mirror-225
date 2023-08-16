from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_hl7_00204 import CfHl700204
from ukrdc_xsdata.ukrdc.types.cf_hl7_00206 import CfHl700206
from ukrdc_xsdata.ukrdc.types.cf_snomed import CfSnomed
from ukrdc_xsdata.ukrdc.types.clinician import Clinician

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class Allergy:
    """Allergies.

    This item should not be submitted without checking with the UKRR.

    :ivar allergy: Substance to which the patient is allergic. (SNOMED)
    :ivar allergy_category: Type of Allergy (HL7 00204)
    :ivar severity: Severity (HL7 00206)
    :ivar clinician: Diagnosing Clinician
    :ivar discovery_time: Reported Date
    :ivar confirmed_time: Confirmed Time
    :ivar comments: Advice given to the patient
    :ivar inactive_time: Resolved Time
    :ivar free_text_allergy: AL1-5 Free text definition of what happened
    :ivar qualifying_details: Details if patient or family reported
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    allergy: Optional[CfSnomed] = field(
        default=None,
        metadata={
            "name": "Allergy",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    allergy_category: Optional[CfHl700204] = field(
        default=None,
        metadata={
            "name": "AllergyCategory",
            "type": "Element",
            "namespace": "",
        }
    )
    severity: Optional[CfHl700206] = field(
        default=None,
        metadata={
            "name": "Severity",
            "type": "Element",
            "namespace": "",
        }
    )
    clinician: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "Clinician",
            "type": "Element",
            "namespace": "",
        }
    )
    discovery_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DiscoveryTime",
            "type": "Element",
            "namespace": "",
        }
    )
    confirmed_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ConfirmedTime",
            "type": "Element",
            "namespace": "",
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "",
            "max_length": 500,
        }
    )
    inactive_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "InactiveTime",
            "type": "Element",
            "namespace": "",
        }
    )
    free_text_allergy: Optional[str] = field(
        default=None,
        metadata={
            "name": "FreeTextAllergy",
            "type": "Element",
            "namespace": "",
            "max_length": 500,
        }
    )
    qualifying_details: Optional[str] = field(
        default=None,
        metadata={
            "name": "QualifyingDetails",
            "type": "Element",
            "namespace": "",
            "max_length": 500,
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
