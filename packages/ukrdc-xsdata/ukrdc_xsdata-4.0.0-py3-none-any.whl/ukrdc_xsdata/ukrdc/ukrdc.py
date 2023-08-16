from dataclasses import dataclass, field
from typing import List, Optional
from xsdata.models.datatype import XmlDate
from ukrdc_xsdata.ukrdc.allergies.allergy import Allergy
from ukrdc_xsdata.ukrdc.assessments.assessment import Assessment
from ukrdc_xsdata.ukrdc.clinical_relationships.clinical_relationship import ClinicalRelationship
from ukrdc_xsdata.ukrdc.diagnoses.cause_of_death import CauseOfDeath
from ukrdc_xsdata.ukrdc.diagnoses.diagnosis import Diagnosis
from ukrdc_xsdata.ukrdc.diagnoses.renal_diagnosis import RenalDiagnosis
from ukrdc_xsdata.ukrdc.dialysis_prescriptions.dialysis_prescription import DialysisPrescription
from ukrdc_xsdata.ukrdc.dialysis_sessions.dialysis_session import DialysisSessions
from ukrdc_xsdata.ukrdc.documents.document import Document
from ukrdc_xsdata.ukrdc.encounters.encounter import Encounter
from ukrdc_xsdata.ukrdc.encounters.transplant_list import TransplantList
from ukrdc_xsdata.ukrdc.encounters.treatment import Treatment
from ukrdc_xsdata.ukrdc.family_histories.family_history import FamilyHistory
from ukrdc_xsdata.ukrdc.lab_orders.lab_order import LabOrders
from ukrdc_xsdata.ukrdc.medications.medication import Medication
from ukrdc_xsdata.ukrdc.observations.observation import Observations
from ukrdc_xsdata.ukrdc.opt_outs.opt_out import OptOut
from ukrdc_xsdata.ukrdc.patient import Patient
from ukrdc_xsdata.ukrdc.procedures.procedure import Procedure
from ukrdc_xsdata.ukrdc.program_memberships.program_membership import ProgramMembership
from ukrdc_xsdata.ukrdc.social_histories.social_history import SocialHistory
from ukrdc_xsdata.ukrdc.surveys.survey import Survey
from ukrdc_xsdata.ukrdc.transplants.transplant import TransplantProcedure
from ukrdc_xsdata.ukrdc.types.pvdata import Pvdata
from ukrdc_xsdata.ukrdc.types.sending_extract import SendingExtract
from ukrdc_xsdata.ukrdc.types.sending_facility import SendingFacility
from ukrdc_xsdata.ukrdc.vascular_accesses.vascular_access import VascularAccess

__NAMESPACE__ = "http://www.rixg.org.uk/"


