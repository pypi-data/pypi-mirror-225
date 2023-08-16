from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_snomed import CfSnomed
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class FamilyHistory:
    """
    :ivar family_member: Family member
    :ivar diagnosis: Diagnosis on family member
    :ivar note_text:
    :ivar entered_at:
    :ivar from_time: Beginning of period covered
    :ivar to_time: End of period covered
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    family_member: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "FamilyMember",
            "type": "Element",
            "namespace": "",
        }
    )
    diagnosis: Optional[CfSnomed] = field(
        default=None,
        metadata={
            "name": "Diagnosis",
            "type": "Element",
            "namespace": "",
        }
    )
    note_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoteText",
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
    from_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "FromTime",
            "type": "Element",
            "namespace": "",
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
