from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.address import Address
from ukrdc_xsdata.ukrdc.types.blood_group import BloodGroup
from ukrdc_xsdata.ukrdc.types.blood_rhesus import BloodRhesus
from ukrdc_xsdata.ukrdc.types.contact_detail import ContactDetail
from ukrdc_xsdata.ukrdc.types.ethnic_group import EthnicGroup
from ukrdc_xsdata.ukrdc.types.family_doctor import FamilyDoctor
from ukrdc_xsdata.ukrdc.types.gender import Gender
from ukrdc_xsdata.ukrdc.types.language import Language
from ukrdc_xsdata.ukrdc.types.name import Name
from ukrdc_xsdata.ukrdc.types.occupation import Occupation
from ukrdc_xsdata.ukrdc.types.patient_number import PatientNumbers
from ukrdc_xsdata.ukrdc.types.personal_contact_type import PersonalContactType

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class Patient:
    """
    :ivar patient_numbers: Patient Numbers
    :ivar names: Names
    :ivar birth_time:
    :ivar death_time:
    :ivar gender:
    :ivar addresses: Addresses
    :ivar contact_details:
    :ivar country_of_birth: From NHS Data Dictionary ISO 3166-1 Use the
        3-char alphabetic code.
    :ivar family_doctor: Current GP / GP Practice
    :ivar person_to_contact: Person to Contact about the Patient's Care.
        This element should not be submitted without prior discussion
        with the UKRR.
    :ivar ethnic_group: Ethnic Group
    :ivar occupation: Occuptation
    :ivar primary_language: Primary Language
    :ivar blood_group: Blood Type (Current)
    :ivar blood_rhesus: Blood Rhesus (Current)
    :ivar death:
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    patient_numbers: List[PatientNumbers] = field(
        default_factory=list,
        metadata={
            "name": "PatientNumbers",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        }
    )
    names: Optional["Patient.Names"] = field(
        default=None,
        metadata={
            "name": "Names",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    birth_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "BirthTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    death_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DeathTime",
            "type": "Element",
            "namespace": "",
        }
    )
    gender: Optional[Gender] = field(
        default=None,
        metadata={
            "name": "Gender",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    addresses: Optional["Patient.Addresses"] = field(
        default=None,
        metadata={
            "name": "Addresses",
            "type": "Element",
            "namespace": "",
        }
    )
    contact_details: Optional["Patient.ContactDetails"] = field(
        default=None,
        metadata={
            "name": "ContactDetails",
            "type": "Element",
            "namespace": "",
        }
    )
    country_of_birth: Optional[str] = field(
        default=None,
        metadata={
            "name": "CountryOfBirth",
            "type": "Element",
            "namespace": "",
        }
    )
    family_doctor: Optional[FamilyDoctor] = field(
        default=None,
        metadata={
            "name": "FamilyDoctor",
            "type": "Element",
            "namespace": "",
        }
    )
    person_to_contact: Optional[PersonalContactType] = field(
        default=None,
        metadata={
            "name": "PersonToContact",
            "type": "Element",
            "namespace": "",
        }
    )
    ethnic_group: Optional[EthnicGroup] = field(
        default=None,
        metadata={
            "name": "EthnicGroup",
            "type": "Element",
            "namespace": "",
        }
    )
    occupation: Optional[Occupation] = field(
        default=None,
        metadata={
            "name": "Occupation",
            "type": "Element",
            "namespace": "",
        }
    )
    primary_language: Optional[Language] = field(
        default=None,
        metadata={
            "name": "PrimaryLanguage",
            "type": "Element",
            "namespace": "",
        }
    )
    blood_group: Optional[BloodGroup] = field(
        default=None,
        metadata={
            "name": "BloodGroup",
            "type": "Element",
            "namespace": "",
        }
    )
    blood_rhesus: Optional[BloodRhesus] = field(
        default=None,
        metadata={
            "name": "BloodRhesus",
            "type": "Element",
            "namespace": "",
        }
    )
    death: Optional[bool] = field(
        default=None,
        metadata={
            "name": "Death",
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
    class Names:
        name: List[Name] = field(
            default_factory=list,
            metadata={
                "name": "Name",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            }
        )

    @dataclass
    class Addresses:
        address: List[Address] = field(
            default_factory=list,
            metadata={
                "name": "Address",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            }
        )

    @dataclass
    class ContactDetails:
        """
        :ivar contact_detail: Only 1 of each type should be sent. This
            must only be used for the Patient's own Contact Details and
            not those of third parties. This should not be submitted for
            patients who are only being sent as part of the UKRR data
            collection.
        """
        contact_detail: List[ContactDetail] = field(
            default_factory=list,
            metadata={
                "name": "ContactDetail",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
                "max_occurs": 4,
            }
        )
