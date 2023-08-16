from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfEdtaCodCode(Enum):
    """
    :cvar VALUE_0: Cause of death uncertain / not determined
    :cvar VALUE_11: Myocardial Ischaemia and Infraction
    :cvar VALUE_12: Hyperkalaemia
    :cvar VALUE_13: Haemorrhagic Pericarditis
    :cvar VALUE_14: Other causes of cardiac failure
    :cvar VALUE_15: Cardiac arrest/sudden death; other cause or unknown
    :cvar VALUE_16: Hypertensive cardiac failure
    :cvar VALUE_17: Hypokalaemia
    :cvar VALUE_18: Fluid Overload / Pulmonary Oedema
    :cvar VALUE_19: Elevated PVR / Pulmonary hypertension
    :cvar VALUE_21: Pulmonary Embolus
    :cvar VALUE_22: Cerebro-Vascular Accident, other cause or
        unspecified
    :cvar VALUE_23: Gastro-Intestinal Haemorrhage (Digestive)
    :cvar VALUE_24: Haemorrhage from graft site
    :cvar VALUE_25: Haemorrhage from vascular access or dailysis circuit
    :cvar VALUE_26: Cerebral haemorrhage from ruptured vascular aneurysm
        (not code 22 or 23)
    :cvar VALUE_27: Haemorrhage from surgery (except digestive
        haemorrhage
    :cvar VALUE_28: Other haemorrhage, other site and/or other cause
    :cvar VALUE_29: Mesenteric Infarction
    :cvar VALUE_31: Pulmonary Infection (Bacterial)
    :cvar VALUE_32: Pulmonary Infection (Viral)
    :cvar VALUE_33: Pulmonary Infection (Fungal or Protozoal; parasitic)
    :cvar VALUE_34: Infections elsewhere (except viral hepatitis)
    :cvar VALUE_35: Septicaemia
    :cvar VALUE_36: Tuberculosis (Lung)
    :cvar VALUE_37: Tuberculosis (Elsewhere)
    :cvar VALUE_38: Generalised Viral Infection
    :cvar VALUE_39: Peritonitis (all causes except for Peritoneal
        Dialysis)
    :cvar VALUE_41: Liver disease due to hepatitis B virus
    :cvar VALUE_42: Liver disease due to other viral hepatitis
    :cvar VALUE_43: Liver disease due to drug toxicity
    :cvar VALUE_44: Cirrhosis - not viral (alcoholic or other cause)
    :cvar VALUE_45: Cystic liver disease
    :cvar VALUE_46: Liver failure - cause unknown
    :cvar VALUE_51: Patient refused further treatment for ERF
    :cvar VALUE_52: Suicide
    :cvar VALUE_53: ERF Treatment ceased for any other reason
    :cvar VALUE_54: ERF TReatment withdrawn for medical reasons
    :cvar VALUE_61: Uremia caused by graph failure
    :cvar VALUE_62: Pancreatitis
    :cvar VALUE_63: Bone Marrow Depression (Aplosia)
    :cvar VALUE_64: Cachexia
    :cvar VALUE_66: Malignant disease in patient treated by
        immuosuppressive therapy
    :cvar VALUE_67: Malignant disease: solid tumours except those of 66
    :cvar VALUE_68: Malignant disease: lymphoproliferative disorders
        (Except 66)
    :cvar VALUE_69: Dementia
    :cvar VALUE_70: Peritonitis (sclerosing, with peritoneal dialysis)
    :cvar VALUE_71: Perforation of peptic ulcer
    :cvar VALUE_72: Perforation of colon
    :cvar VALUE_73: COPD
    :cvar VALUE_79: Multi-system failure
    :cvar VALUE_81: Accident related to ERF Treatment
    :cvar VALUE_82: Accident unrelated to ERF Treatment
    :cvar VALUE_99: Cause of death uncertain/not determined
    :cvar VALUE_100: Peritonitis (bacterial, with peritoneal dialysis)
    :cvar VALUE_101: Peritonitis (fungal, with peritoneal dialysis)
    :cvar VALUE_102: Peritonitis (due to other cause, with peritoneal
        dialysis)
    :cvar VALUE_103: Peripheral Vascular Disease
    :cvar VALUE_104: Calciphylaxis
    :cvar VALUE_105: Ischaemic bowel
    :cvar VALUE_106: Ruptured AAA
    :cvar VALUE_107: Advanced CKD not on dialysis (conservative
        management)
    :cvar VALUE_108: Acute Kidney Injury
    :cvar VALUE_109: C Diff Colitis
    :cvar VALUE_110: Line Related Sepsis
    """
    VALUE_0 = "0"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_35 = "35"
    VALUE_36 = "36"
    VALUE_37 = "37"
    VALUE_38 = "38"
    VALUE_39 = "39"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_44 = "44"
    VALUE_45 = "45"
    VALUE_46 = "46"
    VALUE_51 = "51"
    VALUE_52 = "52"
    VALUE_53 = "53"
    VALUE_54 = "54"
    VALUE_61 = "61"
    VALUE_62 = "62"
    VALUE_63 = "63"
    VALUE_64 = "64"
    VALUE_66 = "66"
    VALUE_67 = "67"
    VALUE_68 = "68"
    VALUE_69 = "69"
    VALUE_70 = "70"
    VALUE_71 = "71"
    VALUE_72 = "72"
    VALUE_73 = "73"
    VALUE_79 = "79"
    VALUE_81 = "81"
    VALUE_82 = "82"
    VALUE_99 = "99"
    VALUE_100 = "100"
    VALUE_101 = "101"
    VALUE_102 = "102"
    VALUE_103 = "103"
    VALUE_104 = "104"
    VALUE_105 = "105"
    VALUE_106 = "106"
    VALUE_107 = "107"
    VALUE_108 = "108"
    VALUE_109 = "109"
    VALUE_110 = "110"


class CfEdtaCodCodingStandard(Enum):
    EDTA_COD = "EDTA_COD"


@dataclass
class CfEdtaCod:
    class Meta:
        name = "CF_EDTA_COD"

    coding_standard: Optional[CfEdtaCodCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfEdtaCodCode] = field(
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
            "max_length": 255,
        }
    )
