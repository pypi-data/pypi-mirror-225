from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from xsdata.models.datatype import XmlDate, XmlDateTime


@dataclass
class BodyPartsAffected:
    class Meta:
        name = "body_parts_affected"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 60,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Drug:
    class Meta:
        name = "drug"

    drugstartdate: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    drugname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "max_length": 110,
        }
    )
    drugdose: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "max_length": 1000,
        }
    )
    code: Optional["Drug.Code"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class Code:
        codetype: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )
        codevalue: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )


@dataclass
class FamilyHistory:
    class Meta:
        name = "family_history"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 60,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class IbdDiseaseComplications:
    class Meta:
        name = "ibd_disease_complications"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 60,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


class IbdDiseaseExtent(Enum):
    """
    IBD Disease Extent.
    """
    PROCTITIS = "Proctitis"
    LEFT_SIDED_COLITIS = "Left Sided Colitis"
    EXTENSIVE_COLITIS = "Extensive Colitis"
    ILEAL_CROHNS = "Ileal Crohns"
    ILEO_COLONIC_DISEASE = "Ileo-Colonic Disease"
    CROHNS_COLITIS = "Crohns Colitis"
    ISOLATED_UPPER_GI_DISEASE = "Isolated Upper GI Disease"


@dataclass
class Letter:
    """
    :ivar letterdate:
    :ivar lettertitle:
    :ivar letterfilename:
    :ivar letterfiletype:
    :ivar lettertype:
    :ivar lettercontent: Letter content should be sent as a CDATA
        section to avoid parsing errors. E.g. and end with the string
    :ivar letterfilebody: This property is used when the Note is binary
        data, e.g DOC, PDF, JPG
    """
    class Meta:
        name = "letter"

    letterdate: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    lettertitle: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    letterfilename: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    letterfiletype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    lettertype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "max_length": 50,
        }
    )
    lettercontent: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    letterfilebody: Optional[bytes] = field(
        default=None,
        metadata={
            "type": "Element",
            "format": "base64",
        }
    )


class Prepost(Enum):
    """
    Pre or Post Dialysis Result.
    """
    PRE = "PRE"
    POST = "POST"


@dataclass
class PvDiagnosis:
    class Meta:
        name = "pv_diagnosis"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 150,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


class PvStatus(Enum):
    """
    Patient View Status.
    """
    INCLUDE = "Include"
    REMOVE = "Remove"
    LOST = "Lost"
    DIED = "Died"
    SUSPEND = "Suspend"
    FOLLOWUP = "Followup"


class Rrtstatus(Enum):
    """
    RRT Treatment Modality.
    """
    HD = "HD"
    PD = "PD"
    TP = "TP"
    GEN = "GEN"
    XFER = "XFER"


class Sex(Enum):
    """
    Sex.
    """
    M = "M"
    F = "F"
    U = "U"


@dataclass
class SmokingHistory:
    class Meta:
        name = "smoking_history"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 60,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class SurgicalHistory:
    class Meta:
        name = "surgical_history"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 60,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class VaccinationRecord:
    class Meta:
        name = "vaccination_record"

    value: str = field(
        default="",
        metadata={
            "required": True,
            "max_length": 60,
        }
    )
    primary: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        }
    )


@dataclass
class Drugdetails:
    class Meta:
        name = "drugdetails"

    drug: List[Drug] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Letterdetails:
    class Meta:
        name = "letterdetails"

    letter: List[Letter] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Result:
    class Meta:
        name = "result"

    datestamp: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    prepost: Optional[Prepost] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "max_length": 20,
        }
    )


@dataclass
class Test:
    class Meta:
        name = "test"

    testname: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
            "max_length": 40,
        }
    )
    testcode: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    units: Optional[str] = field(
        default=None,
        metadata={
            "type": "Element",
            "max_length": 20,
        }
    )
    daterange: Optional["Test.Daterange"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    result: List[Result] = field(
        default_factory=list,
        metadata={
            "type": "Element",
        }
    )

    @dataclass
    class Daterange:
        start: Optional[XmlDate] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )
        stop: Optional[XmlDate] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            }
        )


@dataclass
class Testdetails:
    class Meta:
        name = "testdetails"

    test: List[Test] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        }
    )


