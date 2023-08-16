from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class SendingFacility:
    """
    :ivar value:
    :ivar channel_name: This should be a reference for the System /
        Version which generated the file. The intended purpose is to
        allow us to identify, or temporarily rectify, issues with what a
        particular extract is generating.
    :ivar time: This should be the time that the extract was generated.
    :ivar schema_version: This should be the version (from the XSD
        Schema) that the extract has been written against. This is to
        allow us to process incoming files accordingly as well as track
        which Units are submitting which version. Note that the RDA
        Schema version is unrelated to the UKRR Dataset version.
    """
    value: str = field(
        default="",
        metadata={
            "required": True,
            "min_length": 1,
            "max_length": 7,
        }
    )
    channel_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "channelName",
            "type": "Attribute",
            "required": True,
        }
    )
    time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        }
    )
    schema_version: Optional[str] = field(
        default=None,
        metadata={
            "name": "schemaVersion",
            "type": "Attribute",
            "required": True,
            "pattern": r"\d+\.\d+\.\d+",
        }
    )
