from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDate
from ukrdc_xsdata.ukrdc.procedures.procedure import Procedure
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class DialysisSession(Procedure):
    """
    :ivar symtomatic_hypotension: Symptomatic hypotension (QHD19)
    :ivar vascular_access: Vascular Access Used (QHD20)
    :ivar vascular_access_site: Vascular Access Site (QHD21)
    :ivar time_dialysed: Time Dialysed in Minutes (QHD31)
    """
    symtomatic_hypotension: Optional[str] = field(
        default=None,
        metadata={
            "name": "SymtomaticHypotension",
            "type": "Element",
            "namespace": "",
            "pattern": r"Y|N",
        }
    )
    vascular_access: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "VascularAccess",
            "type": "Element",
            "namespace": "",
        }
    )
    vascular_access_site: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "VascularAccessSite",
            "type": "Element",
            "namespace": "",
        }
    )
    time_dialysed: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeDialysed",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class DialysisSessions:
    dialysis_session: List[DialysisSession] = field(
        default_factory=list,
        metadata={
            "name": "DialysisSession",
            "type": "Element",
            "namespace": "",
        }
    )
    start: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
    stop: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        }
    )
