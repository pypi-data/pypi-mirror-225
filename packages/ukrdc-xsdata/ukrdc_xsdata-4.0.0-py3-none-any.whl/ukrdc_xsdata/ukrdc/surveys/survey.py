from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class Level:
    """
    :ivar level_type: Score Type
    :ivar value:
    """
    level_type: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "LevelType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )


@dataclass
class Question:
    """
    :ivar question_type: Question Type
    :ivar response:
    :ivar question_text:
    """
    question_type: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "QuestionType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    response: Optional[str] = field(
        default=None,
        metadata={
            "name": "Response",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    question_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "QuestionText",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class Score:
    """
    :ivar score_type: Score Type
    :ivar value:
    """
    score_type: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "ScoreType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )


@dataclass
class Survey:
    """
    :ivar survey_time: When the survey was completed.
    :ivar survey_type: Survey Type
    :ivar questions:
    :ivar scores:
    :ivar levels:
    :ivar entered_by: Who completed the survey
    :ivar entered_at: Where the Survey was completed
    :ivar type_of_treatment: Current Modality
    :ivar hdlocation: If Current Modality = HD, where is it performed?
    :ivar template: This is currently only used to flag surveys which
        were submitted via the SharedHD project. Another field may be
        more appropriate.
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    survey_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "SurveyTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    survey_type: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "SurveyType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    questions: Optional["Survey.Questions"] = field(
        default=None,
        metadata={
            "name": "Questions",
            "type": "Element",
            "namespace": "",
        }
    )
    scores: Optional["Survey.Scores"] = field(
        default=None,
        metadata={
            "name": "Scores",
            "type": "Element",
            "namespace": "",
        }
    )
    levels: Optional["Survey.Levels"] = field(
        default=None,
        metadata={
            "name": "Levels",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_by: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "EnteredBy",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_at: Optional[Location] = field(
        default=None,
        metadata={
            "name": "EnteredAt",
            "type": "Element",
            "namespace": "",
        }
    )
    type_of_treatment: Optional[str] = field(
        default=None,
        metadata={
            "name": "TypeOfTreatment",
            "type": "Element",
            "namespace": "",
        }
    )
    hdlocation: Optional[str] = field(
        default=None,
        metadata={
            "name": "HDLocation",
            "type": "Element",
            "namespace": "",
        }
    )
    template: Optional[str] = field(
        default=None,
        metadata={
            "name": "Template",
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
    class Questions:
        question: List[Question] = field(
            default_factory=list,
            metadata={
                "name": "Question",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Scores:
        score: List[Score] = field(
            default_factory=list,
            metadata={
                "name": "Score",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Levels:
        level: List[Level] = field(
            default_factory=list,
            metadata={
                "name": "Level",
                "type": "Element",
                "namespace": "",
            }
        )
