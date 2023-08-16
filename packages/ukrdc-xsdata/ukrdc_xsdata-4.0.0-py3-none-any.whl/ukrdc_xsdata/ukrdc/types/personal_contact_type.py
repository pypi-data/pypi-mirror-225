from dataclasses import dataclass, field
from typing import List, Optional
from ukrdc_xsdata.ukrdc.types.contact_detail import ContactDetail

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class PersonalContactType:
    name: Optional[str] = field(
        default=None,
        metadata={
            "name": "Name",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    contact_details: List[ContactDetail] = field(
        default_factory=list,
        metadata={
            "name": "ContactDetails",
            "type": "Element",
            "namespace": "",
        }
    )
    relationship: Optional[str] = field(
        default=None,
        metadata={
            "name": "Relationship",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
