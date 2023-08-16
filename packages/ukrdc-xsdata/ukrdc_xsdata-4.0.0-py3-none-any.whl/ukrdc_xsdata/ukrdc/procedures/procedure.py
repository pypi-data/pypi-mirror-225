from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_snomed import CfSnomed
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class Procedure:
    """
    :ivar procedure_type: At least code must be entered
    :ivar procedure_time: The time the Procedure started.
    :ivar entered_by: Person entering the diagnosis as a National
        Clinicial code where possible or other local code if not.
    :ivar entered_at: Location the procedure was performed at. Use
        National coding e.g. RXF01
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    procedure_type: Optional[CfSnomed] = field(
        default=None,
        metadata={
            "name": "ProcedureType",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    procedure_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ProcedureTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    entered_by: Optional[Clinician] = field(
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
