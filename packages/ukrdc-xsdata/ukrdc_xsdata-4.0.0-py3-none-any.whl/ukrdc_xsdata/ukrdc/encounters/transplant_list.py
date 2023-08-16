from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


class TransplantListEncounterType(Enum):
    """
    :cvar E: Emergency
    :cvar I: Inpatient
    :cvar O: Outpatient
    :cvar N: N/A
    :cvar G: ?
    :cvar P: Pre-Admit
    :cvar S: ?
    """
    E = "E"
    I = "I"
    O = "O"
    N = "N"
    G = "G"
    P = "P"
    S = "S"


@dataclass
class TransplantList:
    """
    :ivar encounter_number:
    :ivar encounter_type: General Encounter Type (PV1-2)
    :ivar from_time: Start of Registration
    :ivar to_time: End of Registration
    :ivar admitting_clinician: Responsible Clinician as a National
        Clinicial code where possible or other local code if not.
    :ivar health_care_facility: Transplant Unit
    :ivar admit_reason: Type of Organ
    :ivar admission_source: Referring Unit
    :ivar discharge_reason: Registration End Status
    :ivar discharge_location: Parent renal unit as national ODS code
        (e.g. RXF01)
    :ivar entered_at: National code for the hospital providing care -
        e.g. RXF01
    :ivar visit_description: Details of validation e.g. Date Done, by
        whom, who provided the info
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    encounter_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "EncounterNumber",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    encounter_type: Optional[TransplantListEncounterType] = field(
        default=None,
        metadata={
            "name": "EncounterType",
            "type": "Element",
            "namespace": "",
        }
    )
    from_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "FromTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    to_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ToTime",
            "type": "Element",
            "namespace": "",
        }
    )
    admitting_clinician: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "AdmittingClinician",
            "type": "Element",
            "namespace": "",
        }
    )
    health_care_facility: Optional[Location] = field(
        default=None,
        metadata={
            "name": "HealthCareFacility",
            "type": "Element",
            "namespace": "",
        }
    )
    admit_reason: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "AdmitReason",
            "type": "Element",
            "namespace": "",
        }
    )
    admission_source: Optional[Location] = field(
        default=None,
        metadata={
            "name": "AdmissionSource",
            "type": "Element",
            "namespace": "",
        }
    )
    discharge_reason: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "DischargeReason",
            "type": "Element",
            "namespace": "",
        }
    )
    discharge_location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "DischargeLocation",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_at: Optional[Location] = field(
        default=None,
        metadata={
            "name": "EnteredAt",
            "type": "Element",
            "namespace": "",
        }
    )
    visit_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "VisitDescription",
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
