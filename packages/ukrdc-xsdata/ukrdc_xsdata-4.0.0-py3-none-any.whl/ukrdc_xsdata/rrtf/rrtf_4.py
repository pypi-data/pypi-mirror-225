from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional


class PicklistEpoFreq(Enum):
    """
    :cvar VALUE_2XW: 2 Times per Week
    :cvar VALUE_3XW: 3 Times per Week
    :cvar VALUE_1W: Every Week
    :cvar VALUE_2W: Every 2 Weeks
    :cvar VALUE_3W: Every 3 Weeks
    :cvar VALUE_4W: Every 4 Weeks
    :cvar VALUE_5W: Every 5 Weeks
    :cvar VALUE_6W: Every 6 Weeks
    :cvar VALUE_7W: Every 7 Weeks
    :cvar VALUE_8W: Every 8 Weeks
    """
    VALUE_2XW = "2xw"
    VALUE_3XW = "3xw"
    VALUE_1W = "1w"
    VALUE_2W = "2w"
    VALUE_3W = "3w"
    VALUE_4W = "4w"
    VALUE_5W = "5w"
    VALUE_6W = "6w"
    VALUE_7W = "7w"
    VALUE_8W = "8w"


class PicklistPat36(Enum):
    """
    :cvar GP: GP
    :cvar CN: Hospital
    """
    GP = "GP"
    CN = "CN"


class PicklistRr10(Enum):
    """
    :cvar VALUE_10: Hyperacute rejection
    :cvar VALUE_11: Non viable transplant kidney
    :cvar VALUE_12: Primary non function of transplant kidney
    :cvar VALUE_13: Acute rejection
    :cvar VALUE_14: Chronic allograft nephropathy
    :cvar VALUE_15: Rejection following withdrawal of immunosuppression
        - non compliance
    :cvar VALUE_16: Rejection following withdrawal of immunosuppression
        - medical reason
    :cvar VALUE_20: De novo glomerulonephritis
    :cvar VALUE_21: Interstitial nephritis - viral - BKV
    :cvar VALUE_22: Interstitial nephritis - viral - other
    :cvar VALUE_23: Interstitial nephritis - drug induced
    :cvar VALUE_24: Interstitial nephritis - other
    :cvar VALUE_25: Transplant pyelonephritis
    :cvar VALUE_26: Calcineurin inhibitor nephrotoxicity
    :cvar VALUE_27: Non calcineurin inhibitor drug toxicity
    :cvar VALUE_28: Recurrent primary renal disease
    :cvar VALUE_40: Obstruction of transplant kidney
    :cvar VALUE_41: Transplant arterial thrombosis
    :cvar VALUE_42: Transplant venous thrombosis
    :cvar VALUE_43: Transplant infarction - cause unknown
    :cvar VALUE_44: Transplant renal artery stenosis
    :cvar VALUE_45: Surgical removal of transplant
    :cvar VALUE_46: Surgical trauma to transplant
    :cvar VALUE_47: Non surgical trauma to transplant kidney
    :cvar VALUE_48: Haemorrhage post transplant biopsy
    :cvar VALUE_70: Malignant disease of the transplant kidney/ureter
    :cvar VALUE_71: Malignant disease - other
    :cvar VALUE_90: Death with functioning graft
    :cvar VALUE_98: Other
    :cvar VALUE_99: Unknown
    """
    VALUE_10 = 10
    VALUE_11 = 11
    VALUE_12 = 12
    VALUE_13 = 13
    VALUE_14 = 14
    VALUE_15 = 15
    VALUE_16 = 16
    VALUE_20 = 20
    VALUE_21 = 21
    VALUE_22 = 22
    VALUE_23 = 23
    VALUE_24 = 24
    VALUE_25 = 25
    VALUE_26 = 26
    VALUE_27 = 27
    VALUE_28 = 28
    VALUE_40 = 40
    VALUE_41 = 41
    VALUE_42 = 42
    VALUE_43 = 43
    VALUE_44 = 44
    VALUE_45 = 45
    VALUE_46 = 46
    VALUE_47 = 47
    VALUE_48 = 48
    VALUE_70 = 70
    VALUE_71 = 71
    VALUE_90 = 90
    VALUE_98 = 98
    VALUE_99 = 99


class PicklistRr14(Enum):
    """
    :cvar VALUE_10: Heart
    :cvar VALUE_11: Lungs
    :cvar VALUE_12: Liver
    :cvar VALUE_13: Pancreas
    :cvar VALUE_14: Intestines
    """
    VALUE_10 = 10
    VALUE_11 = 11
    VALUE_12 = 12
    VALUE_13 = 13
    VALUE_14 = 14


class PicklistRr15(Enum):
    """
    :cvar VALUE_0: None
    :cvar VALUE_1: Aspirin
    :cvar VALUE_2: LMW Heparin
    :cvar VALUE_3: Heparin
    :cvar VALUE_4: Warfarin
    :cvar VALUE_9: Other
    """
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_9 = 9


class PicklistRr16(Enum):
    """
    :cvar VALUE_0: None
    :cvar VALUE_1: Aciclovir
    :cvar VALUE_2: Ganciclovir
    :cvar VALUE_3: Valganciclovir
    :cvar VALUE_4: CMV immunoglobulin
    :cvar VALUE_9: Other
    """
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_9 = 9


class PicklistRr17(Enum):
    """
    :cvar VALUE_0: None
    :cvar VALUE_1: Dapsone
    :cvar VALUE_2: Co-trimoxazole
    :cvar VALUE_9: Other
    """
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_9 = 9


class PicklistRr18(Enum):
    """
    :cvar A: White - British
    :cvar B: White - Irish
    :cvar C: Other White background
    :cvar D: Mixed - White and Black Caribbean
    :cvar E: Mixed - White and Black African
    :cvar F: Mixed - White and Asian
    :cvar G: Other Mixed background
    :cvar H: Asian or Asian British - Indian
    :cvar J: Asian or Asian British - Pakistani
    :cvar K: Asian or Asian British - Bangladeshi
    :cvar L: Other Asian background
    :cvar M: Black Caribbean
    :cvar N: Black African
    :cvar P: Other Black background
    :cvar R: Chinese
    :cvar S: Other ethnic background
    :cvar Z: Refused / Not stated
    """
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    P = "P"
    R = "R"
    S = "S"
    Z = "Z"


class PicklistRr2(Enum):
    """
    :cvar S: Single
    :cvar M: Married
    :cvar C: Cohabitating
    :cvar D: Divorced
    :cvar P: Separated
    :cvar W: Widowed
    :cvar U: Unknown
    """
    S = "S"
    M = "M"
    C = "C"
    D = "D"
    P = "P"
    W = "W"
    U = "U"


class PicklistRr21(Enum):
    """
    :cvar VALUE_101: Self care
    :cvar VALUE_102: Self care + Clinical staff
    :cvar VALUE_103: Self care + Family member
    :cvar VALUE_104: Self care + other
    :cvar VALUE_201: Clinical staff
    :cvar VALUE_301: Family member
    :cvar VALUE_999: Other
    """
    VALUE_101 = 101
    VALUE_102 = 102
    VALUE_103 = 103
    VALUE_104 = 104
    VALUE_201 = 201
    VALUE_301 = 301
    VALUE_999 = 999


class PicklistRr22(Enum):
    """
    :cvar VALUE_1: Oral
    :cvar VALUE_2: Topical
    :cvar VALUE_3: Inhalation
    :cvar VALUE_4: Injection
    :cvar VALUE_5: Intra peritoneal
    :cvar VALUE_9: Other - specified in comments
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_9 = 9


class PicklistRr23(Enum):
    """
    :cvar L: litres
    :cvar DL: decilitres
    :cvar ML: mililitres
    :cvar G: grams
    :cvar MG: miligrams
    :cvar G_1: micrograms
    :cvar NG: nanograms
    :cvar TAB: tablets
    :cvar UNITS: units (i.e. for Epoetins)
    :cvar MMOL: milimols
    :cvar OTHER: Other - specified in comments
    """
    L = "L"
    DL = "dl"
    ML = "ml"
    G = "g"
    MG = "mg"
    G_1 = "µg"
    NG = "ng"
    TAB = "Tab"
    UNITS = "Units"
    MMOL = "mmol"
    OTHER = "Other"


class PicklistRr24(Enum):
    """
    :cvar VALUE_20: Transplant ; Cadaver donor
    :cvar VALUE_21: Transplant ; Live related - sibling
    :cvar VALUE_74: Transplant ; Live related - father
    :cvar VALUE_75: Transplant ; Live related - mother
    :cvar VALUE_77: Transplant ; Live related - child
    :cvar VALUE_23: Transplant ; Live related - other
    :cvar VALUE_24: Transplant ; Live genetically unrelated
    :cvar VALUE_25: Transplant ; Cadaver donor + transp other organ
    :cvar VALUE_26: Transplant ; Live donor + transplant other organ
    :cvar VALUE_27: Transplant ; Live donor non-UK transplant
    :cvar VALUE_28: Transplant ; non-heart-beating donor
    :cvar VALUE_29: Transplant ; type unknown
    """
    VALUE_20 = 20
    VALUE_21 = 21
    VALUE_74 = 74
    VALUE_75 = 75
    VALUE_77 = 77
    VALUE_23 = 23
    VALUE_24 = 24
    VALUE_25 = 25
    VALUE_26 = 26
    VALUE_27 = 27
    VALUE_28 = 28
    VALUE_29 = 29


class PicklistRr27(Enum):
    """
    :cvar VALUE_1: Bladder
    :cvar VALUE_2: Bladder + CIC
    :cvar VALUE_3: Augmented bladder
    :cvar VALUE_4: Urinary diversion
    :cvar VALUE_5: Bladder with drainage procedure e.g. mitrofanoff
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5


