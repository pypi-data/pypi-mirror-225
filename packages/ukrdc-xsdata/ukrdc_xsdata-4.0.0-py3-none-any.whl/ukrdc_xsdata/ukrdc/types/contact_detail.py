from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class ContactDetailUse(Enum):
    """
    :cvar PRN: Home Phone
    :cvar WPN: Work Phone
    :cvar PRS: Mobile Number
    :cvar NET: Email
    """
    PRN = "PRN"
    WPN = "WPN"
    PRS = "PRS"
    NET = "NET"


@dataclass
class ContactDetail:
    """
    :ivar value: The contact detail = phone number or email id
    :ivar comments:
    :ivar use: Based on HL7 table 201
    """
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "",
            "max_length": 80,
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "",
            "max_length": 70,
        }
    )
    use: Optional[ContactDetailUse] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
