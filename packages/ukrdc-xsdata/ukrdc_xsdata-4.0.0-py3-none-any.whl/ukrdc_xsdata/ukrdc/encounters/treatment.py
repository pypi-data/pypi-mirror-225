from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_rr7_discharge import CfRr7Discharge
from ukrdc_xsdata.ukrdc.types.cf_rr7_treatment import CfRr7Treatment
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AttributesQbl05(Enum):
    """
    :cvar HOME: Home Dialysis
    :cvar INCENTRE: Treatment occurs In-centre
    :cvar ASSISTED: Treatment is assisted by a paid carer
    """
    HOME = "HOME"
    INCENTRE = "INCENTRE"
    ASSISTED = "ASSISTED"


@dataclass
class Treatment:
    """
    :ivar encounter_number:
    :ivar from_time: Start of Treatment (TXT00)
    :ivar to_time: End of Treatment (TXT01)
    :ivar admitting_clinician: Responsible Clinician as a National
        Clinicial code where possible or other local code if not.
    :ivar health_care_facility: Treatment Centre (TXT20)
    :ivar admit_reason: Modality
    :ivar admission_source: Prior Main Renal Unit
    :ivar discharge_reason: Reason for Discharge
    :ivar discharge_location: Destination Main Renal Unit
    :ivar entered_at: National code for the hospital providing care -
        e.g. RXF01
    :ivar visit_description: Free text about the Treatment record.
    :ivar attributes:
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    encounter_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "EncounterNumber",
            "type": "Element",
            "namespace": "",
        }
    )
    from_time: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "FromTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    to_time: Optional[XmlDate] = field(
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
    admit_reason: Optional[CfRr7Treatment] = field(
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
    discharge_reason: Optional[CfRr7Discharge] = field(
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
    attributes: Optional["Treatment.Attributes"] = field(
        default=None,
        metadata={
            "name": "Attributes",
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

    @dataclass
    class Attributes:
        """
        :ivar qbl05: HD Treatment Location (RR8) AKA TXT21
        """
        qbl05: Optional[AttributesQbl05] = field(
            default=None,
            metadata={
                "name": "QBL05",
                "type": "Element",
                "namespace": "",
            }
        )