class PicklistRr28(Enum):
    """
    :cvar VALUE_1: MRSA
    :cvar VALUE_2: MSSA
    :cvar VALUE_3: E Coli
    :cvar VALUE_4: Fungal
    :cvar VALUE_5: Coagulase negative Staphyloccus
    :cvar VALUE_6: Streptococcus + Enterococcus
    :cvar VALUE_7: Staphylococcus aureus
    :cvar VALUE_8: Pseudomonas Aeruginosa
    :cvar VALUE_9: Culture negative peritonitis
    :cvar VALUE_10: Other gram positive micro organism
    :cvar VALUE_11: Other gram negative micro organism
    :cvar VALUE_13: Mycobacteria
    :cvar VALUE_88: Other
    :cvar VALUE_99: Unknown
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7
    VALUE_8 = 8
    VALUE_9 = 9
    VALUE_10 = 10
    VALUE_11 = 11
    VALUE_13 = 13
    VALUE_88 = 88
    VALUE_99 = 99


class PicklistRr29(Enum):
    """
    :cvar VALUE_100: Peritonitis
    :cvar VALUE_101: Peritonitis - Acute Severe
    :cvar VALUE_102: Peritonitis - Refractory
    :cvar VALUE_103: Peritonitis - Relapsing
    :cvar VALUE_104: Peritonitis - Recurrent
    :cvar VALUE_105: Peritonitis - Simple
    :cvar VALUE_120: Exit Site Infection
    :cvar VALUE_121: Exit Site Infection without Tunnel infection
    :cvar VALUE_123: Tunnel infection
    :cvar VALUE_200: Catheter Blockage
    :cvar VALUE_201: Catheter Blockage - Fibrin
    :cvar VALUE_202: Catheter Blockage - Omental Wrap
    :cvar VALUE_203: Catheter Blockage - Adhesions
    :cvar VALUE_204: Catheter Blockage - misplaced (intra peritoneal)
    :cvar VALUE_209: Catheter Blockage - cause unclear
    :cvar VALUE_300: Catheter Displacement
    :cvar VALUE_301: Catheter Displacement - Cuff Extrusion
    :cvar VALUE_302: Catheter Displacement - fell out
    :cvar VALUE_303: Catheter Displacement - failed or unsuccessful
        attempt to reinsert
    :cvar VALUE_400: Solute-Related
    :cvar VALUE_401: Solute-Related - inadequate clearance - defined by
        either Kt/V or Creatinine clearance
    :cvar VALUE_402: Solute-Related - inadequate clearance - phosphate
        clearance
    :cvar VALUE_403: Solute-Related - Uraemic symptoms
    :cvar VALUE_404: Solute-Related - Clinical signs of poor nutrition
    :cvar VALUE_405: Solute-Related - Hypoalbuminaemia
    :cvar VALUE_406: Solute-Related - Loss of residual renal function
    :cvar VALUE_407: Solute-Related - patient size
    :cvar VALUE_420: Fluid-UF-Related
    :cvar VALUE_421: Fluid-UF-Related - UF failure - PET Defined
    :cvar VALUE_422: Fluid-UF-Related - Unable to remove excess body
        water
    :cvar VALUE_423: Fluid-UF-Related - Unwillingness to Prescribe More
        Dialysate Glucose to Achieve Sufficient UF
    :cvar VALUE_424: Fluid-UF-Related - excess fluid removal
    :cvar VALUE_500: Leaks
    :cvar VALUE_501: Leaks - scrotal oedema
    :cvar VALUE_502: Leaks - Pleuro-Peritoneal Leak
    :cvar VALUE_503: Leaks - Abdominal Wall
    :cvar VALUE_504: Leaks - elsewhere
    :cvar VALUE_520: Hernia
    :cvar VALUE_521: Hernia - inguinal
    :cvar VALUE_522: Hernia - peri-umbilical
    :cvar VALUE_523: Hernia - elsewhere
    :cvar VALUE_600: Psychosocial
    :cvar VALUE_601: Psychosocial - Patient Choice
    :cvar VALUE_602: Psychosocial - Severe Depression
    :cvar VALUE_603: Psychosocial - Caregiver Choice
    :cvar VALUE_604: Psychosocial - Change in Circumstance (e.g., Death
        of Caregiver, Change in Job, etc.)
    :cvar VALUE_620: Medical
    :cvar VALUE_621: Medical - Physical Incapacity
    :cvar VALUE_622: Medical - Mental Incapacity
    :cvar VALUE_700: Diagnosed EPS
    :cvar VALUE_701: Risk or Possibility of EPS
    :cvar VALUE_702: Time on PD
    :cvar VALUE_703: GI Symptoms but Not Formally Diagnosed with EPS
    :cvar VALUE_800: Haemoperitoneum
    :cvar VALUE_801: Intra-Abdominal Pathology
    :cvar VALUE_802: Unexplained Cachexia/failure to Thrive
    :cvar VALUE_803: Other Reason not Included Elsewhere
    :cvar VALUE_804: Recovery of renal function
    :cvar VALUE_805: Removal post transplant
    :cvar VALUE_806: Removal with other modality change
    """
    VALUE_100 = 100
    VALUE_101 = 101
    VALUE_102 = 102
    VALUE_103 = 103
    VALUE_104 = 104
    VALUE_105 = 105
    VALUE_120 = 120
    VALUE_121 = 121
    VALUE_123 = 123
    VALUE_200 = 200
    VALUE_201 = 201
    VALUE_202 = 202
    VALUE_203 = 203
    VALUE_204 = 204
    VALUE_209 = 209
    VALUE_300 = 300
    VALUE_301 = 301
    VALUE_302 = 302
    VALUE_303 = 303
    VALUE_400 = 400
    VALUE_401 = 401
    VALUE_402 = 402
    VALUE_403 = 403
    VALUE_404 = 404
    VALUE_405 = 405
    VALUE_406 = 406
    VALUE_407 = 407
    VALUE_420 = 420
    VALUE_421 = 421
    VALUE_422 = 422
    VALUE_423 = 423
    VALUE_424 = 424
    VALUE_500 = 500
    VALUE_501 = 501
    VALUE_502 = 502
    VALUE_503 = 503
    VALUE_504 = 504
    VALUE_520 = 520
    VALUE_521 = 521
    VALUE_522 = 522
    VALUE_523 = 523
    VALUE_600 = 600
    VALUE_601 = 601
    VALUE_602 = 602
    VALUE_603 = 603
    VALUE_604 = 604
    VALUE_620 = 620
    VALUE_621 = 621
    VALUE_622 = 622
    VALUE_700 = 700
    VALUE_701 = 701
    VALUE_702 = 702
    VALUE_703 = 703
    VALUE_800 = 800
    VALUE_801 = 801
    VALUE_802 = 802
    VALUE_803 = 803
    VALUE_804 = 804
    VALUE_805 = 805
    VALUE_806 = 806


class PicklistRr30(Enum):
    """
    :cvar VALUE_1: Sporadic
    :cvar VALUE_2: Recessive
    :cvar VALUE_3: Dominant
    :cvar VALUE_4: X linked
    :cvar VALUE_5: Mitochondrial
    :cvar VALUE_6: Uncertain
    :cvar VALUE_9: None
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_9 = 9


class PicklistRr31(Enum):
    """
    :cvar VALUE_1: Mental - Mainstream - Would be capable of mainstream
        education with no support
    :cvar VALUE_2: Mental - Mainstream + support - Would be capable of
        attending mainstream education but would need special support
    :cvar VALUE_3: Mental - Special - Incapable of attending mainstream
        education
    :cvar VALUE_4: Physical - Mainstream - Would be capable of
        mainstream education with no support
    :cvar VALUE_5: Physical - Mainstream + support - Would be capable of
        attending mainstream education but would need special support
    :cvar VALUE_6: Physical - Special - Incapable of attending
        mainstream education
    :cvar VALUE_7: Visual - Normal +/- glasses - Normal vision or good
        vision with spectacles
    :cvar VALUE_8: Visual - Partially sighted - Partially sighted even
        with spectacles
    :cvar VALUE_9: Visual - Blind - Blind or near blind
    :cvar VALUE_10: Auditory - Normal +/- aids - Normal hearing or near
        normal hearing with or without aids
    :cvar VALUE_11: Auditory - Poor even with aids - Poor hearing even
        with aids
    :cvar VALUE_12: Auditory - Profoundly deaf - Deaf despite aids
    """
    VALUE_1 = 1
    VALUE_2 = 2
    VALUE_3 = 3
    VALUE_4 = 4
    VALUE_5 = 5
    VALUE_6 = 6
    VALUE_7 = 7
    VALUE_8 = 8
    VALUE_9 = 9
    VALUE_10 = 10
    VALUE_11 = 11
    VALUE_12 = 12


class PicklistRr4(Enum):
    """
    :cvar VALUE_0: Chronic Renal Failure, Aetiology uncertain
    :cvar VALUE_10: Glomerulonephritis, historically not examined
    :cvar VALUE_11: Severe nephoritic syndrome with focal sclerosis
        (Paediatric)
    :cvar VALUE_12: IgA nephropathy proven by immunofluoresence
    :cvar VALUE_13: Dense deposite disease, membrano-prolif. GN Type II
    :cvar VALUE_14: Membranous nephropathy
    :cvar VALUE_15: Membrano-proliferative GN Type I
    :cvar VALUE_16: Rapidly progressive GN without systemic disease
        (crescentic)
    :cvar VALUE_17: Focal segmental glomeruloscerosis with nephrotic
        syndrome in adults
    :cvar VALUE_19: Glomerulonephritis, historically examined
    :cvar VALUE_20: Pyelo/Interstital nephritis - cause not specified
    :cvar VALUE_21: Pyelo/Interstital nephritis - with neurogenic
        bladder
    :cvar VALUE_22: Pyelo/Interstital nephritis - congen. obst. uropathy
        +/- reflux
    :cvar VALUE_23: Pyelo/Interstital nephritis - acquired obst.
        uropathy
    :cvar VALUE_24: Pyelo/Interstital nephritis - vesico-ureteric reflux
        no obstruction
    :cvar VALUE_25: Pyelo/Interstital nephritis - due to urolithiasis
    :cvar VALUE_29: Pyelo/Interstital nephritis - due to other cause
        (please specify)
    :cvar VALUE_30: Tubulo interstital nephritis (not pyelonephritis)
    :cvar VALUE_31: Nephropathy due to analgesic drugs
    :cvar VALUE_32: Nephropathy due to cis-platinum
    :cvar VALUE_33: Nephropathy due to Cyclosporin A
    :cvar VALUE_34: Lead induced nephropathy (interstitial)
    :cvar VALUE_39: Nephroapthy caused by other specific drug
    :cvar VALUE_40: Cystic Kidney Disease - Type Unspecified
    :cvar VALUE_41: Polycystic Kidneys - Adult Type (Dominant)
    :cvar VALUE_42: Polycystic Kidneys = Infantile (Recessive)
    :cvar VALUE_43: Medullary Cystic Disease - including
        Nephoronophthisis
    :cvar VALUE_49: Cystic Kidney Disease - Other Specified Type
    :cvar VALUE_50: Hereditary/Familial Nephropathy - Typoe Unspecified
    :cvar VALUE_51: Hereditary Nephritis with Nerve Deafness (Alport's)
    :cvar VALUE_52: Cystinosis
    :cvar VALUE_53: Primary Oxalosis
    :cvar VALUE_54: Fabry's disease
    :cvar VALUE_59: Hereditary Nephropathy - Other
    :cvar VALUE_60: congenital Renal Hypoplasia - Type Unspecified
    :cvar VALUE_61: Oligomeganephronic Hypoplasia
    :cvar VALUE_63: Congenital Renal Dysplasia +/- Urinary Tract
        Malformation
    :cvar VALUE_66: Syndrome of Agenesis of Abdo. muscles - Prune Belly
        Syndrome
    :cvar VALUE_70: Renal Vascular Disease - Type Unspecified
    :cvar VALUE_71: Renal Vascular Disease due to MALIGNANT Hypertension
    :cvar VALUE_72: Renal Vascular Disease due to Hypertension
    :cvar VALUE_73: Renal Vascular Disease due to Polyarteritis
    :cvar VALUE_74: Wegener's Granulomatosis
    :cvar VALUE_75: Ischaemic Renal Disease/Cholesterol Embolism
    :cvar VALUE_76: Glomerulonephritis related to liver cirrhosis
    :cvar VALUE_78: Cryoglobulinaemic Glomerulonephritis
    :cvar VALUE_79: Renal Vascular Disease - Classified (Please Specify)
    :cvar VALUE_80: Diabetes Type 1 (Insulin Dependent)
    :cvar VALUE_81: Diabetes Type 2 (Non-Insulin Dependent)
    :cvar VALUE_82: Myelomatosis
    :cvar VALUE_83: Amyloid
    :cvar VALUE_84: Systemic Lupus Erythematosus
    :cvar VALUE_85: Henoch-Schonlein Purpura
    :cvar VALUE_86: Goodpastures Syndrome
    :cvar VALUE_87: Scleroderma
    :cvar VALUE_88: Haemolytic Uraemic Syndrome
    :cvar VALUE_89: Multu-System Diseased - Type Unspecified
    :cvar VALUE_90: Cortical or Tubula Necrosis
    :cvar VALUE_91: Tuberculosis
    :cvar VALUE_92: Gout
    :cvar VALUE_93: Nephrocalcinosis / Hypercalcaemic Nephropathy
    :cvar VALUE_94: Balkan Nephropathy
    :cvar VALUE_95: Kidney Tumour
    :cvar VALUE_96: Traumatic or Surgical Loss of Kidney
    :cvar VALUE_99: Other identified Renal Disorders - Please Specify
    """
    VALUE_0 = "0"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_33 = "33"
    VALUE_34 = "34"
    VALUE_39 = "39"
    VALUE_40 = "40"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_49 = "49"
    VALUE_50 = "50"
    VALUE_51 = "51"
    VALUE_52 = "52"
    VALUE_53 = "53"
    VALUE_54 = "54"
    VALUE_59 = "59"
    VALUE_60 = "60"
    VALUE_61 = "61"
    VALUE_63 = "63"
    VALUE_66 = "66"
    VALUE_70 = "70"
    VALUE_71 = "71"
    VALUE_72 = "72"
    VALUE_73 = "73"
    VALUE_74 = "74"
    VALUE_75 = "75"
    VALUE_76 = "76"
    VALUE_78 = "78"
    VALUE_79 = "79"
    VALUE_80 = "80"
    VALUE_81 = "81"
    VALUE_82 = "82"
    VALUE_83 = "83"
    VALUE_84 = "84"
    VALUE_85 = "85"
    VALUE_86 = "86"
    VALUE_87 = "87"
    VALUE_88 = "88"
    VALUE_89 = "89"
    VALUE_90 = "90"
    VALUE_91 = "91"
    VALUE_92 = "92"
    VALUE_93 = "93"
    VALUE_94 = "94"
    VALUE_95 = "95"
    VALUE_96 = "96"
    VALUE_99 = "99"


class PicklistRr50(Enum):
    """
    :cvar L: Rope Ladder
    :cvar B: Buttonhole
    :cvar U: Unknown
    """
    L = "L"
    B = "B"
    U = "U"


