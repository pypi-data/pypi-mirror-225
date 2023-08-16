from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.procedures.procedure import Procedure

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AttributesAcc30(Enum):
    """
    :cvar VALUE_1: Open Surgery (Direct Visualisation)
    :cvar VALUE_2: Laparoscopic
    :cvar VALUE_3: Percutaneous
    :cvar VALUE_4: Peritoneoscopic
    """
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"


@dataclass
class VascularAccess(Procedure):
    attributes: Optional["VascularAccess.Attributes"] = field(
        default=None,
        metadata={
            "name": "Attributes",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class Attributes:
        """
        :ivar acc19: Date Access first used for Dialysis
        :ivar acc20: Date of Access Failure
        :ivar acc21: Date of Removal
        :ivar acc22: Reason for Removal of Haemodialysis Access (HD
            Only) (RR49)
        :ivar acc30: PD Catheter Insertion Technique (PD Only) (RR143)
        :ivar acc40: Reason for Removal of PD Catheter (PD Only) (RR29)
        """
        acc19: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "ACC19",
                "type": "Element",
                "namespace": "",
            }
        )
        acc20: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "ACC20",
                "type": "Element",
                "namespace": "",
            }
        )
        acc21: Optional[XmlDateTime] = field(
            default=None,
            metadata={
                "name": "ACC21",
                "type": "Element",
                "namespace": "",
            }
        )
        acc22: Optional[str] = field(
            default=None,
            metadata={
                "name": "ACC22",
                "type": "Element",
                "namespace": "",
            }
        )
        acc30: Optional[AttributesAcc30] = field(
            default=None,
            metadata={
                "name": "ACC30",
                "type": "Element",
                "namespace": "",
            }
        )
        acc40: Optional[str] = field(
            default=None,
            metadata={
                "name": "ACC40",
                "type": "Element",
                "namespace": "",
            }
        )
