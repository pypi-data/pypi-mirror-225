from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfRr7TreatmentCode(Enum):
    """
    :cvar VALUE_1: Haemodialysis
    :cvar VALUE_2: Haemofiltration
    :cvar VALUE_3: Haemodiafiltration
    :cvar VALUE_5: Ultrafiltration
    :cvar VALUE_10: CAPD Connect
    :cvar VALUE_11: CAPD Disconnect
    :cvar VALUE_12: Cycling PD &gt;= 6 Nights/Week Dry
    :cvar VALUE_13: Cycling PD &lt; 6 Nights/Week Dry
    :cvar VALUE_14: Cycling PD &gt;= 6 Nights/Week Wet (Day Dwell)
    :cvar VALUE_15: Cycling PD &lt; 6 Nights/Week Wet (Day Dwell)
    :cvar VALUE_16: Assisted Cycling PD &gt;= 6 nights/week dry
    :cvar VALUE_17: Assisted Cycling PD &gt;= 6 nights/week wet (day
        dwell)
    :cvar VALUE_20: Transplant; Cadaver Donor
    :cvar VALUE_78: Transplant; Live Donor
    :cvar VALUE_29: Transplant; Type Unknown
    :cvar VALUE_120: Transplant Clinic Followup
    :cvar VALUE_81: Acute Kidney Injury - Haemodialysis
    :cvar VALUE_82: Acute Kidney Injury - Haemofiltration
    :cvar VALUE_83: Acute Kidney Injury - Peritoneal Dialysis
    :cvar VALUE_101: First Assessment by Renal Service
    :cvar VALUE_93: Conservative Management - Mutual decision not to
        offer RRT
    :cvar VALUE_94: Conservative Management - Clinical decision not to
        offer RRT
    :cvar VALUE_110: Plasmapharesis / Plasma Exchange
    :cvar VALUE_111: Assisted CAPD
    :cvar VALUE_121: Assisted APD
    :cvar VALUE_201: Hybrid CAPD with HD
    :cvar VALUE_202: Hybrid APD with HD
    :cvar VALUE_203: Hybrid APD with CAPD
    :cvar VALUE_900: CKD (Not on RRT)
    :cvar VALUE_4: Haemodialysis &gt; 4 days per week / daily
    :cvar VALUE_9: Haemodialysis - type unknown
    :cvar VALUE_19: Peritoneal Dialysis - Type Unknown
    :cvar VALUE_21: Transplant; Live Related - Sibling
    :cvar VALUE_22: Transplant; Live Related - Parent or Child
    :cvar VALUE_23: Transplant; Live Related - Other
    :cvar VALUE_24: Transplant; Live Genetically Unrelated
    :cvar VALUE_25: Transplant; Cadaver + Transp Other Organ
    :cvar VALUE_26: Transplant; Live Donor + Transp Other Organ
    :cvar VALUE_27: Transplant; Live donor Non-UK Transplant
    :cvar VALUE_28: Transplant; Non-Heart-beating Donor
    :cvar VALUE_31: Graft acute rejection episode - biopsy proven
    :cvar VALUE_32: Graft acute rejection episode - no biopsy
    :cvar VALUE_74: Transplant : Live related - father
    :cvar VALUE_75: Transplant : Live related - mother
    :cvar VALUE_77: Transplant : Live related - child
    :cvar VALUE_80: Acute Renal Failure not dialysed
    """
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_5 = "5"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_20 = "20"
    VALUE_78 = "78"
    VALUE_29 = "29"
    VALUE_120 = "120"
    VALUE_81 = "81"
    VALUE_82 = "82"
    VALUE_83 = "83"
    VALUE_101 = "101"
    VALUE_93 = "93"
    VALUE_94 = "94"
    VALUE_110 = "110"
    VALUE_111 = "111"
    VALUE_121 = "121"
    VALUE_201 = "201"
    VALUE_202 = "202"
    VALUE_203 = "203"
    VALUE_900 = "900"
    VALUE_4 = "4"
    VALUE_9 = "9"
    VALUE_19 = "19"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_74 = "74"
    VALUE_75 = "75"
    VALUE_77 = "77"
    VALUE_80 = "80"


class CfRr7TreatmentCodingStandard(Enum):
    CF_RR7_TREATMENT = "CF_RR7_TREATMENT"


@dataclass
class CfRr7Treatment:
    class Meta:
        name = "CF_RR7_TREATMENT"

    coding_standard: Optional[CfRr7TreatmentCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfRr7TreatmentCode] = field(
        default=None,
        metadata={
            "name": "Code",
            "type": "Element",
            "namespace": "",
        }
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "",
            "max_length": 32000,
        }
    )