class PicklistRr6(Enum):
    """
    :cvar I44: Erythropoietin Alpha (Eprex)
    :cvar I45: Erythropoietin Beta (Neorecormon)
    :cvar ZI45X: Darboepoietin (Aranesp)
    :cvar ZI45Y: Methoxy Polyethylene Glycol-Epoetin Beta (Mircera)
    :cvar ZI45W: Erythropoietin Delta (Dynepo)
    :cvar ZI45Z: Erythropoietin NOS
    :cvar ZI45V: Erythropoietin Zeta (Retacrit)
    """
    I44 = "i44.."
    I45 = "i45.."
    ZI45X = "Zi45x"
    ZI45Y = "Zi45y"
    ZI45W = "Zi45w"
    ZI45Z = "Zi45z"
    ZI45V = "Zi45v"


class PicklistRr7(Enum):
    """
    :cvar VALUE_1: Haemodialysis
    :cvar VALUE_2: Haemofiltration
    :cvar VALUE_3: Haemodiafiltration
    :cvar VALUE_4: Haemodialysis &gt; 4 days per week / daily
    :cvar VALUE_5: Ultrafiltration
    :cvar VALUE_9: Haemodialysis - type unknown
    :cvar VALUE_10: CAPD Connect
    :cvar VALUE_11: CAPD Disconnect
    :cvar VALUE_12: Cycling PD &gt;= 6 Nights/Week Dry
    :cvar VALUE_13: Cycling PD &lt; 6 Nights/Week Dry
    :cvar VALUE_14: Cycling PD &gt;= 6 Nights/Week Wet (Day Dwell)
    :cvar VALUE_15: Cycling PD &lt; 6 Nights/Week Wet (Day Dwell)
    :cvar VALUE_16: Assisted Cycling PD &gt;= 6 nights/week dry
    :cvar VALUE_17: Assisted Cycling PD &gt;= 6 nights/week wet (day
        dwell)
    :cvar VALUE_19: Peritoneal Dialysis - Type Unknown
    :cvar VALUE_20: Transplant; Cadaver Donor
    :cvar VALUE_21: Transplant; Live Related - Sibling
    :cvar VALUE_22: Transplant; Live Related - Parent or Child
    :cvar VALUE_23: Transplant; Live Related - Other
    :cvar VALUE_24: Transplant; Live Genetically Unrelated
    :cvar VALUE_25: Transplant; Cadaver + Transp Other Organ
    :cvar VALUE_26: Transplant; Live Donor + Transp Other Organ
    :cvar VALUE_27: Transplant; Live donor Non-UK Transplant
    :cvar VALUE_28: Transplant; Non-Heart-beating Donor
    :cvar VALUE_29: Transplant; Type Unknown
    :cvar VALUE_30: Graft Failure
    :cvar VALUE_31: Graft acute rejection episode - biopsy proven
    :cvar VALUE_32: Graft acute rejection episode - no biopsy
    :cvar VALUE_35: Transfer in pre-emptive tranplant (TXT-Only)
    :cvar VALUE_36: Transfer out pre-emptive transplant (TXT-Only)
    :cvar VALUE_37: Transfer to Adult nephrology (TXT-Only)
    :cvar VALUE_38: Patient transferred out (TXT-Only)
    :cvar VALUE_39: Transfer in from another centre, treatment unknown
        (TXT-Only)
    :cvar VALUE_41: Transfer in on: Haemodialysis
    :cvar VALUE_42: Transfer in on: Haemofiltration
    :cvar VALUE_43: Transfer in on: Haemodiafiltration
    :cvar VALUE_45: Transfer in on: Haemodialysis &gt; 4 Days per Week
    :cvar VALUE_49: Transfer in on: Ultrafiltration
    :cvar VALUE_50: Transfer in on: CAPD Connect
    :cvar VALUE_51: Transfer in on: CAPD Disconnect
    :cvar VALUE_52: Transfer in on: Cycling PD &gt;= 6 nights/week with
        without bag
    :cvar VALUE_53: Transfer in on: Cycling PD &lt; 6 nights/week dry
    :cvar VALUE_54: Transfer in on: Cycling PD &gt;= 6 nights/week wet
        (day dwell)
    :cvar VALUE_55: Transfer in on: Cycling PD &lt; 6 nights/week wet
        (day dwell)
    :cvar VALUE_56: Transfer in on: Assisted Cycling PD &gt;= 6
        nights/week dry
    :cvar VALUE_57: Transfer in on: Assisted Cycling PD &gt;= 6
        nights/week wet (day dwell)
    :cvar VALUE_59: Transfer in on: Peritoneal Dialysis - Type Unknown
    :cvar VALUE_60: Transfer in on: Transplant; Cadaver Donor
    :cvar VALUE_61: Transfer in on: Transplant; Live Related - Sibling
    :cvar VALUE_62: Transfer in on: Transplant; Live Related - Parent or
        Child
    :cvar VALUE_63: Transfer in on: Transplant; Live Related - Other
    :cvar VALUE_64: Transfer in on: Transplant; Live Genetically
        Unrelated
    :cvar VALUE_65: Transfer in on: Transplant; Cadaver + Transp Other
        Organ
    :cvar VALUE_66: Transfer in on: Transplant; Live Donor + Transp
        Other Organ
    :cvar VALUE_68: Transfer in on: Transplant; Non-Heart-beating Donor
    :cvar VALUE_69: Transfer in on: Transplant; Type Unknown
    :cvar VALUE_72: Graft Functioning
    :cvar VALUE_76: Nephrectomy - Transplant
    :cvar VALUE_79: Transplant Pancreas (Only)
    :cvar VALUE_80: Acute Renal Failure not dialysed
    :cvar VALUE_81: Acute Haemodialysis - ARF
    :cvar VALUE_82: Acute Haemofiltration - ARF
    :cvar VALUE_83: Acute Peritoneal Dialysis - ARF
    :cvar VALUE_84: ARF - Recovered
    :cvar VALUE_85: ARF - Stopped Dialysis (without recovery of
        function)
    :cvar VALUE_86: ARF - Transferred Out
    :cvar VALUE_90: Patient - Renal Function Recovered
    :cvar VALUE_91: Patient - Treatment Stopped (Without Recovery of
        Function)
    :cvar VALUE_92: Conservative Management - Treatment stopped without
        recovery
    :cvar VALUE_93: Conservative Management - Mutual decision not to
        offer RRT
    :cvar VALUE_94: Conservative Management - Clinical decision not to
        offer RRT
    :cvar VALUE_95: Patient - Lost to follow-up
    """
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"
    VALUE_5 = "5"
    VALUE_9 = "9"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_17 = "17"
    VALUE_19 = "19"
    VALUE_20 = "20"
    VALUE_21 = "21"
    VALUE_22 = "22"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_25 = "25"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_30 = "30"
    VALUE_31 = "31"
    VALUE_32 = "32"
    VALUE_35 = "35"
    VALUE_36 = "36"
    VALUE_37 = "37"
    VALUE_38 = "38"
    VALUE_39 = "39"
    VALUE_41 = "41"
    VALUE_42 = "42"
    VALUE_43 = "43"
    VALUE_45 = "45"
    VALUE_49 = "49"
    VALUE_50 = "50"
    VALUE_51 = "51"
    VALUE_52 = "52"
    VALUE_53 = "53"
    VALUE_54 = "54"
    VALUE_55 = "55"
    VALUE_56 = "56"
    VALUE_57 = "57"
    VALUE_59 = "59"
    VALUE_60 = "60"
    VALUE_61 = "61"
    VALUE_62 = "62"
    VALUE_63 = "63"
    VALUE_64 = "64"
    VALUE_65 = "65"
    VALUE_66 = "66"
    VALUE_68 = "68"
    VALUE_69 = "69"
    VALUE_72 = "72"
    VALUE_76 = "76"
    VALUE_79 = "79"
    VALUE_80 = "80"
    VALUE_81 = "81"
    VALUE_82 = "82"
    VALUE_83 = "83"
    VALUE_84 = "84"
    VALUE_85 = "85"
    VALUE_86 = "86"
    VALUE_90 = "90"
    VALUE_91 = "91"
    VALUE_92 = "92"
    VALUE_93 = "93"
    VALUE_94 = "94"
    VALUE_95 = "95"


class PicklistRr8(Enum):
    """
    :cvar HOSP: Hospital
    :cvar HOME: Home
    :cvar SATL: Satellite
    """
    HOSP = "HOSP"
    HOME = "HOME"
    SATL = "SATL"


class PicklistVa02(Enum):
    """
    :cvar NLN: Non-tunnnelled line
    :cvar TLN: Tunnnelled line
    :cvar AVF: Arteriovenous Fistula
    :cvar AVG: Arteriovenous graft
    :cvar VLP: Vein loop
    :cvar PDC: PD Catheter
    :cvar PDT: PD Catheter Temp
    """
    NLN = "NLN"
    TLN = "TLN"
    AVF = "AVF"
    AVG = "AVG"
    VLP = "VLP"
    PDC = "PDC"
    PDT = "PDT"


class PicklistVa03(Enum):
    """
    :cvar R: Right Handed
    :cvar L: Left Handed
    :cvar A: Ambidextrous
    :cvar U: Unknown
    """
    R = "R"
    L = "L"
    A = "A"
    U = "U"


class PicklistVa143(Enum):
    """
    :cvar VALUE_1: Open surgery (direct visualisation)
    :cvar VALUE_2: Laparoscopic
    :cvar VALUE_3: Percutaneous
    :cvar VALUE_4: Peritoneoscopic
    """
    VALUE_1 = "1"
    VALUE_2 = "2"
    VALUE_3 = "3"
    VALUE_4 = "4"


class PicklistVa40(Enum):
    """
    :cvar R: Right
    :cvar L: Left
    :cvar U: Unknown
    """
    R = "R"
    L = "L"
    U = "U"


class PicklistVa41(Enum):
    """
    :cvar SB: Radio-cephalic Snuff Box
    :cvar RC: Radio-cephalic Wrist
    :cvar BC: Brachio-cephalic
    :cvar BB: Brachio-basilic
    :cvar UC: Ulna-cephalic
    :cvar RU: Radio-ulnar
    :cvar PS: Popliteal-long saphenous
    :cvar UF: Forearm NOS
    :cvar UO: Other
    :cvar LJ: Internal Jugular Line
    :cvar LS: Subclavian line
    :cvar LA: Axillary vein line
    :cvar LF: Femoral vein line
    :cvar TB: Brachio-basilic &amp; transposition
    :cvar TS: Popliteal-long saphenous &amp; transposition
    :cvar UT: Thigh NOS
    :cvar UA: Ankle
    :cvar AR: Upper Arm
    """
    SB = "SB"
    RC = "RC"
    BC = "BC"
    BB = "BB"
    UC = "UC"
    RU = "RU"
    PS = "PS"
    UF = "UF"
    UO = "UO"
    LJ = "LJ"
    LS = "LS"
    LA = "LA"
    LF = "LF"
    TB = "TB"
    TS = "TS"
    UT = "UT"
    UA = "UA"
    AR = "AR"


class PicklistVa42(Enum):
    """
    :cvar LA: Local Anaesthetic
    :cvar GA: General Anaesthetic
    :cvar SA: Spinal
    :cvar UK: Unknown
    """
    LA = "LA"
    GA = "GA"
    SA = "SA"
    UK = "UK"


class PicklistVa43(Enum):
    """
    :cvar VALUE_1: Radiological to fistula - Angioplasty
    :cvar VALUE_4: Radiological to fistula - Thrombolysis
    :cvar VALUE_5: Radiological to central veins - Angioplasty
    :cvar VALUE_8: Radiological to central veins - Thrombolysis
    :cvar VALUE_9: Surgical - Surgical correction with jump graft
    :cvar VALUE_10: Surgical - Surgical correction with vein patch
    :cvar VALUE_11: Surgical - Banding of arteriovenous fistula
    :cvar VALUE_12: Surgical - Thrombectomy of fistula/graft
    :cvar VALUE_13: Surgical - Ligation of AVF
    :cvar VALUE_14: Surgical - Evacuation of haematoma
    :cvar VALUE_15: Surgical dilatation of AVF/G
    :cvar VALUE_16: Surgical transposition of established AVF
    :cvar VALUE_18: Surgical - Pseudoaneurysm repair
    :cvar VALUE_19: Surgical - Refashioning of arteriovenous fistula
    :cvar VALUE_23: Surgical - Surgical revision of graft
    :cvar VALUE_24: Surgical - Excision of AV graft
    :cvar VALUE_26: Repositioning central line by endovascular snare
    :cvar VALUE_27: Removal of central line
    :cvar VALUE_28: Repositioning of PD catheter
    :cvar VALUE_29: Removal of PD catheter
    :cvar VALUE_32: Immediate replacement
    :cvar VALUE_33: Additional Surgical Procedure(not above)
    """
    VALUE_1 = "1"
    VALUE_4 = "4"
    VALUE_5 = "5"
    VALUE_8 = "8"
    VALUE_9 = "9"
    VALUE_10 = "10"
    VALUE_11 = "11"
    VALUE_12 = "12"
    VALUE_13 = "13"
    VALUE_14 = "14"
    VALUE_15 = "15"
    VALUE_16 = "16"
    VALUE_18 = "18"
    VALUE_19 = "19"
    VALUE_23 = "23"
    VALUE_24 = "24"
    VALUE_26 = "26"
    VALUE_27 = "27"
    VALUE_28 = "28"
    VALUE_29 = "29"
    VALUE_32 = "32"
    VALUE_33 = "33"


