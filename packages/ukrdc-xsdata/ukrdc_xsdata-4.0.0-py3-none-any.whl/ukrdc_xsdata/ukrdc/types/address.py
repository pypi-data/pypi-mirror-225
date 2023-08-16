from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AddressUse(Enum):
    """
    :cvar H: Home
    :cvar PST: Postal
    :cvar TMP: Temporary
    """
    H = "H"
    PST = "PST"
    TMP = "TMP"


class CountryCodingStandard(Enum):
    """
    :cvar ISO3166_1:
        http://www.datadictionary.nhs.uk/data_dictionary/attributes/c/cou/country_code_de.asp
    """
    ISO3166_1 = "ISO3166-1"


@dataclass
class Address:
    """
    :ivar from_time:
    :ivar to_time:
    :ivar street: Everything prior to the Town in the Address
    :ivar town:
    :ivar county:
    :ivar postcode:
    :ivar country:
    :ivar use: From National MIM
    """
    from_time: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "FromTime",
            "type": "Element",
            "namespace": "",
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
    street: Optional[str] = field(
        default=None,
        metadata={
            "name": "Street",
            "type": "Element",
            "namespace": "",
            "max_length": 220,
        }
    )
    town: Optional[str] = field(
        default=None,
        metadata={
            "name": "Town",
            "type": "Element",
            "namespace": "",
        }
    )
    county: Optional[str] = field(
        default=None,
        metadata={
            "name": "County",
            "type": "Element",
            "namespace": "",
        }
    )
    postcode: Optional[str] = field(
        default=None,
        metadata={
            "name": "Postcode",
            "type": "Element",
            "namespace": "",
            "max_length": 8,
            "pattern": r"((([A-Z][0-9]{1,2})|(([A-Z][A-HJ-Y][0-9]{1,2})|(([A-Z][0-9][A-Z])|([A-Z][A-HJ-Y][0-9][A-Z])))) {0,6}([0-9][ABD-HJLNP-UW-Z]{2})?|ZZ99 {0,1}([0-9][A-Z]Z)?)",
        }
    )
    country: Optional["Address.Country"] = field(
        default=None,
        metadata={
            "name": "Country",
            "type": "Element",
            "namespace": "",
        }
    )
    use: Optional[AddressUse] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )

    @dataclass
    class Country:
        coding_standard: Optional[CountryCodingStandard] = field(
            default=None,
            metadata={
                "name": "CodingStandard",
                "type": "Element",
                "namespace": "",
            }
        )
        code: Optional[str] = field(
            default=None,
            metadata={
                "name": "Code",
                "type": "Element",
                "namespace": "",
                "max_length": 100,
            }
        )
        description: Optional[str] = field(
            default=None,
            metadata={
                "name": "Description",
                "type": "Element",
                "namespace": "",
                "max_length": 100,
            }
        )
