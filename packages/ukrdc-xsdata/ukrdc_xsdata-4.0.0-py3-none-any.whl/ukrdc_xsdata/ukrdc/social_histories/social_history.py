from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class SocialHistory:
    """
    :ivar social_habit: Social Habits
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    social_habit: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "SocialHabit",
            "type": "Element",
            "namespace": "",
            "required": True,
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