class PicklistVa49(Enum):
    """
    :cvar VALUE_61: Stenosis
    :cvar VALUE_62: Infection
    :cvar VALUE_63: Aneurysm
    :cvar VALUE_65: Rupture
    :cvar VALUE_66: AVF Thrombosis
    :cvar VALUE_67: Steal Syndrome
    :cvar VALUE_68: Heart Failure
    :cvar VALUE_69: Haemorrhage
    :cvar VALUE_70: Infected Exit Site
    :cvar VALUE_71: Septicaemia
    :cvar VALUE_72: Endocarditis
    :cvar VALUE_73: CVC displacement
    :cvar VALUE_74: Venous occlusion
    :cvar VALUE_75: Venous perforation
    :cvar VALUE_76: Pneumothorax
    :cvar VALUE_77: Air embolism
    :cvar VALUE_80: Subcutaneous haematoma
    :cvar VALUE_81: Tunnel infection
    :cvar VALUE_82: Peritonitis
    :cvar VALUE_83: Subcutaneous leak
    :cvar VALUE_84: Peritoneal leak
    :cvar VALUE_85: Peritoneo-pleural leak
    :cvar VALUE_86: Inadequate inflow - Malposition
    :cvar VALUE_87: Inadequate inflow - Fibrin
    :cvar VALUE_88: Inadequate inflow - Omental wrap
    :cvar VALUE_89: Inadequate outflow - Malposition
    :cvar VALUE_90: Inadequate outflow - Fibrin
    :cvar VALUE_91: Inadequate outflow - Omental wrap
    :cvar VALUE_92: Hernia
    :cvar VALUE_93: Catheter fell out
    :cvar VALUE_94: Externalisation of the cuff
    :cvar VALUE_95: EPS encapsulating peritoneal sclerosis
    :cvar VALUE_96: Bowel Perforation
    :cvar VALUE_97: PD catheter exit site infection
    :cvar VALUE_98: Elective removal post transplant
    :cvar VALUE_99: Elective removal with other modality change
    """
    VALUE_61 = "61"
    VALUE_62 = "62"
    VALUE_63 = "63"
    VALUE_65 = "65"
    VALUE_66 = "66"
    VALUE_67 = "67"
    VALUE_68 = "68"
    VALUE_69 = "69"
    VALUE_70 = "70"
    VALUE_71 = "71"
    VALUE_72 = "72"
    VALUE_73 = "73"
    VALUE_74 = "74"
    VALUE_75 = "75"
    VALUE_76 = "76"
    VALUE_77 = "77"
    VALUE_80 = "80"
    VALUE_81 = "81"
    VALUE_82 = "82"
    VALUE_83 = "83"
    VALUE_84 = "84"
    VALUE_85 = "85"
    VALUE_86 = "86"
    VALUE_87 = "87"
    VALUE_88 = "88"
    VALUE_89 = "89"
    VALUE_90 = "90"
    VALUE_91 = "91"
    VALUE_92 = "92"
    VALUE_93 = "93"
    VALUE_94 = "94"
    VALUE_95 = "95"
    VALUE_96 = "96"
    VALUE_97 = "97"
    VALUE_98 = "98"
    VALUE_99 = "99"


