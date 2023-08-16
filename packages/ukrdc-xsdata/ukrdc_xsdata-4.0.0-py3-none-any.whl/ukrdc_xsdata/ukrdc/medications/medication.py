from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField
from ukrdc_xsdata.ukrdc.types.drug_product import DrugProduct
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


class RouteCodingStandard(Enum):
    SNOMED = "SNOMED"
    RR22 = "RR22"


@dataclass
class Medication:
    """
    :ivar prescription_number: Prescription ID
    :ivar from_time: Start Time of the prescription
    :ivar to_time: End Time of the prescription
    :ivar entering_organization: Where the Medicine was Prescribed
    :ivar route: Medication Route
    :ivar drug_product:
    :ivar frequency: Frequency
    :ivar comments: Other instructions
    :ivar dose_quantity: Dose
    :ivar dose_uo_m:
    :ivar indication: The condition or problem for which the drug is
        being prescribed
    :ivar encounter_number: This is used to associate the prescribing of
        a Medication with the activity in a particular Encounter record.
        This element should not be submitted without prior discussion
        with the UKRR.
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    prescription_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "PrescriptionNumber",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
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
    entering_organization: Optional[Location] = field(
        default=None,
        metadata={
            "name": "EnteringOrganization",
            "type": "Element",
            "namespace": "",
        }
    )
    route: Optional["Medication.Route"] = field(
        default=None,
        metadata={
            "name": "Route",
            "type": "Element",
            "namespace": "",
        }
    )
    drug_product: Optional[DrugProduct] = field(
        default=None,
        metadata={
            "name": "DrugProduct",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    frequency: Optional[str] = field(
        default=None,
        metadata={
            "name": "Frequency",
            "type": "Element",
            "namespace": "",
            "max_length": 255,
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "",
            "max_length": 255,
        }
    )
    dose_quantity: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "DoseQuantity",
            "type": "Element",
            "namespace": "",
        }
    )
    dose_uo_m: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "DoseUoM",
            "type": "Element",
            "namespace": "",
        }
    )
    indication: Optional[str] = field(
        default=None,
        metadata={
            "name": "Indication",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
    encounter_number: Optional[str] = field(
        default=None,
        metadata={
            "name": "EncounterNumber",
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
    class Route:
        coding_standard: Optional[RouteCodingStandard] = field(
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
                "max_length": 18,
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
