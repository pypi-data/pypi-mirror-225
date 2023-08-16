from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


class ObservationPrePost(Enum):
    """
    :cvar PRE: Pre-Dialysis
    :cvar POST: Post-Dialysis
    :cvar UNK: Unknown
    :cvar NA: Not Applicable
    """
    PRE = "PRE"
    POST = "POST"
    UNK = "UNK"
    NA = "NA"


@dataclass
class Observation:
    """
    :ivar observation_time: When the Observation was made
    :ivar observation_code: Code for the Observation - UKRR, PV or
        SNOMED Coding Standards.
    :ivar observation_value:
    :ivar observation_units:
    :ivar pre_post: Was the Observation made PRE or POST dialysis
    :ivar comments:
    :ivar entered_at:
    :ivar entering_organization:
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    observation_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ObservationTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    observation_code: Optional["Observation.ObservationCode"] = field(
        default=None,
        metadata={
            "name": "ObservationCode",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    observation_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ObservationValue",
            "type": "Element",
            "namespace": "",
            "max_length": 20,
        }
    )
    observation_units: Optional[str] = field(
        default=None,
        metadata={
            "name": "ObservationUnits",
            "type": "Element",
            "namespace": "",
            "max_length": 30,
        }
    )
    pre_post: Optional[ObservationPrePost] = field(
        default=None,
        metadata={
            "name": "PrePost",
            "type": "Element",
            "namespace": "",
        }
    )
    comments: Optional[str] = field(
        default=None,
        metadata={
            "name": "Comments",
            "type": "Element",
            "namespace": "",
            "max_length": 1000,
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
    entering_organization: Optional[Location] = field(
        default=None,
        metadata={
            "name": "EnteringOrganization",
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
    class ObservationCode:
        coding_standard: Optional[str] = field(
            default=None,
            metadata={
                "name": "CodingStandard",
                "type": "Element",
                "namespace": "",
                "max_length": 100,
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
class Observations:
    observation: List[Observation] = field(
        default_factory=list,
        metadata={
            "name": "Observation",
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
