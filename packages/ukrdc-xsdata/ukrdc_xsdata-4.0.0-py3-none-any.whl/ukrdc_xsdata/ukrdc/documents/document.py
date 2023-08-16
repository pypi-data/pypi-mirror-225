from dataclasses import dataclass, field
from typing import Optional
from xsdata.models.datatype import XmlDateTime
from ukrdc_xsdata.ukrdc.types.clinician import Clinician
from ukrdc_xsdata.ukrdc.types.coded_field import CodedField
from ukrdc_xsdata.ukrdc.types.location import Location

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class Document:
    """
    :ivar document_time: Document Creation
    :ivar note_text: The body of the document as plain text
    :ivar document_type: For future use.
    :ivar clinician: The person responsibile for the content of the
        document
    :ivar document_name: Document title
    :ivar status: ACTIVE or INACTIVE
    :ivar entered_by: Person entering the document as a National
        Clinicial code where possible or other local code if not.
    :ivar entered_at: Location the document was created at. Use National
        coding e.g. RXF01
    :ivar file_type: The MIME type of the data if supplied as a stream.
    :ivar file_name: The filename of the document
    :ivar stream: This property is used when the Document is binary
        data, e.g DOC, PDF, JPG
    :ivar document_url: URL to the document if notetext/stream is not
        supplied.
    :ivar updated_on: Last Modified Date
    :ivar external_id: Unique Identifier
    """
    document_time: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "DocumentTime",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    note_text: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoteText",
            "type": "Element",
            "namespace": "",
        }
    )
    document_type: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "DocumentType",
            "type": "Element",
            "namespace": "",
        }
    )
    clinician: Optional[Clinician] = field(
        default=None,
        metadata={
            "name": "Clinician",
            "type": "Element",
            "namespace": "",
        }
    )
    document_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocumentName",
            "type": "Element",
            "namespace": "",
            "max_length": 220,
        }
    )
    status: Optional[CodedField] = field(
        default=None,
        metadata={
            "name": "Status",
            "type": "Element",
            "namespace": "",
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
    file_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileType",
            "type": "Element",
            "namespace": "",
        }
    )
    file_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "FileName",
            "type": "Element",
            "namespace": "",
        }
    )
    stream: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "Stream",
            "type": "Element",
            "namespace": "",
            "format": "base64",
        }
    )
    document_url: Optional[str] = field(
        default=None,
        metadata={
            "name": "DocumentURL",
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