@dataclass
class PatientRecord:
    """
    :ivar sending_facility: The value of this element is the Site or
        System responsible for the data being sent.
    :ivar sending_extract: The type of data feed. This is used to enable
        different behaviour when the original source of data was
        something other than a UKRDC feed (i.e. when "PV XML" is
        converted to "RDA XML" it is given a SendingExtract of "PV").
        Unless told otherwise the value should be set to "UKRDC".
    :ivar patient: Patient Demographics
    :ivar lab_orders: Lab Orders
    :ivar social_histories: Other Health Related Behaviours
    :ivar family_histories: Family Histories
    :ivar observations: Observations. These are measurements taken about
        a patient that do not involve a Laboratory.
    :ivar allergies: Allergies.
    :ivar diagnoses:
    :ivar medications: Medications
    :ivar dialysis_prescriptions: Dialysis Prescriptions
    :ivar procedures: Procedures
    :ivar documents: Documents
    :ivar encounters:
    :ivar program_memberships: Program Memberships. These are used to
        record whether or not a patient wishes to participate in one of
        the UKRDC’s member projects. In the case of projects such as
        RADAR the Program Membership record should only be closed if the
        patient actively wishes to withdraw. It should not be end dated
        when they leave the unit or die. If a patient decides to leave a
        project and then re-joins a new Program Membership record should
        be created (with a different ExternalID) rather than re-opening
        the original one.
    :ivar opt_outs: Opt-Outs
    :ivar clinical_relationships: This is used to record the
        relationship between a Patient and a Clinician or Care Facility.
        This element should not be submitted without prior discussion
        with the UKRR.
    :ivar surveys: Surveys
    :ivar assessments: Assessments
    :ivar pvdata: This is used internally to hold data items sent in PV
        XML files and should not be sent by external parties.
    """
    class Meta:
        namespace = "http://www.rixg.org.uk/"

    sending_facility: Optional[SendingFacility] = field(
        default=None,
        metadata={
            "name": "SendingFacility",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    sending_extract: Optional[SendingExtract] = field(
        default=None,
        metadata={
            "name": "SendingExtract",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    patient: Optional[Patient] = field(
        default=None,
        metadata={
            "name": "Patient",
            "type": "Element",
            "namespace": "",
            "required": True,
        }
    )
    lab_orders: Optional[LabOrders] = field(
        default=None,
        metadata={
            "name": "LabOrders",
            "type": "Element",
            "namespace": "",
        }
    )
    social_histories: Optional["PatientRecord.SocialHistories"] = field(
        default=None,
        metadata={
            "name": "SocialHistories",
            "type": "Element",
            "namespace": "",
        }
    )
    family_histories: Optional["PatientRecord.FamilyHistories"] = field(
        default=None,
        metadata={
            "name": "FamilyHistories",
            "type": "Element",
            "namespace": "",
        }
    )
    observations: Optional[Observations] = field(
        default=None,
        metadata={
            "name": "Observations",
            "type": "Element",
            "namespace": "",
        }
    )
    allergies: Optional["PatientRecord.Allergies"] = field(
        default=None,
        metadata={
            "name": "Allergies",
            "type": "Element",
            "namespace": "",
        }
    )
    diagnoses: Optional["PatientRecord.Diagnoses"] = field(
        default=None,
        metadata={
            "name": "Diagnoses",
            "type": "Element",
            "namespace": "",
        }
    )
    medications: Optional["PatientRecord.Medications"] = field(
        default=None,
        metadata={
            "name": "Medications",
            "type": "Element",
            "namespace": "",
        }
    )
    dialysis_prescriptions: Optional["PatientRecord.DialysisPrescriptions"] = field(
        default=None,
        metadata={
            "name": "DialysisPrescriptions",
            "type": "Element",
            "namespace": "",
        }
    )
    procedures: Optional["PatientRecord.Procedures"] = field(
        default=None,
        metadata={
            "name": "Procedures",
            "type": "Element",
            "namespace": "",
        }
    )
    documents: Optional["PatientRecord.Documents"] = field(
        default=None,
        metadata={
            "name": "Documents",
            "type": "Element",
            "namespace": "",
        }
    )
    encounters: Optional["PatientRecord.Encounters"] = field(
        default=None,
        metadata={
            "name": "Encounters",
            "type": "Element",
            "namespace": "",
        }
    )
    program_memberships: Optional["PatientRecord.ProgramMemberships"] = field(
        default=None,
        metadata={
            "name": "ProgramMemberships",
            "type": "Element",
            "namespace": "",
        }
    )
    opt_outs: Optional["PatientRecord.OptOuts"] = field(
        default=None,
        metadata={
            "name": "OptOuts",
            "type": "Element",
            "namespace": "",
        }
    )
    clinical_relationships: Optional["PatientRecord.ClinicalRelationships"] = field(
        default=None,
        metadata={
            "name": "ClinicalRelationships",
            "type": "Element",
            "namespace": "",
        }
    )
    surveys: Optional["PatientRecord.Surveys"] = field(
        default=None,
        metadata={
            "name": "Surveys",
            "type": "Element",
            "namespace": "",
        }
    )
    assessments: Optional["PatientRecord.Assessments"] = field(
        default=None,
        metadata={
            "name": "Assessments",
            "type": "Element",
            "namespace": "",
        }
    )
    pvdata: Optional[Pvdata] = field(
        default=None,
        metadata={
            "name": "PVData",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass
    class SocialHistories:
        social_history: Optional[SocialHistory] = field(
            default=None,
            metadata={
                "name": "SocialHistory",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class FamilyHistories:
        family_history: List[FamilyHistory] = field(
            default_factory=list,
            metadata={
                "name": "FamilyHistory",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Allergies:
        allergy: List[Allergy] = field(
            default_factory=list,
            metadata={
                "name": "Allergy",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Diagnoses:
        """
        :ivar diagnosis: Co-Morbidities
        :ivar cause_of_death: Cause of Death
        :ivar renal_diagnosis: Renal Diagnoses
        """
        diagnosis: List[Diagnosis] = field(
            default_factory=list,
            metadata={
                "name": "Diagnosis",
                "type": "Element",
                "namespace": "",
            }
        )
        cause_of_death: Optional[CauseOfDeath] = field(
            default=None,
            metadata={
                "name": "CauseOfDeath",
                "type": "Element",
                "namespace": "",
            }
        )
        renal_diagnosis: Optional[RenalDiagnosis] = field(
            default=None,
            metadata={
                "name": "RenalDiagnosis",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Medications:
        medication: List[Medication] = field(
            default_factory=list,
            metadata={
                "name": "Medication",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class DialysisPrescriptions:
        dialysis_prescription: List[DialysisPrescription] = field(
            default_factory=list,
            metadata={
                "name": "DialysisPrescription",
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

    @dataclass
    class Procedures:
        """
        :ivar procedure: Procedures (not otherwise Specified)
        :ivar dialysis_sessions: Dialysis Sessions
        :ivar transplant: Transplant Procedures
        :ivar vascular_access: Vascular Access Constructions
        """
        procedure: List[Procedure] = field(
            default_factory=list,
            metadata={
                "name": "Procedure",
                "type": "Element",
                "namespace": "",
            }
        )
        dialysis_sessions: List[DialysisSessions] = field(
            default_factory=list,
            metadata={
                "name": "DialysisSessions",
                "type": "Element",
                "namespace": "",
            }
        )
        transplant: List[TransplantProcedure] = field(
            default_factory=list,
            metadata={
                "name": "Transplant",
                "type": "Element",
                "namespace": "",
            }
        )
        vascular_access: List[VascularAccess] = field(
            default_factory=list,
            metadata={
                "name": "VascularAccess",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Documents:
        document: List[Document] = field(
            default_factory=list,
            metadata={
                "name": "Document",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Encounters:
        """
        :ivar encounter: This is used to record the duration of
            something other than a Treatment. This element should not be
            submitted without prior discussion with the UKRR.
        :ivar treatment: This is used to record the duration a Patient
            received a particular type of Care/Treatment at a particular
            Treatment Facility. It is similar in concept to the UKRR TXT
            records however at the end of the period it should be end-
            dated rather than an additional record being sent. It is
            possible for treatment records to overlap if a patient has
            multiple treatments (such as post-transplant dialysis). A
            treatment record should exist for any period of time where
            they would be considered a patient (so for example code 900
            record for pre-RRT CKD and a code 94 record for post-RRT
            Conservative care). Details of Transplants themselves should
            be recorded as Procedures but Treatment records should be
            used to record periods of Transplant related
            Inpatient/Outpatient care.
        :ivar transplant_list: This is only for NHSBT supplied
            Transplant Waiting List data.
        """
        encounter: List[Encounter] = field(
            default_factory=list,
            metadata={
                "name": "Encounter",
                "type": "Element",
                "namespace": "",
            }
        )
        treatment: List[Treatment] = field(
            default_factory=list,
            metadata={
                "name": "Treatment",
                "type": "Element",
                "namespace": "",
            }
        )
        transplant_list: List[TransplantList] = field(
            default_factory=list,
            metadata={
                "name": "TransplantList",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class ProgramMemberships:
        program_membership: List[ProgramMembership] = field(
            default_factory=list,
            metadata={
                "name": "ProgramMembership",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class OptOuts:
        opt_out: List[OptOut] = field(
            default_factory=list,
            metadata={
                "name": "OptOut",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class ClinicalRelationships:
        clinical_relationship: List[ClinicalRelationship] = field(
            default_factory=list,
            metadata={
                "name": "ClinicalRelationship",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Surveys:
        survey: List[Survey] = field(
            default_factory=list,
            metadata={
                "name": "Survey",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass
    class Assessments:
        assessment: List[Assessment] = field(
            default_factory=list,
            metadata={
                "name": "Assessment",
                "type": "Element",
                "namespace": "",
            }
        )
