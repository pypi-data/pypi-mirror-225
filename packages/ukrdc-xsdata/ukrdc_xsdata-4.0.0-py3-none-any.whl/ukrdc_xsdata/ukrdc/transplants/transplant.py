from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDate
from ukrdc_xsdata.ukrdc.procedures.procedure import Procedure

__NAMESPACE__ = "http://www.rixg.org.uk/"


class TransplantProcedureDonorType(Enum):
    DBD = "DBD"
    DCD = "DCD"
    LIVE = "LIVE"


@dataclass
class TransplantProcedure(Procedure):
    """
    :ivar donor_type: NHSBT Type
    :ivar date_registered: Date Registered for Transplantation
    :ivar failure_date: Failure Date
    :ivar cold_ischaemic_time: Cold ischaemic time in Minutes
    :ivar hlamismatch_a: Mismatch A
    :ivar hlamismatch_b: Mismatch B
    :ivar hlamismatch_c: Mismatch DR
    """
    donor_type: Optional[TransplantProcedureDonorType] = field(
        default=None,
        metadata={
            "name": "DonorType",
            "type": "Element",
            "namespace": "",
        }
    )
    date_registered: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "DateRegistered",
            "type": "Element",
            "namespace": "",
        }
    )
    failure_date: Optional[XmlDate] = field(
        default=None,
        metadata={
            "name": "FailureDate",
            "type": "Element",
            "namespace": "",
        }
    )
    cold_ischaemic_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ColdIschaemicTime",
            "type": "Element",
            "namespace": "",
        }
    )
    hlamismatch_a: Optional[str] = field(
        default=None,
        metadata={
            "name": "HLAMismatchA",
            "type": "Element",
            "namespace": "",
        }
    )
    hlamismatch_b: Optional[str] = field(
        default=None,
        metadata={
            "name": "HLAMismatchB",
            "type": "Element",
            "namespace": "",
        }
    )
    hlamismatch_c: Optional[str] = field(
        default=None,
        metadata={
            "name": "HLAMismatchC",
            "type": "Element",
            "namespace": "",
        }
    )
