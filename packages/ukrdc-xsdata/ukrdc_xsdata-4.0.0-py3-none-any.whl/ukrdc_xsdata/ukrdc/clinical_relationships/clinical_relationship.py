from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class ClinicalRelationship:
    """
    :ivar from_time: Start of the relationship
    :ivar to_time: End of the relationship
    :ivar clinician:
    :ivar facility_code:
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
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
    clinician: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "Clinician",
            "type": "Element",
            "namespace": "",
        }
    )
    facility_code: Optional[Location] = field(
        default=None,
        metadata={
            "name": "FacilityCode",
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