@dataclass
class Patientview:
    """
    PatientView XML Schema.
    """
    class Meta:
        name = "patientview"

    sequence: Optional[int] = field(
        default=None,
        metadata={
            "type": "Element",
            "min_inclusive": 0,
            "max_inclusive": 999999,
            "total_digits": 6,
        }
    )
    dateofreport: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    flag: Optional[PvStatus] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    centredetails: Optional["Patientview.Centredetails"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )
    gpdetails: Optional["Patientview.Gpdetails"] = field(
        default=None,
        metadata={
            "type": "Element",
        }
    )
    patient: Optional["Patientview.Patient"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        }
    )

    @dataclass
    class Centredetails:
        centrecode: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        centrename: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 60,
            }
        )
        centreaddress1: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        centreaddress2: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        centreaddress3: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        centreaddress4: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        centrepostcode: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 20,
            }
        )
        centretelephone: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        centreemail: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )

    @dataclass
    class Gpdetails:
        gpname: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 50,
            }
        )
        gpaddress1: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        gpaddress2: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        gpaddress3: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        gpaddress4: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        gppostcode: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 20,
            }
        )
        gptelephone: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )
        gpemail: Optional[str] = field(
            default=None,
            metadata={
                "type": "Element",
                "max_length": 100,
            }
        )

    @dataclass
    class Patient:
        personaldetails: Optional["Patientview.Patient.Personaldetails"] = field(
            default=None,
            metadata={
                "type": "Element",
                "required": True,
            }
        )
        clinicaldetails: Optional["Patientview.Patient.Clinicaldetails"] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )
        testdetails: Optional[Testdetails] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )
        drugdetails: Optional[Drugdetails] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )
        letterdetails: Optional[Letterdetails] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )
        diagnostics: Optional["Patientview.Patient.Diagnostics"] = field(
            default=None,
            metadata={
                "type": "Element",
            }
        )
        footcheckup: List["Patientview.Patient.Footcheckup"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
            }
        )
        eyecheckup: List["Patientview.Patient.Eyecheckup"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
            }
        )
        allergy: List["Patientview.Patient.Allergy"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
            }
        )

        @dataclass
        class Personaldetails:
            surname: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                    "max_length": 30,
                }
            )
            forename: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                    "max_length": 30,
                }
            )
            dateofbirth: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            sex: Optional[Sex] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            nhsno: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                    "length": 10,
                    "white_space": "collapse",
                }
            )
            ethnicorigin: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            hospitalnumber: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 30,
                }
            )
            address1: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 60,
                }
            )
            address2: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 60,
                }
            )
            address3: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 60,
                }
            )
            address4: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 60,
                }
            )
            postcode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 10,
                }
            )
            telephone1: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 100,
                }
            )
            telephone2: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 100,
                }
            )
            mobile: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 100,
                }
            )

        @dataclass
        class Clinicaldetails:
            rrtstatus: Optional[Rrtstatus] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            tpstatus: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 70,
                }
            )
            diagnosisedta: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 5,
                }
            )
            diagnosisdate: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            diagnosis: List[PvDiagnosis] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )
            ibddiseaseextent: Optional[IbdDiseaseExtent] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            ibddiseasecomplications: Optional[IbdDiseaseComplications] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            bodypartsaffected: List[BodyPartsAffected] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )
            familyhistory: List[FamilyHistory] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )
            smokinghistory: Optional[SmokingHistory] = field(
                default=None,
                metadata={
                    "type": "Element",
                }
            )
            surgicalhistory: List[SurgicalHistory] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )
            vaccinationrecord: List[VaccinationRecord] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                }
            )
            bloodgroup: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "max_length": 30,
                }
            )

        @dataclass
        class Diagnostics:
            diagnostic: List["Patientview.Patient.Diagnostics.Diagnostic"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                }
            )

            @dataclass
            class Diagnostic:
                diagnosticdate: Optional[XmlDateTime] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "required": True,
                    }
                )
                diagnosticresult: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "required": True,
                    }
                )
                diagnosticname: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                        "required": True,
                    }
                )
                diagnostictype: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )

        @dataclass
        class Footcheckup:
            datestamp: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            foot: List["Patientview.Patient.Footcheckup.Foot"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                }
            )

            @dataclass
            class Foot:
                ptpulse: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                dppulse: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                side: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class Eyecheckup:
            datestamp: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            location: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            eye: List["Patientview.Patient.Eyecheckup.Eye"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                }
            )

            @dataclass
            class Eye:
                rgrade: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                mgrade: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                va: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Element",
                    }
                )
                side: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                        "required": True,
                    }
                )

        @dataclass
        class Allergy:
            allergysubstance: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergytypecode: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergyreaction: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergyconfidencelevel: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergyinfosource: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergystatus: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergydescription: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
            allergyrecordeddate: Optional[XmlDate] = field(
                default=None,
                metadata={
                    "type": "Element",
                    "required": True,
                }
            )
