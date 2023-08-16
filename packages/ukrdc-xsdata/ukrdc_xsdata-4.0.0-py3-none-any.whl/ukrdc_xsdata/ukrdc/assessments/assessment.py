from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.rixg.org.uk/"


class AssessmentOutcomeCodingStandard(Enum):
    RR51 = "RR51"


class AssessmentTypeCodingStandard(Enum):
    RR50 = "RR50"


@dataclass
class Assessment:
    """
    :ivar assessment_start: The Date the Assessment Started
    :ivar assessment_end: The Date the Assessment Ended
    :ivar assessment_type: Assessment Type
    :ivar assessment_outcome: Assessment Outcome
    """
    assessment_start: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "AssessmentStart",
            "type": "Element",
            "namespace": "",
        }
    )
    assessment_end: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "AssessmentEnd",
            "type": "Element",
            "namespace": "",
        }
    )
    assessment_type: Optional["Assessment.AssessmentType"] = field(
        default=None,
        metadata={
            "name": "AssessmentType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    assessment_outcome: Optional["Assessment.AssessmentOutcome"] = field(
        default=None,
        metadata={
            "name": "AssessmentOutcome",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )

    @dataclass
    class AssessmentType:
        coding_standard: Optional[AssessmentTypeCodingStandard] = field(
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

    @dataclass
    class AssessmentOutcome:
        coding_standard: Optional[AssessmentOutcomeCodingStandard] = field(
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
