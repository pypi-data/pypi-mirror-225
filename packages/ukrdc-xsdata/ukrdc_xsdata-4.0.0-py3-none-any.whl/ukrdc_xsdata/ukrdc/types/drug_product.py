from dataclasses import dataclass, field
from typing import Optional
from ukrdc_xsdata.ukrdc.types.cf_dmd import CfDmd
from ukrdc_xsdata.ukrdc.types.cf_rr23 import CfRr23
from ukrdc_xsdata.ukrdc.types.cf_snomed import CfSnomed

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class DrugProduct:
    """
    :ivar id: DM+D code for the drug
    :ivar generic: Generic name
    :ivar label_name: Brand Name
    :ivar form: SNOMED Code and description
    :ivar strength_units: Units
    """
    id: Optional[CfDmd] = field(
        default=None,
        metadata={
            "name": "Id",
            "type": "Element",
            "namespace": "",
        }
    )
    generic: Optional[str] = field(
        default=None,
        metadata={
            "name": "Generic",
            "type": "Element",
            "namespace": "",
            "required": True,
            "max_length": 125,
        }
    )
    label_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "LabelName",
            "type": "Element",
            "namespace": "",
            "max_length": 255,
        }
    )
    form: Optional[CfSnomed] = field(
        default=None,
        metadata={
            "name": "Form",
            "type": "Element",
            "namespace": "",
        }
    )
    strength_units: Optional[CfRr23] = field(
        default=None,
        metadata={
            "name": "StrengthUnits",
            "type": "Element",
            "namespace": "",
        }
    )
