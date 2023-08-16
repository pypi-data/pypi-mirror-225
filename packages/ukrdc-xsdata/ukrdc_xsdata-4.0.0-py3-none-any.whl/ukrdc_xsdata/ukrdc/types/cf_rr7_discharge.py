from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfRr7DischargeCode(Enum):
    """
    :cvar VALUE_30: Kidney Transplant Failure
    :cvar VALUE_38: Patient Transferred Out
    :cvar VALUE_90: Treatment Stopped (Renal Function Recovered)
    :cvar VALUE_91: Treatment Stopped (Without Recovery of Function)
    :cvar VALUE_95: Patient - Lost to follow-up
    :cvar VALUE_84: ARF - Recovered
    :cvar VALUE_85: ARF - Stopped Dialysis (without recovery of
        function)
    :cvar VALUE_86: ARF - Transferred Out
    :cvar VALUE_92: Conservative Management - Treatment stopped without
        recovery
    """
    VALUE_30 = "30"
    VALUE_38 = "38"
    VALUE_90 = "90"
    VALUE_91 = "91"
    VALUE_95 = "95"
    VALUE_84 = "84"
    VALUE_85 = "85"
    VALUE_86 = "86"
    VALUE_92 = "92"


class CfRr7DischargeCodingStandard(Enum):
    CF_RR7_DISCHARGE = "CF_RR7_DISCHARGE"


@dataclass
class CfRr7Discharge:
    class Meta:
        name = "CF_RR7_DISCHARGE"

    coding_standard: Optional[CfRr7DischargeCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfRr7DischargeCode] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "",
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
