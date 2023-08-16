from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class DialysisPrescription:
    """
    :ivar entered_on: The date the Dialysis Prescription was created.
    :ivar from_time: Time the Period the Dialysis Prescription Applies
        To Starts
    :ivar to_time: Time the Period the Dialysis Prescription Applies To
        Ends
    :ivar session_type: Session Type (Same as QHD41)
    :ivar sessions_per_week: Number of Dialysis Sessions per Week
    :ivar time_dialysed: Time Dialysed (Minutes)
    :ivar vascular_access: Vascular Access to Use (QHD20)
    """
    entered_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EnteredOn",
            "type": "Element",
            "namespace": "",
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
    session_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "SessionType",
            "type": "Element",
            "namespace": "",
        }
    )
    sessions_per_week: Optional[int] = field(
        default=None,
        metadata={
            "name": "SessionsPerWeek",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    time_dialysed: Optional[int] = field(
        default=None,
        metadata={
            "name": "TimeDialysed",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    vascular_access: Optional[str] = field(
        default=None,
        metadata={
            "name": "VascularAccess",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
