from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class ProgramMembership:
    """
    :ivar entered_by: Person entering the consent as a National
        Clinicial code where possible or other local code if not.
    :ivar entered_at: National code for the trust recording the consent
        - e.g. RXF01
    :ivar program_name: Name of RDG or study
    :ivar program_description: Free text
    :ivar from_time: Date Consent Given
    :ivar to_time: Date Consent Withdrawn
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    entered_by: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "EnteredBy",
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
    program_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProgramName",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
    program_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "ProgramDescription",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
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
