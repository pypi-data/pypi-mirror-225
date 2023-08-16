from dataclasses import dataclass, field
from typing import Optional
from ukrdc_xsdata.ukrdc.types.address import Address
from ukrdc_xsdata.ukrdc.types.contact_detail import ContactDetail

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class FamilyDoctor:
    """
    :ivar gpname:
    :ivar gppractice_id: National GP Practice Code
    :ivar gpid: National GP Code
    :ivar address: Practice Address
    :ivar contact_detail: Practice Contact Information
    :ivar email: GP E-mail Address
    """
    gpname: Optional[str] = field(
        default=None,
        metadata={
            "name": "GPName",
            "type": "Element",
            "namespace": "",
        }
    )
    gppractice_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "GPPracticeId",
            "type": "Element",
            "namespace": "",
            "max_length": 6,
            "pattern": r"([A-HJ-NPWY][0-9]{5})|((ALD|JER|GUE)[0-9]{3})",
        }
    )
    gpid: Optional[str] = field(
        default=None,
        metadata={
            "name": "GPId",
            "type": "Element",
            "namespace": "",
            "max_length": 8,
            "pattern": r"G[0-9]{7}",
        }
    )
    address: Optional[Address] = field(
        default=None,
        metadata={
            "name": "Address",
            "type": "Element",
            "namespace": "",
        }
    )
    contact_detail: Optional[ContactDetail] = field(
        default=None,
        metadata={
            "name": "ContactDetail",
            "type": "Element",
            "namespace": "",
        }
    )
    email: Optional[str] = field(
        default=None,
        metadata={
            "name": "Email",
            "type": "Element",
            "namespace": "",
        }
    )
