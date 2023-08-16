from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDate

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class Pvdata:
    class Meta:
        name = "PVData"

    rrtstatus: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
    tpstatus: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
    diagnosisdate: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    bloodgroup: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "namespace": "",
            "max_length": 30,
        }
    )