@dataclass
class Cnt:
    """
    :ivar cnt00: Centre Code ID
    :ivar cnt01: Date of Transmission
    :ivar cnt02: Quarter Transmission Applies To
    :ivar cnt03: Year Transmission Applies To
    :ivar idn:
    """
    class Meta:
        name = "CNT"

    cnt00: Optional[str] = field(
        default=None,
        metadata={
            "name": "CNT00",
            "type": "Element",
            "namespace": "",
            "required": True,
            "min_length": 5,
            "max_length": 5,
        }
    )
    cnt01: Optional[str] = field(
        default=None,
        metadata={
            "name": "CNT01",
            "type": "Element",
            "namespace": "",
            "required": True,
            "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
        }
    )
    cnt02: Optional[int] = field(
        default=None,
        metadata={
            "name": "CNT02",
            "type": "Element",
            "namespace": "",
            "required": True,
            "min_inclusive": 1,
            "max_inclusive": 9999,
        }
    )
    cnt03: Optional[int] = field(
        default=None,
        metadata={
            "name": "CNT03",
            "type": "Element",
            "namespace": "",
            "min_inclusive": 1800,
            "max_inclusive": 9999,
        }
    )
    idn: List["Cnt.Idn"] = field(
        default_factory=list,
        metadata={
            "name": "IDN",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        }
    )

    @dataclass
    class Idn:
        """
        :ivar idn00: RR Number
        :ivar idn01: Surname
        :ivar idn02: Forename
        :ivar idn03: Date of Birth
        :ivar idn04: Local Hospital Number
        :ivar idn05: Refused Permission to send identifiable data to
            UKRR
        :ivar idn06: Year of Birth (if IDN05 = Y)
        :ivar idn07: Unique Identifier (if IDN05 = Y)
        :ivar idn08:
        :ivar idn09:
        :ivar pat:
        :ivar erf:
        :ivar com:
        :ivar ser:
        :ivar epo:
        :ivar qua:
        :ivar qbl:
        :ivar pae:
        :ivar ktv:
        :ivar txt:
        :ivar qhd:
        :ivar acl:
        :ivar acc:
        :ivar acp:
        :ivar per:
        :ivar tra:
        :ivar imm:
        :ivar txp:
        :ivar qblp:
        :ivar erfp:
        :ivar hdp:
        :ivar med:
        """
        idn00: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN00",
                "type": "Element",
                "namespace": "",
                "max_length": 10,
            }
        )
        idn01: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN01",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        idn02: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN02",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        idn03: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN03",
                "type": "Element",
                "namespace": "",
                "required": True,
                "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
            }
        )
        idn04: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN04",
                "type": "Element",
                "namespace": "",
                "required": True,
                "max_length": 15,
            }
        )
        idn05: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN05",
                "type": "Element",
                "namespace": "",
                "pattern": r"Y|N",
            }
        )
        idn06: Optional[int] = field(
            default=None,
            metadata={
                "name": "IDN06",
                "type": "Element",
                "namespace": "",
                "min_inclusive": 1899,
                "max_inclusive": 3000,
            }
        )
        idn07: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN07",
                "type": "Element",
                "namespace": "",
                "max_length": 20,
            }
        )
        idn08: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN08",
                "type": "Element",
                "namespace": "",
            }
        )
        idn09: Optional[str] = field(
            default=None,
            metadata={
                "name": "IDN09",
                "type": "Element",
                "namespace": "",
            }
        )
        pat: Optional["Cnt.Idn.Pat"] = field(
            default=None,
            metadata={
                "name": "PAT",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        erf: Optional["Cnt.Idn.Erf"] = field(
            default=None,
            metadata={
                "name": "ERF",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        com: Optional["Cnt.Idn.Com"] = field(
            default=None,
            metadata={
                "name": "COM",
                "type": "Element",
                "namespace": "",
            }
        )
        ser: Optional["Cnt.Idn.Ser"] = field(
            default=None,
            metadata={
                "name": "SER",
                "type": "Element",
                "namespace": "",
            }
        )
        epo: List["Cnt.Idn.Epo"] = field(
            default_factory=list,
            metadata={
                "name": "EPO",
                "type": "Element",
                "namespace": "",
            }
        )
        qua: Optional["Cnt.Idn.Qua"] = field(
            default=None,
            metadata={
                "name": "QUA",
                "type": "Element",
                "namespace": "",
                "required": True,
            }
        )
        qbl: List["Cnt.Idn.Qbl"] = field(
            default_factory=list,
            metadata={
                "name": "QBL",
                "type": "Element",
                "namespace": "",
            }
        )
        pae: List["Cnt.Idn.Pae"] = field(
            default_factory=list,
            metadata={
                "name": "PAE",
                "type": "Element",
                "namespace": "",
            }
        )
        ktv: List["Cnt.Idn.Ktv"] = field(
            default_factory=list,
            metadata={
                "name": "KTV",
                "type": "Element",
                "namespace": "",
            }
        )
        txt: List["Cnt.Idn.Txt"] = field(
            default_factory=list,
            metadata={
                "name": "TXT",
                "type": "Element",
                "namespace": "",
            }
        )
        qhd: List["Cnt.Idn.Qhd"] = field(
            default_factory=list,
            metadata={
                "name": "QHD",
                "type": "Element",
                "namespace": "",
            }
        )
        acl: List["Cnt.Idn.Acl"] = field(
            default_factory=list,
            metadata={
                "name": "ACL",
                "type": "Element",
                "namespace": "",
            }
        )
        acc: List["Cnt.Idn.Acc"] = field(
            default_factory=list,
            metadata={
                "name": "ACC",
                "type": "Element",
                "namespace": "",
            }
        )
        acp: List["Cnt.Idn.Acp"] = field(
            default_factory=list,
            metadata={
                "name": "ACP",
                "type": "Element",
                "namespace": "",
            }
        )
        per: Optional["Cnt.Idn.Per"] = field(
            default=None,
            metadata={
                "name": "PER",
                "type": "Element",
                "namespace": "",
            }
        )
        tra: Optional["Cnt.Idn.Tra"] = field(
            default=None,
            metadata={
                "name": "TRA",
                "type": "Element",
                "namespace": "",
            }
        )
        imm: Optional["Cnt.Idn.Imm"] = field(
            default=None,
            metadata={
                "name": "IMM",
                "type": "Element",
                "namespace": "",
            }
        )
        txp: Optional["Cnt.Idn.Txp"] = field(
            default=None,
            metadata={
                "name": "TXP",
                "type": "Element",
                "namespace": "",
            }
        )
        qblp: Optional["Cnt.Idn.Qblp"] = field(
            default=None,
            metadata={
                "name": "QBLP",
                "type": "Element",
                "namespace": "",
            }
        )
        erfp: Optional["Cnt.Idn.Erfp"] = field(
            default=None,
            metadata={
                "name": "ERFP",
                "type": "Element",
                "namespace": "",
            }
        )
        hdp: Optional["Cnt.Idn.Hdp"] = field(
            default=None,
            metadata={
                "name": "HDP",
                "type": "Element",
                "namespace": "",
            }
        )
        med: Optional["Cnt.Idn.Med"] = field(
            default=None,
            metadata={
                "name": "MED",
                "type": "Element",
                "namespace": "",
            }
        )

        @dataclass
        class Pat:
            """
            :ivar pat00: Sex
            :ivar pat01: Hospital Centre Code
            :ivar pat02: Minimal Dataset Flag
            :ivar pat03: ERF Patient Flag
            :ivar pat04: Paediatric Patient Flag
            :ivar pat05: Patient Centre 1Y Flag
            :ivar pat06: BAPN Number (Paediatric)
            :ivar pat10: UKTSSA Number
            :ivar pat11: CHI Number (Scotland)
            :ivar pat12: Super CHI Number (Scotland)
            :ivar pat13: NHS Number
            :ivar pat16: Scottish Registry Number
            :ivar pat18: H&amp;C Number
            :ivar pat19: Address Line 4
            :ivar pat20: Address Line 1
            :ivar pat21: Address Line 2
            :ivar pat22: Address Line 3
            :ivar pat23: Postcode
            :ivar pat24: Marital Status
            :ivar pat25: Ethnic Group Code
            :ivar pat26: Health Authority Code
            :ivar pat27: GP Postcode
            :ivar pat29: Dominant Arm
            :ivar pat30: Adult Height
            :ivar pat31: Height at First Visit (if &lt; 18 at time of
                visit)
            :ivar pat32: Weight at First Visit (if &lt; 18 at time of
                visit)
            :ivar pat33: Date First Seen by Renal Physician
            :ivar pat34: Serum Creatinine when First Seen
            :ivar pat35: Date of renal referral (i.e. date letter
                recieved)
            :ivar pat36: Referral from GP /Hospital Specialist
            :ivar pat37: Referring GP Code
            :ivar pat38:
            :ivar pat40: Date of Death
            :ivar pat41: Main Cause of Death (Read Code)
            :ivar pat42: Main Cause of Death (EDTA Code)
            :ivar pat43: Secondary Cause of Death (EDTA Code)
            :ivar pat44: Cause of Death Text
            :ivar pat51: Transfer to New Centre flag
            :ivar pat52: Transfer Date
            :ivar pat60: GP Address Line 1
            :ivar pat61: GP Address Line 2
            :ivar pat62: GP Address Line 3
            :ivar pat63: GP Address Line 4
            :ivar pat70: Patient Blood Group
            :ivar pat71: Patient Blood Group Rhesus
            :ivar pat72:
            :ivar pat80: Date of 2nd eGFR 90 Days Later (CKD5)
            :ivar pat81: 2nd eGFR 90 Days Later (CKD5)
            :ivar pat82: Date of 1st eGFR (CKD5)
            :ivar pat83: 1st eGFR (CKD5)
            :ivar patkt: Matched UKTSSA Number - RR Internal Use Only
            """
            pat00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"1|2|8",
                }
            )
            pat01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT01",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            pat02: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT02",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"[A-E]",
                }
            )
            pat03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT03",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            pat04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT04",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            pat05: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT05",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            pat06: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT06",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat10: Optional[int] = field(
                default=None,
                metadata={
                    "name": "PAT10",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 1,
                    "max_inclusive": 999999,
                }
            )
            pat11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT11",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 12,
                }
            )
            pat12: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT12",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 15,
                }
            )
            pat13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT13",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat16: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT16",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 10,
                }
            )
            pat18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT18",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 12,
                }
            )
            pat19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT19",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT20",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "max_length": 40,
                }
            )
            pat21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT21",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT22",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat23: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT23",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"([A-PR-UWYZ0-9][A-HK-Y0-9][AEHJKMNPRTUVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)",
                }
            )
            pat24: Optional[PicklistRr2] = field(
                default=None,
                metadata={
                    "name": "PAT24",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat25: Optional[PicklistRr18] = field(
                default=None,
                metadata={
                    "name": "PAT25",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat26: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT26",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat27: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT27",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"([A-PR-UWYZ0-9][A-HK-Y0-9][AEHJKMNPRTUVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)",
                }
            )
            pat29: Optional[PicklistVa03] = field(
                default=None,
                metadata={
                    "name": "PAT29",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat30: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "PAT30",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("100"),
                    "max_inclusive": Decimal("240"),
                    "fraction_digits": 1,
                }
            )
            pat31: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "PAT31",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("20"),
                    "max_inclusive": Decimal("240"),
                }
            )
            pat32: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "PAT32",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            pat33: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT33",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pat34: Optional[int] = field(
                default=None,
                metadata={
                    "name": "PAT34",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            pat35: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT35",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pat36: Optional[PicklistPat36] = field(
                default=None,
                metadata={
                    "name": "PAT36",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat37: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT37",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat38: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT38",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat40: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT40",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pat41: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT41",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat42: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT42",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat43: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT43",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat44: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT44",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 70,
                }
            )
            pat51: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT51",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            pat52: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT52",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pat60: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT60",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat61: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT61",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat62: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT62",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat63: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT63",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 40,
                }
            )
            pat70: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT70",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat71: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT71",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"POS|NEG",
                }
            )
            pat72: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT72",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat80: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT80",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pat81: Optional[int] = field(
                default=None,
                metadata={
                    "name": "PAT81",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pat82: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAT82",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pat83: Optional[int] = field(
                default=None,
                metadata={
                    "name": "PAT83",
                    "type": "Element",
                    "namespace": "",
                }
            )
            patkt: Optional[int] = field(
                default=None,
                metadata={
                    "name": "PATKT",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 1,
                    "max_inclusive": 999999,
                }
            )

        @dataclass
        class Erf:
            """
            :ivar erf00: Date 1st ERF Treatment
            :ivar erf01: Weight at 1st ERF Treatment
            :ivar erf02: Pre dialysis Creatinine at 1st RRT / ERF
                treatment
            :ivar erf03: Primary Disease Code
            :ivar erf04: EDTA Primary Renal Disease Code
            :ivar erf05: 2 Degree Cause of ERF (1)
            :ivar erf06: 2 Degree Cause of ERF (2)
            :ivar erf08: 2 Degree Cause of ERF (3)
            :ivar erf09: Primary Disease Code Text
            :ivar erf10: First ever Renal Replacement modality HD/PD
            :ivar erf12: Access used when first dialysed
            :ivar erf13: Was the patient assessed by a surgeon regarding
                dialysis Access at least 3 months before their first
                dialysis date
            :ivar erf17: Access used 3 months after the first dialysis
            :ivar erf18: The date the patient was First seen by a renal
                physician (Outpatient or Inpatient nephrology).
            :ivar erf20: Angina
            :ivar erf21: Previous MI within last 3 months
            :ivar erf22: Previous MI more than 3 months prior
            :ivar erf23: Previous CAGB or Coronary Angioplasty
            :ivar erf24: Episode of Heart Failure (either Right or Left)
            :ivar erf30: Smoking
            :ivar erf31: Chronic Obstructive Pulmonary Disease
            :ivar erf32: Cerebrovascular disease - Symptomatic
            :ivar erf33: Diabetes - not causing ERF
            :ivar erf34: Malignancy
            :ivar erf35: Liver Disease
            :ivar erf40: Claudication
            :ivar erf41: Ischaemic/Neuropathic Ulcers
            :ivar erf42: Angioplastci, vasciular graft, aneurysm, sten
                (non-coronary)
            :ivar erf43: Amputation for PVD
            :ivar erf50: Antenatal Diagnosis
            :ivar erf51: Antenatal Treatment
            :ivar erf52: Preterm
            :ivar erf53: Cerebal Palsy
            :ivar erf54: Developmental/Educational Handicap
            :ivar erf55: Congenital Heart Disease
            :ivar erf56: Other Majori Congenital Abnormalities
            :ivar erf57: Downs Syndrome
            :ivar erf58: Other chromosomal abnormalities
            :ivar erf59: Other syndromal diagnosis
            :ivar erf60: Neural tube defect
            :ivar erf62: Date of eGFR value triggering CKD patient to be
                submitted to UKRR
            :ivar erf63: eGFR value triggering CKD patient to be
                submitted to UKRR
            :ivar erf64: Creatinine used to calculate eGFR triggering
                patient to be submitted to UKRR
            :ivar erf70: Date of Last Creatinine Prior to the start of
                ERF
            :ivar erf71: Last Creatinine Prior to the start of ERF
            :ivar erf72: Date of Last Haemoglobin Prior to the start of
                ERF
            :ivar erf73: Last Haemoglobin Prior to the start of ERF
            :ivar erf90: Submit Data to UKTSSA
            :ivar erf91: Submit Data to EDTA
            :ivar erfaj: Primary EDTA Disease Code (2014)
            :ivar erf07:
            :ivar erf14:
            :ivar erf16:
            :ivar erf25:
            :ivar erf61:
            """
            erf00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erf01: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "ERF01",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            erf02: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ERF02",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            erf03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF03",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf04: Optional[PicklistRr4] = field(
                default=None,
                metadata={
                    "name": "ERF04",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf05: Optional[PicklistRr4] = field(
                default=None,
                metadata={
                    "name": "ERF05",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf06: Optional[PicklistRr4] = field(
                default=None,
                metadata={
                    "name": "ERF06",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf08: Optional[PicklistRr4] = field(
                default=None,
                metadata={
                    "name": "ERF08",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf09: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF09",
                    "type": "Element",
                    "namespace": "",
                    "max_length": 70,
                }
            )
            erf10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF10",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf12: Optional[PicklistVa02] = field(
                default=None,
                metadata={
                    "name": "ERF12",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF13",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            erf17: Optional[PicklistVa02] = field(
                default=None,
                metadata={
                    "name": "ERF17",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF18",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF20",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF21",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF22",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf23: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF23",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf24: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF24",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf30: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF30",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf31: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF31",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf32: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF32",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf33: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF33",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf34: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF34",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf35: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF35",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf40: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF40",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf41: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF41",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf42: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF42",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf43: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF43",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf50: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF50",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf51: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF51",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf52: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF52",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf53: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF53",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf54: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF54",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf55: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF55",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf56: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF56",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf57: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF57",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf58: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF58",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf59: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF59",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf60: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF60",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            erf62: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF62",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erf63: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "ERF63",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.0"),
                    "max_inclusive": Decimal("30.0"),
                }
            )
            erf64: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ERF64",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            erf70: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF70",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erf71: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ERF71",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            erf72: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF72",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erf73: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "ERF73",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("3.0"),
                    "max_inclusive": Decimal("20.0"),
                }
            )
            erf90: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF90",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            erf91: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF91",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            erfaj: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFAJ",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf07: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF07",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf14: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF14",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erf16: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "ERF16",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erf25: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF25",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erf61: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERF61",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Com:
            """
            :ivar com00: Date of Co-morbid disease
            :ivar com20: Angia
            :ivar com21: Previous M1 within last 3 months
            :ivar com22: Previous M1 more than 3 months ago
            :ivar com23: Previous CAGB or Coronary Angioplasty
            :ivar com24: Episode of hearth failure (R or L)
            :ivar com30: Smoking
            :ivar com31: Chronic Obstructive Pulmonary Disease
            :ivar com32: Cerebrovascular disease - Symptomatic
            :ivar com33: Diabetes - not causing ERF
            :ivar com34: Malignency
            :ivar com35: Liver Disease
            :ivar com40: Claudication
            :ivar com42: Ischaemic / Neuropathic Ulcers
            :ivar com43: Angioplasty, Vascular Graft, Aneurysm, Stent
                (non-Coronary)
            :ivar com44: Amputation for PVD
            :ivar com70: Karnofsky Performance Scale [0-100]
            :ivar com71:
            :ivar com72:
            :ivar com73:
            :ivar com74:
            :ivar com75:
            :ivar com76:
            :ivar com77:
            :ivar com78:
            :ivar com79:
            :ivar com81:
            :ivar com82:
            :ivar com83:
            :ivar com84:
            :ivar com85:
            :ivar com86:
            :ivar com88:
            :ivar com89:
            :ivar com90:
            :ivar com91:
            :ivar com92:
            :ivar com93:
            :ivar com94:
            :ivar com95:
            :ivar com96:
            :ivar com97: Peripheral Vascular Disease
            :ivar com98: Dementia
            :ivar com99: Atrial Fibrillation
            """
            com00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM20",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM21",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM22",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com23: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM23",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com24: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM24",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com30: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM30",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com31: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM31",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com32: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM32",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com33: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM33",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com34: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM34",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com35: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM35",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com40: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM40",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com42: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM42",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com43: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM43",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com44: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM44",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com70: Optional[int] = field(
                default=None,
                metadata={
                    "name": "COM70",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 0,
                    "max_inclusive": 100,
                }
            )
            com71: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM71",
                    "type": "Element",
                    "namespace": "",
                }
            )
            com72: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM72",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com73: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM73",
                    "type": "Element",
                    "namespace": "",
                }
            )
            com74: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM74",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com75: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM75",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com76: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM76",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com77: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM77",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com78: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM78",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com79: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM79",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com81: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM81",
                    "type": "Element",
                    "namespace": "",
                }
            )
            com82: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM82",
                    "type": "Element",
                    "namespace": "",
                }
            )
            com83: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM83",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com84: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM84",
                    "type": "Element",
                    "namespace": "",
                }
            )
            com85: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM85",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com86: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM86",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com88: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM88",
                    "type": "Element",
                    "namespace": "",
                }
            )
            com89: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM89",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com90: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM90",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com91: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM91",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com92: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM92",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com93: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM93",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com94: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM94",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com95: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM95",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com96: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM96",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            com97: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM97",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com98: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM98",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            com99: Optional[str] = field(
                default=None,
                metadata={
                    "name": "COM99",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )

        @dataclass
        class Ser:
            """
            :ivar ser10: HBV Antibody Status
            :ivar ser11: Date of test HBV Surface Antibody
            :ivar ser14: HBV Surface Antigen Status
            :ivar ser15: Date of Test HBV Surface Antigen
            :ivar ser18: HCV Antibody Status
            :ivar ser19: Date of Test HCV Surface Antibody
            :ivar ser22: CMV Antibody Status
            :ivar ser23: Date of Test CMV Antibody
            :ivar ser24: Date of Test CMV PCR Test
            :ivar ser25: CMV PCR Copies/ml
            :ivar ser26: Date CMV Antigenaemia PP65 Test
            :ivar ser27: CMV Antigenaemia PP65 Assay UNKNOWN TYPE
            :ivar ser30: Date HIV Test
            :ivar ser31: HIV Antigen
            """
            ser10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER10",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            ser11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER11",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser14: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER14",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            ser15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER15",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER18",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            ser19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER19",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER22",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            ser23: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER23",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser24: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER24",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser25: Optional[int] = field(
                default=None,
                metadata={
                    "name": "SER25",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 0,
                    "max_inclusive": 99000,
                }
            )
            ser26: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER26",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser27: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER27",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ser30: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER30",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ser31: Optional[str] = field(
                default=None,
                metadata={
                    "name": "SER31",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )

        @dataclass
        class Epo:
            """
            :ivar epo00: Start Date of Period
            :ivar epo01: End Date of Period
            :ivar epo03: Total units transfused in period
            :ivar epo04: Parenteral Iron in Period Returned as Y/N
            :ivar epo11: EPO Drug Name
            :ivar epo12: EPO Dosage Per Week
            :ivar epo13: EPO Administration Route IV/IM/SC
            :ivar epo14: EPO Frequency
            """
            epo00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "EPO00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            epo01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "EPO01",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            epo03: Optional[int] = field(
                default=None,
                metadata={
                    "name": "EPO03",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 0,
                    "max_inclusive": 99,
                }
            )
            epo04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "EPO04",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            epo11: Optional[PicklistRr6] = field(
                default=None,
                metadata={
                    "name": "EPO11",
                    "type": "Element",
                    "namespace": "",
                }
            )
            epo12: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "EPO12",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0"),
                }
            )
            epo13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "EPO13",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"IV|IM|SC",
                }
            )
            epo14: Optional[PicklistEpoFreq] = field(
                default=None,
                metadata={
                    "name": "EPO14",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Qua:
            """
            :ivar qua00: Start Date of Period
            :ivar qua01: End Date of Period
            :ivar qua02: Detailed Treatment Modality Code
            :ivar qua03: Haemo Flag Patient Flag
            :ivar qua04: Treatment Centre Code
            :ivar qua05: Treatment Supervision Code
            :ivar qua06: Transplant Waiting List Status
            :ivar qua07: Sending Hospital Code
            :ivar qua09: Quarterly Verison of Primary / Secondary Centre
                Flag
            :ivar qua10: Creatinine (umol/l)
            :ivar qua11: Urea (mmol/l)
            :ivar qua12: Creatinine (1st month of Quarter) (umol/l)
            :ivar qua13: Creatinine (2nd month of Quarter) (umol/l)
            :ivar qua21: Hb (g/dl)
            :ivar qua22: Ferritin
            :ivar qua23: Albumin
            :ivar qua24: Aluminium
            :ivar qua25: HBA1c
            :ivar qua26: Cholesterol (mmol/l)
            :ivar qua27: iPTH pmol/l (pmol/l = ng/l/9.8)
            :ivar qua28: % Hyrochromic Red Cells %
            :ivar qua29: MCH
            :ivar qua30: Calcium (mmol/l)
            :ivar qua31: Corrected Calcium (mmol/l)
            :ivar qua32: Phosphate (mmol/l)
            :ivar qua33: Bicarbonate (mmol/l)
            :ivar qua34: Sodium (mmol/l)
            :ivar qua35: CRP
            :ivar qua36: LDL cholesterol (mmol/L)
            :ivar qua37: HDL cholesterol (mmol/L)
            :ivar qua38: Triglycerides (mmol/L)
            :ivar qua39: Alkaline Phosphatase IU/L
            :ivar qua40: Systolic BP (mm Hg), pre-dialysis if HD/PD
            :ivar qua41: Diastolic BP (mm Hg), pre-dialysis if HD/PD
            :ivar qua42: Post-Dialysis Weight (Kg)
            :ivar qua44: Post-Dialysis Systolic BP (mm Hg)
            :ivar qua45: Post-Dialysis Diastolic BP (mm Hg)
            :ivar qua50: Urea Reduction Ratio
            :ivar qua51: On EPO
            :ivar qua52: B12
            :ivar qua53: Red cell folate
            :ivar qua54: Transferrin Saturation
            :ivar qua55: Serum Potassium
            :ivar qua56: Serum Urate / Uric Acid
            :ivar qua57: Protein : Creatinine Ratio (mg/mcmol) -
                Transplant Patients Only
            :ivar qua58: Albumin : Creatinine Ratio (mg/mcmol) -
                Transplant Patients Only
            :ivar qua59: Serum Folate (ug/L)
            :ivar qua61: Blood Flow Rate
            :ivar qua63: Dialyser Reuse
            :ivar qua64: Times per Week
            :ivar qua65: Length of time on dialysis (minutes)
            :ivar qua66: Bicarbonate Dialysis
            :ivar qua67: Total weekly fluid vol if on PD
            :ivar qua68: Bag size (litres) if on PD
            :ivar qua80: Statin Drug Use
            :ivar qua81: Ace Inhibitor
            :ivar qua82: Renagel
            :ivar qua83: Lanthanum
            :ivar qua84: Cinacalcet
            :ivar qua85: Calcium Based Binder
            :ivar qua86: Alucaps
            :ivar qua87: Weight Date
            :ivar qua88: Weight
            """
            qua00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qua01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA01",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qua02: Optional[PicklistRr7] = field(
                default=None,
                metadata={
                    "name": "QUA02",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            qua03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA03",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            qua04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA04",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            qua05: Optional[PicklistRr8] = field(
                default=None,
                metadata={
                    "name": "QUA05",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qua06: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA06",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qua07: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA07",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qua09: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA09",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            qua10: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA10",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            qua11: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA11",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1"),
                    "max_inclusive": Decimal("199"),
                }
            )
            qua12: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA12",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            qua13: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA13",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 4000,
                }
            )
            qua21: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA21",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("3.0"),
                    "max_inclusive": Decimal("20.0"),
                }
            )
            qua22: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA22",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1"),
                    "max_inclusive": Decimal("8000"),
                }
            )
            qua23: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA23",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("10"),
                    "max_inclusive": Decimal("60"),
                }
            )
            qua24: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA24",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0"),
                    "max_inclusive": Decimal("180"),
                }
            )
            qua25: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA25",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("3.0"),
                    "max_inclusive": Decimal("25.0"),
                }
            )
            qua26: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA26",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.0"),
                    "max_inclusive": Decimal("22.0"),
                }
            )
            qua27: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA27",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.1"),
                    "max_inclusive": Decimal("500.0"),
                }
            )
            qua28: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA28",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.1"),
                    "max_inclusive": Decimal("20.0"),
                }
            )
            qua29: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA29",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("19.1"),
                    "max_inclusive": Decimal("39.9"),
                }
            )
            qua30: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA30",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.00"),
                    "max_inclusive": Decimal("4.90"),
                }
            )
            qua31: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA31",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.00"),
                    "max_inclusive": Decimal("4.90"),
                }
            )
            qua32: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA32",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.20"),
                    "max_inclusive": Decimal("5.50"),
                }
            )
            qua33: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA33",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("5.0"),
                    "max_inclusive": Decimal("49.0"),
                }
            )
            qua34: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA34",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("90"),
                    "max_inclusive": Decimal("170"),
                }
            )
            qua35: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA35",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0"),
                    "max_inclusive": Decimal("199"),
                }
            )
            qua36: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA36",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.1"),
                    "max_inclusive": Decimal("14.9"),
                }
            )
            qua37: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA37",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.1"),
                    "max_inclusive": Decimal("4.9"),
                }
            )
            qua38: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA38",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.0"),
                    "max_inclusive": Decimal("39.9"),
                }
            )
            qua39: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA39",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 699,
                }
            )
            qua40: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA40",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 60,
                    "max_inclusive": 300,
                }
            )
            qua41: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA41",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 35,
                    "max_inclusive": 200,
                }
            )
            qua42: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA42",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            qua44: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA44",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 60,
                    "max_inclusive": 300,
                }
            )
            qua45: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA45",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 30,
                    "max_inclusive": 200,
                }
            )
            qua50: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA50",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0"),
                    "max_inclusive": Decimal("99"),
                }
            )
            qua51: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA51",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            qua52: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA52",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 999,
                }
            )
            qua53: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA53",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.1"),
                    "max_inclusive": Decimal("9.9"),
                }
            )
            qua54: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA54",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1"),
                    "max_inclusive": Decimal("70"),
                }
            )
            qua55: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA55",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("2.0"),
                    "max_inclusive": Decimal("8.9"),
                }
            )
            qua56: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA56",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.10"),
                    "max_inclusive": Decimal("1.19"),
                }
            )
            qua57: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA57",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qua58: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA58",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qua59: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA59",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.1"),
                    "max_inclusive": Decimal("39.9"),
                }
            )
            qua61: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA61",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qua63: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA63",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            qua64: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QUA64",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 1,
                    "max_inclusive": 7,
                }
            )
            qua65: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA65",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("30"),
                    "max_inclusive": Decimal("450"),
                }
            )
            qua66: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA66",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            qua67: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA67",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0"),
                    "max_inclusive": Decimal("150.0"),
                }
            )
            qua68: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA68",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0.25"),
                    "max_inclusive": Decimal("9.5"),
                }
            )
            qua80: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA80",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua81: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA81",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua82: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA82",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua83: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA83",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua84: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA84",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua85: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA85",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua86: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA86",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qua87: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QUA87",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qua88: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QUA88",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Qbl:
            """
            :ivar qbl00: Start date of Period
            :ivar qbl01: End date of Period
            :ivar qbl02:
            :ivar qbl03:
            :ivar qbl04:
            :ivar qbl05:
            :ivar qbl06:
            :ivar qbl07:
            :ivar qbl08:
            :ivar qbl09:
            :ivar qbla1:
            :ivar qbla2:
            :ivar qbla3:
            :ivar qbla4:
            :ivar qbla5:
            :ivar qbla6:
            :ivar qbla7:
            :ivar qbla8:
            :ivar qbla9:
            :ivar qblaa:
            :ivar qblab:
            :ivar qblac:
            :ivar qblad:
            :ivar qblaj:
            :ivar qblak:
            :ivar qblal: Unit Calculated eGFR
            :ivar qblam:
            :ivar qblb1:
            :ivar qblb2:
            :ivar qblb3:
            :ivar qblb4:
            :ivar qblb5:
            :ivar qblb6:
            :ivar qblb7:
            :ivar qblb8:
            :ivar qblb9:
            :ivar qblba:
            :ivar qblbb:
            :ivar qblbc:
            :ivar qblbe:
            :ivar qblc1:
            :ivar qblc2:
            :ivar qblc3:
            :ivar qblc4:
            :ivar qblc5:
            :ivar qblc6:
            :ivar qblc7:
            :ivar qblc8:
            :ivar qblc9:
            :ivar qbld1:
            :ivar qbld2:
            :ivar qbld3:
            :ivar qbld4:
            :ivar qbld5:
            :ivar qbld6:
            :ivar qbld7:
            :ivar qbld8:
            :ivar qbld9:
            :ivar qblda: HbA1c (mmol/mol)
            :ivar qbldb:
            :ivar qbldc:
            :ivar qbldf:
            :ivar qble1:
            :ivar qble2:
            :ivar qble3:
            :ivar qble4:
            :ivar qble5:
            :ivar qble6:
            :ivar qble7:
            :ivar qble8:
            :ivar qble9:
            :ivar qblea:
            :ivar qbleb:
            :ivar qblf1:
            :ivar qblf2:
            :ivar qblf3:
            :ivar qblf4:
            :ivar qblf5:
            :ivar qblf6:
            :ivar qblf7:
            :ivar qblf8:
            :ivar qblf9:
            :ivar qblfa:
            :ivar qblfb:
            :ivar qblfc:
            :ivar qblfd:
            :ivar qblfe:
            :ivar qblff:
            :ivar qblfg:
            :ivar qblfh:
            :ivar qblfj:
            :ivar qblfk:
            :ivar qblfl:
            :ivar qblfm:
            :ivar qblfn:
            :ivar qblg1: Weight
            :ivar qblg2:
            :ivar qblg3:
            :ivar qblg4:
            :ivar qblg5:
            :ivar qblg6:
            :ivar qblg7:
            :ivar qblg8:
            :ivar qblg9:
            :ivar qblga:
            :ivar qblgb:
            :ivar qblgc:
            :ivar qblgd:
            :ivar qblge:
            :ivar qblgf:
            :ivar qblgg:
            :ivar qblgh:
            :ivar qblh1:
            :ivar qblh2:
            :ivar qblh3:
            :ivar qblh4:
            :ivar qblh5:
            :ivar qblh6:
            :ivar qblh7:
            :ivar qblh8:
            :ivar qblh9:
            :ivar qblha:
            :ivar qblhb:
            :ivar qblhc:
            :ivar qblhd:
            :ivar qblhe:
            :ivar qblhf:
            :ivar qblhg:
            :ivar qblhh:
            :ivar qblhj:
            :ivar qblhk:
            :ivar qblhl:
            :ivar qblhm:
            :ivar qblhr:
            :ivar qblhs:
            :ivar qblht:
            :ivar qblhu:
            :ivar qblhv:
            :ivar qblhx:
            :ivar qblj1:
            :ivar qblj2:
            :ivar qblj3:
            :ivar qblj4:
            :ivar qblj5:
            :ivar qblj6:
            :ivar qblj7:
            :ivar qblj8:
            :ivar qblj9:
            :ivar qblk1:
            :ivar qblk2:
            :ivar qblk3:
            :ivar qblk4:
            :ivar qblk5:
            :ivar qblk6:
            :ivar qblk7:
            :ivar qblk8:
            :ivar qblk9:
            :ivar qblzz:
            """
            qbl00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbl01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL01",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbl02: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL02",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            qbl03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL03",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbl04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL04",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbl05: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL05",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbl06: Optional[PicklistRr21] = field(
                default=None,
                metadata={
                    "name": "QBL06",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbl07: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL07",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbl08: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL08",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbl09: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBL09",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbla1: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLA1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbla2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLA2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbla3: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLA3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbla4: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLA4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbla5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLA5",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbla6: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLA6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbla7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLA7",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbla8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLA8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbla9: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLA9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblaa: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLAA",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblab: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLAB",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblac: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLAC",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblad: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLAD",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblaj: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLAJ",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblak: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLAK",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblal: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLAL",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("0"),
                    "max_inclusive": Decimal("120"),
                }
            )
            qblam: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLAM",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblb1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLB1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblb2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLB2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblb3: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLB3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblb4: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLB4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblb5: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLB5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblb6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLB6",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblb7: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLB7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblb8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLB8",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblb9: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLB9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblba: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLBA",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblbb: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLBB",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblbc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLBC",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblbe: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLBE",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLC1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblc3: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLC3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc4: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC4",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblc5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblc9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLC9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLD1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLD2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbld3: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLD3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld4: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLD4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld5: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLD5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld6: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLD6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLD7",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbld8: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLD8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qbld9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLD9",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblda: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLDA",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 5,
                    "max_inclusive": 299,
                }
            )
            qbldb: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLDB",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbldc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLDC",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbldf: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLDF",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qble1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLE1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qble2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLE2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qble3: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLE3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qble4: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLE4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qble5: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLE5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qble6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLE6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qble7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLE7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qble8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLE8",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qble9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLE9",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblea: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLEA",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qbleb: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLEB",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblf1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLF1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblf2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLF2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblf3: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLF3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblf4: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLF4",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblf5: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLF5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblf6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLF6",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblf7: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLF7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblf8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLF8",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblf9: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLF9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfa: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFA",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblfb: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLFB",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFC",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblfd: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLFD",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfe: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFE",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblff: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLFF",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfg: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFG",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblfh: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLFH",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfj: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFJ",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblfk: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLFK",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfl: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFL",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblfm: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLFM",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblfn: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLFN",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblg1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLG1",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            qblg2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLG2",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblg3: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLG3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblg4: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLG4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblg5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLG5",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblg6: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLG6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblg7: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLG7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblg8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLG8",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblg9: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLG9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblga: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLGA",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblgb: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLGB",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblgc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLGC",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblgd: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLGD",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblge: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLGE",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblgf: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLGF",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblgg: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLGG",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblgh: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLGH",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblh1: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLH1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh2: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLH2",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh3: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLH3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh4: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLH4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLH5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLH6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLH7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLH8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblh9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLH9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblha: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHA",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhb: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHB",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHC",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhd: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHD",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhe: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHE",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhf: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHF",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhg: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHG",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhh: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHH",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhj: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHJ",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhk: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLHK",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhl: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHL",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhm: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHM",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhr: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHR",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhs: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLHS",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblht: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHT",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhu: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHU",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblhv: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLHV",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhx: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLHX",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj1: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLJ1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj2: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLJ2",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj3: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj4: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblj9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLJ9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk1: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK2",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk3: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk4: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblk9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLK9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblzz: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLZZ",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Pae:
            """
            :ivar pae00:
            :ivar pae01:
            :ivar pae02:
            :ivar pae03: Weight
            :ivar pae04:
            """
            pae00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAE00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pae01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAE01",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            pae02: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAE02",
                    "type": "Element",
                    "namespace": "",
                }
            )
            pae03: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "PAE03",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            pae04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PAE04",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Ktv:
            """
            :ivar ktv00:
            :ivar ktv01:
            :ivar ktv10:
            :ivar ktv11:
            :ivar ktv12: Pre-dialysis Weight
            :ivar ktv13: Post-dialysis Weight
            :ivar ktv14:
            :ivar ktv15:
            :ivar ktv16:
            :ivar ktv17:
            :ivar ktv18:
            :ivar ktv19:
            :ivar ktv20:
            :ivar ktv21: Weight in kilos for PD calc
            :ivar ktv22:
            :ivar ktv23:
            :ivar ktv24:
            :ivar ktv25:
            :ivar ktv26:
            :ivar ktv27:
            :ivar ktv28:
            :ivar ktv29:
            :ivar ktv30:
            :ivar ktv31:
            :ivar ktv32:
            :ivar ktv33:
            :ivar ktv34:
            :ivar ktv35:
            :ivar ktv36:
            :ivar ktv37:
            :ivar ktv38:
            :ivar ktv39:
            :ivar ktv40:
            """
            ktv00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ktv01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV01",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            ktv10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV10",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV11",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv12: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "KTV12",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            ktv13: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "KTV13",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            ktv14: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV14",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV15",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv16: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV16",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv17: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV17",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV18",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV19",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV20",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv21: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "KTV21",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            ktv22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV22",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv23: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV23",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv24: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV24",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv25: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV25",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv26: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV26",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv27: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV27",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv28: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV28",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv29: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV29",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv30: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV30",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv31: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV31",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv32: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV32",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv33: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV33",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv34: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV34",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv35: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV35",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv36: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV36",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv37: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV37",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv38: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV38",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv39: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV39",
                    "type": "Element",
                    "namespace": "",
                }
            )
            ktv40: Optional[str] = field(
                default=None,
                metadata={
                    "name": "KTV40",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Txt:
            """
            :ivar txt00:
            :ivar txt01:
            :ivar txt02:
            :ivar txt03:
            :ivar txt04:
            :ivar txt10:
            :ivar txt11:
            :ivar txt12:
            :ivar txt13:
            :ivar txt14:
            :ivar txt15:
            :ivar txt16: Times per week
            :ivar txt17:
            :ivar txt18:
            :ivar txt19:
            :ivar txt20:
            :ivar txt21: Supervision of Haemodialysis
            :ivar txt30:
            :ivar txt31:
            :ivar txt99: Block Counter
            :ivar txt40:
            :ivar txt41:
            """
            txt00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            txt01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT01",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            txt02: Optional[PicklistRr7] = field(
                default=None,
                metadata={
                    "name": "TXT02",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            txt03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT03",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            txt04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT04",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT10",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT11",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt12: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT12",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT13",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt14: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TXT14",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT15",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt16: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TXT16",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 1,
                    "max_inclusive": 7,
                }
            )
            txt17: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT17",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT18",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT19",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT20",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt21: Optional[PicklistRr8] = field(
                default=None,
                metadata={
                    "name": "TXT21",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt30: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TXT30",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt31: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TXT31",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TXT99",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            txt40: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT40",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txt41: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXT41",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Qhd:
            """
            :ivar qhd00: Date of HD/PEX Session
            :ivar qhd01: Pre HD/PEX weight
            :ivar qhd02: Pre HD/PEX Systolic BP
            :ivar qhd03: Pre HD/PEX Diastolic BP
            :ivar qhd11: Post HD/PEX weight
            :ivar qhd12: Post HD/PEX Systolic BP
            :ivar qhd13: Post HD Diastolic BP
            :ivar qhd19: Symptomatic Hypertension
            :ivar qhd20: Vascular Access Used
            :ivar qhd21: Vascular Access Site
            :ivar qhd22: Access in two sites simultaneously
            :ivar qhd30: Blood Flow Rate
            :ivar qhd31: Time Dialysed in Minutes
            :ivar qhd32: Sodium in dialysate
            :ivar qhd33: Needling Method
            :ivar qhd40: Time Session Started
            :ivar qhd41: HD or PEX
            :ivar qhd99: Block Counter
            """
            qhd00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qhd01: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QHD01",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            qhd02: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD02",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 40,
                    "max_inclusive": 299,
                }
            )
            qhd03: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD03",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 199,
                }
            )
            qhd11: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QHD11",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": Decimal("1.5"),
                    "max_inclusive": Decimal("250.0"),
                }
            )
            qhd12: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD12",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 40,
                    "max_inclusive": 299,
                }
            )
            qhd13: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD13",
                    "type": "Element",
                    "namespace": "",
                    "min_inclusive": 20,
                    "max_inclusive": 199,
                }
            )
            qhd19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD19",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qhd20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD20",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD21",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD22",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qhd30: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD30",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd31: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD31",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd32: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD32",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd33: Optional[PicklistRr50] = field(
                default=None,
                metadata={
                    "name": "QHD33",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd40: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD40",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"([01][0-9]|2[0-3])[:-]?[0-5][0-9]",
                }
            )
            qhd41: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QHD41",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qhd99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QHD99",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Acl:
            acl01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL01",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl02: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL02",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl06: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL06",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl07: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL07",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL10",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL11",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl12: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL12",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL13",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl14: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ACL14",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "min_inclusive": 0,
                    "max_inclusive": 999,
                }
            )
            acl15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACL15",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acl99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ACL99",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Acc:
            """
            :ivar acc10: Date of Referral for Access Construction
            :ivar acc11: Date of Access Construction/Insertion
            :ivar acc12: Type of Access
            :ivar acc13: Anatomical Side of Access
            :ivar acc14: Site of Access
            :ivar acc15: Anaesthetic Method
            :ivar acc18:
            :ivar acc19: Date access FIRST used for dialysis (must be
                &gt; ACC11)
            :ivar acc20: Date of access failure (must be &gt; ACC11)
            :ivar acc21: Date of removal (must be &gt; ACC11)
            :ivar acc22: Reason for removal of Access
            :ivar acc23:
            :ivar acc30: PD Catheter Insertion Technique
            :ivar acc31:
            :ivar acc32: Date of Serum Creatinine (ACC31)
            :ivar acc33: Has diabetes (type I or II) at time of PD
                catheter insertion or Vascular Access creation
            :ivar acc34: BMI at time of Access Insertion
            :ivar acc35: Peritonitis episode within 2 weeks of insertion
                Yes/No
            :ivar acc36: Reposition/ Removal/ replacement -  Codelist
                VA43
            :ivar acc40: PD - Reason for removal of PD Catheter (RR29)
            :ivar acc98: Free Text Comments
            :ivar acc99: Block Counter
            """
            acc10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC10",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acc11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC11",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acc12: Optional[PicklistVa02] = field(
                default=None,
                metadata={
                    "name": "ACC12",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            acc13: Optional[PicklistVa40] = field(
                default=None,
                metadata={
                    "name": "ACC13",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            acc14: Optional[PicklistVa41] = field(
                default=None,
                metadata={
                    "name": "ACC14",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            acc15: Optional[PicklistVa42] = field(
                default=None,
                metadata={
                    "name": "ACC15",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC18",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC19",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acc20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC20",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acc21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC21",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acc22: Optional[PicklistVa49] = field(
                default=None,
                metadata={
                    "name": "ACC22",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc23: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC23",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc30: Optional[PicklistVa143] = field(
                default=None,
                metadata={
                    "name": "ACC30",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc31: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC31",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc32: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC32",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acc33: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC33",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            acc34: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "ACC34",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc35: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC35",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            acc36: Optional[PicklistVa43] = field(
                default=None,
                metadata={
                    "name": "ACC36",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc40: Optional[PicklistRr29] = field(
                default=None,
                metadata={
                    "name": "ACC40",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc98: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACC98",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acc99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ACC99",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Acp:
            """
            :ivar acp00: Date of access construction
            :ivar acp01: Type of access tabled
            :ivar acp03: Date the PD Catheter (Tenckhoff) is first used
                for training or treatment
            :ivar acp10: Date of Access
                Surveillance/Complication/Revision
            :ivar acp11:
            :ivar acp12:
            :ivar acp22: Microbiology result - organism 1 responsible
                for peritonitis
            :ivar acp23: PD Peritonitis organism 2
            :ivar acp24: PD Peritonitis organism 3
            :ivar acp32:
            :ivar acp40: Complications on PD
            :ivar acp41: Reason for switching from PD - 1
            :ivar acp42: Reason for switching from PD - 2
            :ivar acp43: Reason for switching from PD - 3
            :ivar acp99: Block Counter
            """
            acp00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACP00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acp01: Optional[PicklistVa02] = field(
                default=None,
                metadata={
                    "name": "ACP01",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACP03",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acp10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACP10",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            acp11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACP11",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp12: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACP12",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp22: Optional[PicklistRr28] = field(
                default=None,
                metadata={
                    "name": "ACP22",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp23: Optional[PicklistRr28] = field(
                default=None,
                metadata={
                    "name": "ACP23",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp24: Optional[PicklistRr28] = field(
                default=None,
                metadata={
                    "name": "ACP24",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp32: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ACP32",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp40: Optional[PicklistRr29] = field(
                default=None,
                metadata={
                    "name": "ACP40",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp41: Optional[PicklistRr29] = field(
                default=None,
                metadata={
                    "name": "ACP41",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp42: Optional[PicklistRr29] = field(
                default=None,
                metadata={
                    "name": "ACP42",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp43: Optional[PicklistRr29] = field(
                default=None,
                metadata={
                    "name": "ACP43",
                    "type": "Element",
                    "namespace": "",
                }
            )
            acp99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "ACP99",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Per:
            """
            :ivar per00: Date Start Treatment
            :ivar per01: Date End Treatment
            :ivar per10:
            :ivar per11:
            :ivar per20:
            :ivar per21: Intra Peritoneal Antibiotics
            :ivar per22: IV Antibiotics
            :ivar per99: Block Counter
            """
            per00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            per01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER01",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            per10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER10",
                    "type": "Element",
                    "namespace": "",
                }
            )
            per11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER11",
                    "type": "Element",
                    "namespace": "",
                }
            )
            per20: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER20",
                    "type": "Element",
                    "namespace": "",
                }
            )
            per21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER21",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            per22: Optional[str] = field(
                default=None,
                metadata={
                    "name": "PER22",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            per99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "PER99",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Tra:
            """
            :ivar tra00:
            :ivar tra10:
            :ivar tra11:
            :ivar tra12:
            :ivar tra13:
            :ivar tra14:
            :ivar tra15:
            :ivar tra16:
            :ivar tra17:
            :ivar tra18:
            :ivar tra19:
            :ivar tra60:
            :ivar tra61: Transplant date
            :ivar tra62: Transplant number - No of Kidney transplants
            :ivar tra63: Failure of transplant
            :ivar tra64: Date of failure
            :ivar tra65: Cause of failure
            :ivar tra66:
            :ivar tra69: Date graft nephrectomy if graft failed
            :ivar tra70:
            :ivar tra71:
            :ivar tra72:
            :ivar tra73:
            :ivar tra74: Transplant abroad - country of Tx if not done
                in UK
            :ivar tra75:
            :ivar tra76: Graft type
            :ivar tra77:
            :ivar tra78:
            :ivar tra79:
            :ivar tra80:
            :ivar tra8_a:
            :ivar tra81:
            :ivar tra82:
            :ivar tra83:
            :ivar tra84:
            :ivar tra85:
            :ivar tra86:
            :ivar tra87:
            :ivar tra88:
            :ivar tra89:
            :ivar tra90:
            :ivar tra91:
            :ivar tra92:
            :ivar tra93: Anticoaguliant
            :ivar tra94: CMV prophylaxis
            :ivar tra95: Pneumocystis prophylaxis
            :ivar tra96:
            :ivar tra97: Other organ transplanted simultaneously 1
            :ivar tra98: Other organ transplanted simultaneously 2
            """
            tra00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            tra10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA10",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            tra11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA11",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            tra12: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA12",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            tra13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA13",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra14: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA14",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA15",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra16: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA16",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra17: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA17",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA18",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra19: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA19",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra60: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA60",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra61: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA61",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            tra62: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA62",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            tra63: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA63",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"Y|N",
                }
            )
            tra64: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA64",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            tra65: Optional[PicklistRr10] = field(
                default=None,
                metadata={
                    "name": "TRA65",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                }
            )
            tra66: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA66",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra69: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA69",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            tra70: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA70",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra71: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA71",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra72: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA72",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            tra73: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA73",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra74: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA74",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra75: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA75",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra76: Optional[PicklistRr24] = field(
                default=None,
                metadata={
                    "name": "TRA76",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra77: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA77",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra78: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA78",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            tra79: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA79",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            tra80: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA80",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra8_a: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA8A",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"1|2",
                }
            )
            tra81: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA81",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            tra82: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA82",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            tra83: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA83",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra84: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA84",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra85: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TRA85",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra86: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA86",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra87: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA87",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra88: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA88",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra89: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA89",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra90: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA90",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra91: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "TRA91",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra92: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA92",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra93: Optional[PicklistRr15] = field(
                default=None,
                metadata={
                    "name": "TRA93",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra94: Optional[PicklistRr16] = field(
                default=None,
                metadata={
                    "name": "TRA94",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra95: Optional[PicklistRr17] = field(
                default=None,
                metadata={
                    "name": "TRA95",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra96: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TRA96",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            tra97: Optional[PicklistRr14] = field(
                default=None,
                metadata={
                    "name": "TRA97",
                    "type": "Element",
                    "namespace": "",
                }
            )
            tra98: Optional[PicklistRr14] = field(
                default=None,
                metadata={
                    "name": "TRA98",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Imm:
            imm00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM00",
                    "type": "Element",
                    "namespace": "",
                    "required": True,
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            imm10: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM10",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm11: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM11",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm12: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM12",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm13: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM13",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm14: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM14",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm15: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM15",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm16: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM16",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm17: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM17",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm18: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM18",
                    "type": "Element",
                    "namespace": "",
                }
            )
            imm21: Optional[str] = field(
                default=None,
                metadata={
                    "name": "IMM21",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Txp:
            """
            :ivar txp00:
            :ivar txp01:
            :ivar txp99: Block Counter
            """
            txp00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXP00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            txp01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "TXP01",
                    "type": "Element",
                    "namespace": "",
                }
            )
            txp99: Optional[int] = field(
                default=None,
                metadata={
                    "name": "TXP99",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Qblp:
            """
            :ivar qblp1: Drainage of transplanted kidney
            :ivar qblp2:
            :ivar qblp3:
            :ivar qblp4:
            :ivar qblp5:
            :ivar qblp6: Mental disability
            :ivar qblp7: Physical disability
            :ivar qblp8: Visual disability
            :ivar qblp9: Auditory disability
            :ivar qblpa:
            :ivar qblpb:
            :ivar qblpc:
            :ivar qblpd:
            :ivar qblpe:
            :ivar qblpf: Myopathy
            :ivar qblpg: Anthropathy
            :ivar qblph:
            :ivar qblpj:
            :ivar qblpk:
            :ivar qblpl:
            :ivar qblpm:
            :ivar qblpn:
            :ivar qblpp:
            :ivar qblpq:
            :ivar qblpr: Date of onset of Puberty
            :ivar qblpt:
            :ivar qblpv:
            :ivar qblpz:
            :ivar qblhn: Varicella
            :ivar qblhp: Date of Varicella test
            """
            qblp1: Optional[PicklistRr27] = field(
                default=None,
                metadata={
                    "name": "QBLP1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLP2",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp3: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLP3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp4: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLP4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLP5",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qblp6: Optional[PicklistRr31] = field(
                default=None,
                metadata={
                    "name": "QBLP6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp7: Optional[PicklistRr31] = field(
                default=None,
                metadata={
                    "name": "QBLP7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp8: Optional[PicklistRr31] = field(
                default=None,
                metadata={
                    "name": "QBLP8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblp9: Optional[PicklistRr31] = field(
                default=None,
                metadata={
                    "name": "QBLP9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpa: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLPA",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpb: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLPB",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpc: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLPC",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpd: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLPD",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpe: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "QBLPE",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpf: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPF",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qblpg: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPG",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"Y|N",
                }
            )
            qblph: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPH",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpj: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPJ",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpk: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPK",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpl: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPL",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpm: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPM",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpn: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPN",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpp: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPP",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpq: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPQ",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpr: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPR",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblpt: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPT",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblpv: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLPV",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            qblpz: Optional[int] = field(
                default=None,
                metadata={
                    "name": "QBLPZ",
                    "type": "Element",
                    "namespace": "",
                }
            )
            qblhn: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHN",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"NEG|POS|UK",
                }
            )
            qblhp: Optional[str] = field(
                default=None,
                metadata={
                    "name": "QBLHP",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )

        @dataclass
        class Erfp:
            """
            :ivar erfp1:
            :ivar erfp2:
            :ivar erfp3:
            :ivar erfp4: Presumed inheritance
            :ivar erfp5:
            :ivar erfp6:
            :ivar erfp7:
            :ivar erfp8:
            :ivar erfp9:
            :ivar erfpa:
            :ivar erfpb:
            :ivar erfpc:
            :ivar erfpd:
            :ivar erfpe:
            :ivar erfpf:
            :ivar erfpg:
            """
            erfp1: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "ERFP1",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp2: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP2",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp3: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP3",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp4: Optional[PicklistRr30] = field(
                default=None,
                metadata={
                    "name": "ERFP4",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp5: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP5",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp6: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP6",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp7: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP7",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp8: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP8",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfp9: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFP9",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfpa: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPA",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfpb: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPB",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfpc: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPC",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfpd: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPD",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfpe: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPE",
                    "type": "Element",
                    "namespace": "",
                }
            )
            erfpf: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPF",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            erfpg: Optional[str] = field(
                default=None,
                metadata={
                    "name": "ERFPG",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Hdp:
            hdp00: Optional[str] = field(
                default=None,
                metadata={
                    "name": "HDP00",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            hdp01: Optional[int] = field(
                default=None,
                metadata={
                    "name": "HDP01",
                    "type": "Element",
                    "namespace": "",
                }
            )
            hdp02: Optional[int] = field(
                default=None,
                metadata={
                    "name": "HDP02",
                    "type": "Element",
                    "namespace": "",
                }
            )
            hdp03: Optional[int] = field(
                default=None,
                metadata={
                    "name": "HDP03",
                    "type": "Element",
                    "namespace": "",
                }
            )
            hdp04: Optional[int] = field(
                default=None,
                metadata={
                    "name": "HDP04",
                    "type": "Element",
                    "namespace": "",
                }
            )

        @dataclass
        class Med:
            """
            :ivar med01:
            :ivar med02:
            :ivar med03: Generic Drug Name
            :ivar med04: Brand Name of Drug
            :ivar med05: Units
            :ivar med06:
            :ivar med07: Route
            :ivar med08:
            :ivar med09:
            """
            med01: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MED01",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            med02: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MED02",
                    "type": "Element",
                    "namespace": "",
                    "pattern": r"(((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((20[0-9][0-9]))|((((0[1-9])|(1\d)|(2[0-8]))/((0[1-9])|(1[0-2])))|((31/((0[13578])|(1[02])))|((29|30)/((0[1,3-9])|(1[0-2])))))/((19[0-9][0-9]))|(29/02/20(([02468][048])|([13579][26])))|(29/02/19(([02468][048])|([13579][26]))))",
                }
            )
            med03: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MED03",
                    "type": "Element",
                    "namespace": "",
                }
            )
            med04: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MED04",
                    "type": "Element",
                    "namespace": "",
                }
            )
            med05: Optional[PicklistRr23] = field(
                default=None,
                metadata={
                    "name": "MED05",
                    "type": "Element",
                    "namespace": "",
                }
            )
            med06: Optional[Decimal] = field(
                default=None,
                metadata={
                    "name": "MED06",
                    "type": "Element",
                    "namespace": "",
                }
            )
            med07: Optional[PicklistRr22] = field(
                default=None,
                metadata={
                    "name": "MED07",
                    "type": "Element",
                    "namespace": "",
                }
            )
            med08: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MED08",
                    "type": "Element",
                    "namespace": "",
                }
            )
            med09: Optional[str] = field(
                default=None,
                metadata={
                    "name": "MED09",
                    "type": "Element",
                    "namespace": "",
                }
            )
