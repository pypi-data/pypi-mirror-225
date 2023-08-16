from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime
from ukrdc_xsdata.ukrdc.types.cf_hl7_0004 import CfHl70004
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField
from ukrdc_xsdata.ukrdc.types.location import Location
from ukrdc_xsdata.ukrdc.types.service_id import ServiceId

__NAMESPACE__ = "http://www.rixg.org.uk/"


class ResultItemInterpretationCodes(Enum):
    """
    :cvar POS: Positive
    :cvar NEG: Negative
    :cvar UNK: Unknown
    """
    POS = "POS"
    NEG = "NEG"
    UNK = "UNK"


class ResultItemPrePost(Enum):
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


class ResultItemStatus(Enum):
    """
    :cvar F: Final
    :cvar P: Preliminary
    :cvar D: Deleted
    """
    F = "F"
    P = "P"
    D = "D"


@dataclass
class ResultItem:
    """
    :ivar result_type: AT
    :ivar entered_on:
    :ivar pre_post: Was the sample taken PRE or POST dialysis
    :ivar service_id: Test Code (OBX:3)
    :ivar sub_id: Sub-Test Id (OBX:4)
    :ivar result_value: OBX:5
    :ivar result_value_units: OBX:6
    :ivar reference_range: OBX:7
    :ivar interpretation_codes: Interpretation Codes (OBX:8)
    :ivar status: OBX:11
    :ivar observation_time: OBX:14
    :ivar comments: From NTE:3
    :ivar reference_comment:
    """
    result_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultType",
            "type": "Element",
            "namespace": "",
            "max_length": 2,
        }
    )
    entered_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EnteredOn",
            "type": "Element",
            "namespace": "",
        }
    )
    pre_post: Optional[ResultItemPrePost] = field(
        default=None,
        metadata={
            "name": "PrePost",
            "type": "Element",
            "namespace": "",
        }
    )
    service_id: Optional[ServiceId] = field(
        default=None,
        metadata={
            "name": "ServiceId",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    sub_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "SubId",
            "type": "Element",
            "namespace": "",
            "max_length": 30,
        }
    )
    result_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultValue",
            "type": "Element",
            "namespace": "",
            "max_length": 20,
        }
    )
    result_value_units: Optional[str] = field(
        default=None,
        metadata={
            "name": "ResultValueUnits",
            "type": "Element",
            "namespace": "",
            "max_length": 30,
        }
    )
    reference_range: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceRange",
            "type": "Element",
            "namespace": "",
            "max_length": 220,
        }
    )
    interpretation_codes: Optional[ResultItemInterpretationCodes] = field(
        default=None,
        metadata={
            "name": "InterpretationCodes",
            "type": "Element",
            "namespace": "",
        }
    )
    status: Optional[ResultItemStatus] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "",
        }
    )
    observation_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "ObservationTime",
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
    reference_comment: Optional[str] = field(
        default=None,
        metadata={
            "name": "ReferenceComment",
            "type": "Element",
            "namespace": "",
            "max_length": 1000,
        }
    )


@dataclass
class ResultItems:
    result_item: List[ResultItem] = field(
        default_factory=list,
        metadata={
            "name": "ResultItem",
            "type": "Element",
            "namespace": "",
        }
    )


@dataclass
class LabOrder:
    """
    :ivar receiving_location: Location or Facility receiving/performing
        the order.
    :ivar placer_id: ORC:2 Placer (Hospital)'s Order Id
    :ivar filler_id: ORC:3 Filler (Lab)'s Order Id
    :ivar ordered_by: Requesting Location (as in Hospital, GP, etc.)
    :ivar order_item: OBR:4 Service Id - the identity of the test
        ordered.
    :ivar order_category:
    :ivar specimen_collected_time: OBR:22
    :ivar specimen_received_time: OBR:14
    :ivar status:
    :ivar priority:
    :ivar specimen_source: OBR:15.1 e.g. serum, blood
    :ivar duration: OBR:27.3
    :ivar result_items:
    :ivar patient_class: In patient / out patient - equivalent to PV1:2
        Patient Class
    :ivar entered_on: Date Order entered
    :ivar entered_at:
    :ivar entering_organization:
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    receiving_location: Optional[Location] = field(
        default=None,
        metadata={
            "name": "ReceivingLocation",
            "type": "Element",
            "namespace": "",
        }
    )
    placer_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "PlacerId",
            "type": "Element",
            "namespace": "",
            "required": True,
            "max_length": 100,
        }
    )
    filler_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "FillerId",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
    ordered_by: Optional[Location] = field(
        default=None,
        metadata={
            "name": "OrderedBy",
            "type": "Element",
            "namespace": "",
        }
    )
    order_item: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "OrderItem",
            "type": "Element",
            "namespace": "",
        }
    )
    order_category: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "OrderCategory",
            "type": "Element",
            "namespace": "",
        }
    )
    specimen_collected_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "SpecimenCollectedTime",
            "type": "Element",
            "namespace": "",
        }
    )
    specimen_received_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "SpecimenReceivedTime",
            "type": "Element",
            "namespace": "",
        }
    )
    status: Optional[str] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "",
            "max_length": 100,
        }
    )
    priority: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "Priority",
            "type": "Element",
            "namespace": "",
        }
    )
    specimen_source: Optional[str] = field(
        default=None,
        metadata={
            "name": "SpecimenSource",
            "type": "Element",
            "namespace": "",
            "max_length": 50,
        }
    )
    duration: Optional[str] = field(
        default=None,
        metadata={
            "name": "Duration",
            "type": "Element",
            "namespace": "",
        }
    )
    result_items: Optional[ResultItems] = field(
        default=None,
        metadata={
            "name": "ResultItems",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    patient_class: Optional[CfHl70004] = field(
        default=None,
        metadata={
            "name": "PatientClass",
            "type": "Element",
            "namespace": "",
        }
    )
    entered_on: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "EnteredOn",
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
class LabOrders:
    lab_order: List[LabOrder] = field(
        default_factory=list,
        metadata={
            "name": "LabOrder",
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
