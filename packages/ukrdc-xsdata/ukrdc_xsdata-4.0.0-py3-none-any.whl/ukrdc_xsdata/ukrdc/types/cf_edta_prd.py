from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class CfEdtaPrdCode(Enum):
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
    :cvar VALUE_1003: Adult Nephrotic Syndrome - No Histology
    :cvar VALUE_1019: Nephrotic Syndrome Of Childhood - Steroid
        Sensitive - No Histology
    :cvar VALUE_1026: Congenital Nephrotic Syndrome (Cns) - No Histology
    :cvar VALUE_1035: Congenital Nephrotic Syndrome (Cns) - Finnish Type
        - No Histology
    :cvar VALUE_1042: Congenital Nephrotic Syndrome (Cns) - Finnish Type
        - Histologically Proven
    :cvar VALUE_1057: Congenital Nephrotic Syndrome (Cns) - Diffuse
        Mesangial Sclerosis
    :cvar VALUE_1061: Congenital Nephrotic Syndrome (Cns) - Focal
        Segmental Glomerulosclerosis (Fsgs)
    :cvar VALUE_1074: Denys-Drash Syndrome
    :cvar VALUE_1088: Congenital Nephrotic Syndrome (Cns) - Congenital
        Infection
    :cvar VALUE_1090: Minimal Change Nephropathy - No Histology
    :cvar VALUE_1100: Minimal Change Nephropathy - Histologically Proven
    :cvar VALUE_1116: Iga Nephropathy - No Histology
    :cvar VALUE_1128: Iga Nephropathy - Histologically Proven
    :cvar VALUE_1137: Familial Iga Nephropathy - No Histology
    :cvar VALUE_1144: Familial Iga Nephropathy - Histologically Proven
    :cvar VALUE_1159: Iga Nephropathy Secondary To Liver Cirrhosis - No
        Histology
    :cvar VALUE_1163: Iga Nephropathy Secondary To Liver Cirrhosis -
        Histologically Proven
    :cvar VALUE_1171: Igm - Associated Nephropathy
    :cvar VALUE_1185: Membranous Nephropathy - Idiopathic
    :cvar VALUE_1192: Membranous Nephropathy - Malignancy Associated
    :cvar VALUE_1205: Membranous Nephropathy - Drug Induced
    :cvar VALUE_1214: Membranous Nephropathy - Infection Associated
    :cvar VALUE_1222: Mesangiocapillary Glomerulonephritis Type 1
    :cvar VALUE_1233: Mesangiocapillary Glomerulonephritis Type 2 (Dense
        Deposit Disease)
    :cvar VALUE_1246: Mesangiocapillary Glomerulonephritis Type 3
    :cvar VALUE_1251: Idiopathic Rapidly Progressive (Crescentic)
        Glomerulonephritis
    :cvar VALUE_1267: Primary Focal Segmental Glomerulosclerosis (Fsgs)
    :cvar VALUE_1279: Familial Focal Segmental Glomerulosclerosis (Fsgs)
        - Autosomal Recessive - No Histology
    :cvar VALUE_1280: Familial Focal Segmental Glomerulosclerosis (Fsgs)
        - Autosomal Recessive - Histologically Proven
    :cvar VALUE_1298: Familial Focal Segmental Glomerulosclerosis (Fsgs)
        - Autosomal Dominant - No Histology
    :cvar VALUE_1308: Familial Focal Segmental Glomerulosclerosis (Fsgs)
        - Autosomal Dominant - Histologically Proven
    :cvar VALUE_1312: Focal Segmental Glomerulosclerosis (Fsgs)
        Secondary To Obesity - No Histology
    :cvar VALUE_1320: Focal Segmental Glomerulosclerosis (Fsgs)
        Secondary To Obesity - Histologically Proven
    :cvar VALUE_1331: Diffuse Endocapillary Glomerulonephritis
    :cvar VALUE_1349: Mesangial Proliferative Glomerulonephritis
    :cvar VALUE_1354: Focal And Segmental Proliferative
        Glomerulonephritis
    :cvar VALUE_1365: Glomerulonephritis - Secondary To Other Systemic
        Disease
    :cvar VALUE_1377: Glomerulonephritis - Histologically Indeterminate
    :cvar VALUE_1383: Systemic Vasculitis - Anca Negative -
        Histologically Proven
    :cvar VALUE_1396: Systemic Vasculitis - Anca Positive - No Histology
    :cvar VALUE_1401: Granulomatosis With Polyangiitis - No Histology
    :cvar VALUE_1417: Granulomatosis With Polyangiitis - Histologically
        Proven
    :cvar VALUE_1429: Microscopic Polyangiitis - Histologically Proven
    :cvar VALUE_1438: Churg-Strauss Syndrome - No Histology
    :cvar VALUE_1440: Churg-Strauss Syndrome - Histologically Proven
    :cvar VALUE_1455: Polyarteritis Nodosa
    :cvar VALUE_1464: Anti-Glomerular Basement Membrane (Gbm) Disease /
        Goodpasture'S Syndrome - No Histology
    :cvar VALUE_1472: Anti-Glomerular Basement Membrane (Gbm) Disease /
        Goodpasture'S Syndrome - Histologically Proven
    :cvar VALUE_1486: Systemic Lupus Erythematosus / Nephritis - No
        Histology
    :cvar VALUE_1493: Systemic Lupus Erythematosus / Nephritis -
        Histologically Proven
    :cvar VALUE_1504: Henoch-Schonlein Purpura / Nephritis - No
        Histology
    :cvar VALUE_1515: Henoch-Schonlein Purpura / Nephritis -
        Histologically Proven
    :cvar VALUE_1527: Renal Scleroderma / Systemic Sclerosis - No
        Histology
    :cvar VALUE_1536: Renal Scleroderma / Systemic Sclerosis -
        Histologically Proven
    :cvar VALUE_1543: Essential Mixed Cryoglobulinaemia - No Histology
    :cvar VALUE_1558: Essential Mixed Cryoglobulinaemia - Histologically
        Proven
    :cvar VALUE_1562: Cryoglobulinaemia Secondary To Hepatitis C - No
        Histology
    :cvar VALUE_1570: Cryoglobulinaemia Secondary To Hepatitis C -
        Histologically Proven
    :cvar VALUE_1589: Cryoglobulinaemia Secondary To Systemic Disease -
        No Histology
    :cvar VALUE_1591: Cryoglobulinaemia Secondary To Systemic Disease -
        Histologically Proven
    :cvar VALUE_1602: Primary Reflux Nephropathy - Sporadic
    :cvar VALUE_1618: Familial Reflux Nephropathy
    :cvar VALUE_1625: Congenital Dysplasia / Hypoplasia
    :cvar VALUE_1639: Multicystic Dysplastic Kidneys
    :cvar VALUE_1641: Dysplasia Due To Fetal Ace-Inhibitor Exposure
    :cvar VALUE_1656: Glomerulocystic Disease
    :cvar VALUE_1660: Congenital Pelvi-Ureteric Junction Obstruction
    :cvar VALUE_1673: Congenital Vesico-Ureteric Junction Obstruction
    :cvar VALUE_1687: Posterior Urethral Valves
    :cvar VALUE_1694: Syndrome Of Agenesis Of Abdominal Muscles - Prune
        Belly Syndrome
    :cvar VALUE_1706: Congenital Neurogenic Bladder
    :cvar VALUE_1710: Bladder Exstrophy
    :cvar VALUE_1723: Megacystis-Megaureter
    :cvar VALUE_1734: Oligomeganephronia
    :cvar VALUE_1747: Renal Papillary Necrosis - Cause Unknown
    :cvar VALUE_1752: Acquired Obstructive Uropathy / Nephropathy
    :cvar VALUE_1768: Acquired Obstructive Nephropathy Due To Neurogenic
        Bladder
    :cvar VALUE_1775: Obstructive Nephropathy Due To Prostatic
        Hypertrophy
    :cvar VALUE_1781: Obstructive Nephropathy Due To Prostate Cancer
    :cvar VALUE_1799: Obstructive Nephropathy Due To Bladder Cancer
    :cvar VALUE_1809: Obstructive Nephropathy Due To Other Malignancies
    :cvar VALUE_1813: Idiopathic Retroperitoneal Fibrosis
    :cvar VALUE_1821: Retroperitoneal Fibrosis Secondary To Malignancies
    :cvar VALUE_1832: Calculus Nephropathy / Urolithiasis
    :cvar VALUE_1845: Calcium Oxalate Urolithiasis
    :cvar VALUE_1850: Enteric Hyperoxaluria
    :cvar VALUE_1866: Magnesium Ammonium Phosphate (Struvite)
        Urolithiasis
    :cvar VALUE_1878: Uric Acid Urolithiasis
    :cvar VALUE_1884: Tubulointerstitial Nephritis - No Histology
    :cvar VALUE_1897: Tubulointerstitial Nephritis - Histologically
        Proven
    :cvar VALUE_1907: Familial Interstitial Nephropathy - No Histology
    :cvar VALUE_1911: Familial Interstitial Nephropathy - Histologically
        Proven
    :cvar VALUE_1924: Tubulointerstitial Nephritis Associated With
        Autoimmune Disease - No Histology
    :cvar VALUE_1930: Tubulointerstitial Nephritis Associated With
        Autoimmune Disease - Histologically Proven
    :cvar VALUE_1948: Tubulointerstitial Nephritis With Uveitis (Tinu) -
        No Histology
    :cvar VALUE_1953: Tubulointerstitial Nephritis With Uveitis (Tinu) -
        Histologically Proven
    :cvar VALUE_1969: Renal Sarcoidosis - No Histology
    :cvar VALUE_1976: Renal Sarcoidosis - Histologically Proven
    :cvar VALUE_1982: Aristolochic Acid Nephropathy (Balkan / Chinese
        Herb / Endemic Nephropathy) - No Histology
    :cvar VALUE_1995: Aristolochic Acid Nephropathy (Balkan / Chinese
        Herb / Endemic Nephropathy) - Histologically Proven
    :cvar VALUE_2005: Drug-Induced Tubulointerstitial Nephritis  - No
        Histology
    :cvar VALUE_2014: Drug-Induced Tubulointerstitial Nephritis -
        Histologically Proven
    :cvar VALUE_2022: Nephropathy Due To Analgesic Drugs - No Histology
    :cvar VALUE_2033: Nephropathy Due To Analgesic Drugs -
        Histologically Proven
    :cvar VALUE_2046: Nephropathy Due To Ciclosporin - No Histology
    :cvar VALUE_2051: Nephropathy Due To Ciclosporin - Histologically
        Proven
    :cvar VALUE_2067: Nephropathy Due To Tacrolimus - No Histology
    :cvar VALUE_2079: Nephropathy Due To Tacrolimus - Histologically
        Proven
    :cvar VALUE_2080: Nephropathy Due To Aminoglycosides - No Histology
    :cvar VALUE_2098: Nephropathy Due To Aminoglycosides -
        Histologically Proven
    :cvar VALUE_2108: Nephropathy Due To Amphotericin - No Histology
    :cvar VALUE_2112: Nephropathy Due To Amphotericin - Histologically
        Proven
    :cvar VALUE_2120: Nephropathy Due To Cisplatin - No Histology
    :cvar VALUE_2131: Nephropathy Due To Cisplatin - Histologically
        Proven
    :cvar VALUE_2149: Nephropathy Due To Lithium - No Histology
    :cvar VALUE_2154: Nephropathy Due To Lithium - Histologically Proven
    :cvar VALUE_2165: Lead Induced Nephropathy - No Histology
    :cvar VALUE_2177: Lead Induced Nephropathy - Histologically Proven
    :cvar VALUE_2183: Acute Urate Nephropathy - No Histology
    :cvar VALUE_2196: Acute Urate Nephropathy - Histologically Proven
    :cvar VALUE_2203: Chronic Urate Nephropathy - Histologically Proven
    :cvar VALUE_2219: Radiation Nephritis
    :cvar VALUE_2226: Renal / Perinephric Abscess
    :cvar VALUE_2235: Renal Tuberculosis
    :cvar VALUE_2242: Leptospirosis
    :cvar VALUE_2257: Hantavirus Nephropathy
    :cvar VALUE_2261: Xanthogranulomatous Pyelonephritis
    :cvar VALUE_2274: Nephropathy Related To Hiv - No Histology
    :cvar VALUE_2288: Nephropathy Related To Hiv - Histologically Proven
    :cvar VALUE_2290: Schistosomiasis
    :cvar VALUE_2300: Other Specific Infection
    :cvar VALUE_2316: Diabetic Nephropathy In Type I Diabetes - No
        Histology
    :cvar VALUE_2328: Diabetic Nephropathy In Type I Diabetes -
        Histologically Proven
    :cvar VALUE_2337: Diabetic Nephropathy In Type Ii Diabetes - No
        Histology
    :cvar VALUE_2344: Diabetic Nephropathy In Type Ii Diabetes -
        Histologically Proven
    :cvar VALUE_2359: Chronic Hypertensive Nephropathy - No Histology
    :cvar VALUE_2363: Chronic Hypertensive Nephropathy - Histologically
        Proven
    :cvar VALUE_2371: Malignant Hypertensive Nephropathy / Accelerated
        Hypertensive Nephropathy - No Histology
    :cvar VALUE_2385: Malignant Hypertensive Nephropathy / Accelerated
        Hypertensive Nephropathy - Histologically Proven
    :cvar VALUE_2392: Ageing Kidney - No Histology
    :cvar VALUE_2407: Ischaemic Nephropathy - No Histology
    :cvar VALUE_2411: Ischaemic Nephropathy / Microvascular Disease -
        Histologically Proven
    :cvar VALUE_2424: Renal Artery Stenosis
    :cvar VALUE_2430: Atheroembolic Renal Disease - No Histology
    :cvar VALUE_2448: Atheroembolic Renal Disease - Histologically
        Proven
    :cvar VALUE_2453: Fibromuscular Dysplasia Of Renal Artery
    :cvar VALUE_2469: Renal Arterial Thrombosis / Occlusion
    :cvar VALUE_2476: Renal Vein Thrombosis
    :cvar VALUE_2482: Cardiorenal Syndrome
    :cvar VALUE_2495: Hepatorenal Syndrome
    :cvar VALUE_2509: Renal Amyloidosis
    :cvar VALUE_2513: Aa Amyloid Secondary To Chronic Inflammation
    :cvar VALUE_2521: Al Amyloid Secondary To Plasma Cell Dyscrasia
    :cvar VALUE_2532: Familial Amyloid Secondary To Protein Mutations -
        No Histology
    :cvar VALUE_2545: Familial Amyloid Secondary To Protein Mutations -
        Histologically Proven
    :cvar VALUE_2550: Familial Aa Amyloid Secondary To Familial
        Mediterranean Fever / Traps (Hibernian Fever) - No Histology
    :cvar VALUE_2566: Familial Aa Amyloid Secondary To Familial
        Mediterranean Fever / Traps (Hibernian Fever) - Histologically
        Proven
    :cvar VALUE_2578: Myeloma Kidney - No Histology
    :cvar VALUE_2584: Myeloma Cast Nephropathy - Histologically Proven
    :cvar VALUE_2597: Light Chain Deposition Disease
    :cvar VALUE_2606: Immunotactoid / Fibrillary Nephropathy
    :cvar VALUE_2610: Haemolytic Uraemic Syndrome (Hus) - Diarrhoea
        Associated
    :cvar VALUE_2623: Atypical Haemolytic Uraemic Syndrome (Hus) -
        Diarrhoea Negative
    :cvar VALUE_2634: Thrombotic Thrombocytopenic Purpura (Ttp)
    :cvar VALUE_2647: Haemolytic Uraemic Syndrome (Hus) Secondary To
        Systemic Disease
    :cvar VALUE_2652: Congenital Haemolytic Uraemic Syndrome (Hus)
    :cvar VALUE_2668: Familial Haemolytic Uraemic Syndrome (Hus)
    :cvar VALUE_2675: Familial Thrombotic Thrombocytopenic Purpura (Ttp)
    :cvar VALUE_2681: Nephropathy Due To Pre-Eclampsia / Eclampsia
    :cvar VALUE_2699: Sickle Cell Nephropathy - No Histology
    :cvar VALUE_2702: Sickle Cell Nephropathy - Histologically Proven
    :cvar VALUE_2718: Autosomal Dominant (Ad) Polycystic Kidney Disease
    :cvar VALUE_2725: Autosomal Dominant (Ad) Polycystic Kidney Disease
        Type I
    :cvar VALUE_2739: Autosomal Dominant (Ad) Polycystic Kidney Disease
        Type Ii
    :cvar VALUE_2741: Autosomal Recessive (Ar) Polycystic Kidney Disease
    :cvar VALUE_2756: Alport Syndrome - No Histology
    :cvar VALUE_2760: Alport Syndrome - Histologically Proven
    :cvar VALUE_2773: Benign Familial Haematuria
    :cvar VALUE_2787: Thin Basement Membrane Disease
    :cvar VALUE_2794: Cystic Kidney Disease
    :cvar VALUE_2804: Medullary Cystic Kidney Disease Type I
    :cvar VALUE_2815: Medullary Cystic Kidney Disease Type Ii
    :cvar VALUE_2827: Uromodulin-Associated Nephropathy (Familial
        Juvenile Hyperuricaemic Nephropathy)
    :cvar VALUE_2836: Nephronophthisis
    :cvar VALUE_2843: Nephronophthisis - Type 1 (Juvenile Type)
    :cvar VALUE_2858: Nephronophthisis - Type 2 (Infantile Type)
    :cvar VALUE_2862: Nephronophthisis - Type 3 (Adolescent Type)
    :cvar VALUE_2870: Nephronophthisis - Type 4 (Juvenile Type)
    :cvar VALUE_2889: Nephronophthisis - Type 5
    :cvar VALUE_2891: Nephronophthisis - Type 6
    :cvar VALUE_2901: Primary Fanconi Syndrome
    :cvar VALUE_2917: Tubular Disorder As Part Of Inherited Metabolic
        Diseases
    :cvar VALUE_2929: Dent Disease
    :cvar VALUE_2938: Lowe Syndrome (Oculocerebrorenal Syndrome)
    :cvar VALUE_2940: Inherited Aminoaciduria
    :cvar VALUE_2955: Cystinuria
    :cvar VALUE_2964: Cystinosis
    :cvar VALUE_2972: Inherited Renal Glycosuria
    :cvar VALUE_2986: Hypophosphataemic Rickets X-Linked (Xl)
    :cvar VALUE_2993: Hypophosphataemic Rickets Autosomal Recessive (Ar)
    :cvar VALUE_3000: Primary Renal Tubular Acidosis (Rta)
    :cvar VALUE_3016: Proximal Renal Tubular Acidosis (Rta) - Type Ii
    :cvar VALUE_3028: Distal Renal Tubular Acidosis (Rta) - Type I
    :cvar VALUE_3037: Distal Renal Tubular Acidosis With Sensorineural
        Deafness - Gene Mutations
    :cvar VALUE_3044: Nephrogenic Diabetes Insipidus
    :cvar VALUE_3059: Lesch Nyhan Syndrome - Hypoxanthine Guanine
        Phosphoribosyl Transferase Deficiency
    :cvar VALUE_3063: Phosphoribosyl Pyrophosphate Synthetase (Prpps)
        Superactivity
    :cvar VALUE_3071: Alagille Syndrome
    :cvar VALUE_3085: Bartter Syndrome
    :cvar VALUE_3092: Gitelman Syndrome
    :cvar VALUE_3102: Liddle Syndrome
    :cvar VALUE_3118: Apparent Mineralocorticoid Excess
    :cvar VALUE_3125: Glucocorticoid Suppressible Hyperaldosteronism
    :cvar VALUE_3139: Inherited / Genetic Diabetes Mellitus Type Ii
    :cvar VALUE_3141: Pseudohypoaldosteronism Type 1
    :cvar VALUE_3156: Pseudohypoaldosteronism Type 2 (Gordon Syndrome)
    :cvar VALUE_3160: Familial Hypocalciuric Hypercalcaemia
    :cvar VALUE_3173: Familial Hypercalciuric Hypocalcaemia
    :cvar VALUE_3187: Familial Hypomagnesaemia
    :cvar VALUE_3194: Primary Hyperoxaluria
    :cvar VALUE_3207: Primary Hyperoxaluria Type I
    :cvar VALUE_3211: Primary Hyperoxaluria Type Ii
    :cvar VALUE_3224: Fabry Disease - No Histology
    :cvar VALUE_3230: Fabry Disease - Histologically Proven
    :cvar VALUE_3248: Xanthinuria
    :cvar VALUE_3253: Nail-Patella Syndrome
    :cvar VALUE_3269: Rubinstein-Taybi Syndrome
    :cvar VALUE_3276: Tuberous Sclerosis
    :cvar VALUE_3282: Von Hippel-Lindau Disease
    :cvar VALUE_3295: Medullary Sponge Kidneys
    :cvar VALUE_3305: Horse-Shoe Kidney
    :cvar VALUE_3314: Frasier Syndrome
    :cvar VALUE_3322: Branchio-Oto-Renal Syndrome
    :cvar VALUE_3333: Williams Syndrome
    :cvar VALUE_3346: Townes-Brocks Syndrome
    :cvar VALUE_3351: Lawrence-Moon-Biedl / Bardet-Biedl Syndrome
    :cvar VALUE_3367: Mitochondrial Cytopathy
    :cvar VALUE_3379: Familial Nephropathy
    :cvar VALUE_3380: Acute Kidney Injury
    :cvar VALUE_3398: Acute Kidney Injury Due To Hypovolaemia
    :cvar VALUE_3403: Acute Kidney Injury Due To Circulatory Failure
    :cvar VALUE_3419: Acute Kidney Injury Due To Sepsis
    :cvar VALUE_3426: Acute Kidney Injury Due To Rhabdomyolysis
    :cvar VALUE_3435: Acute Kidney Injury Due To Nephrotoxicity
    :cvar VALUE_3442: Acute Cortical Necrosis
    :cvar VALUE_3457: Acute Pyelonephritis
    :cvar VALUE_3461: Kidney Tumour
    :cvar VALUE_3474: Renal Cell Carcinoma - Histologically Proven
    :cvar VALUE_3488: Transitional Cell Carcinoma - Histologically
        Proven
    :cvar VALUE_3490: Wilms Tumour - Histologically Proven
    :cvar VALUE_3501: Mesoblastic Nephroma - Histologically Proven
    :cvar VALUE_3517: Single Kidney Identified In Adulthood
    :cvar VALUE_3529: Chronic Kidney Disease (Ckd) / Chronic Renal
        Failure (Crf) Caused By Tumour Nephrectomy
    :cvar VALUE_3538: Chronic Kidney Disease (Ckd) / Chronic Renal
        Failure (Crf) Due To Traumatic Loss Of Kidney
    :cvar VALUE_3540: Chronic Kidney Disease (Ckd) / Chronic Renal
        Failure (Crf) Due To Donor Nephrectomy
    :cvar VALUE_3555: Chronic Kidney Disease (Ckd) / Chronic Renal
        Failure (Crf) - Aetiology Uncertain / Unknown - No Histology
    :cvar VALUE_3564: Chronic Kidney Disease (Ckd) / Chronic Renal
        Failure (Crf) - Aetiology Uncertain / Unknown - Histologically
        Proven
    :cvar VALUE_3572: Haematuria And Proteinuria - No Histology
    :cvar VALUE_3604: Nephrotic Syndrome Of Childhood - Steroid
        Resistant - No Histology
    :cvar VALUE_3615: Nephrotic Syndrome Of Childhood - No Trial Of
        Steroids - No Histology
    :cvar VALUE_3627: Renal Cysts And Diabetes Syndrome
    :cvar VALUE_3636: Chronic Urate Nephropathy - No Histology
    :cvar VALUE_3643: Chronic Renal Failure Due To Systemic Infection
    :cvar VALUE_3658: Renal Coloboma Syndrome
    :cvar VALUE_3662: Hypercalcaemic Nephropathy
    :cvar VALUE_3670: Retroperitoneal Fibrosis Secondary To Peri-
        Aortitis
    :cvar VALUE_3689: Retroperitoneal Fibrosis Secondary To Drugs
    :cvar VALUE_3691: Renal Failure
    :cvar VALUE_3708: Chronic Renal Failure
    :cvar VALUE_3712: Isolated Haematuria - No Histology
    :cvar VALUE_3720: Isolated Proteinuria - No Histology
    :cvar VALUE_3731: Primary Hyperoxaluria Type Iii
    :cvar VALUE_3749: Glomerulonephritis - No Histology
    :cvar VALUE_3847: Systemic vasculitis - ANCA negative - no histology
    :cvar VALUE_3852: Systemic vasculitis - ANCA positive -
        histologically proven
    :cvar VALUE_36171008: Glomerulonephritis (disorder)
    :cvar VALUE_52254009: Nephrotic syndrome (disorder)
    :cvar VALUE_445119005: Steroid sensitive nephrotic syndrome of
        childhood (disorder)
    :cvar VALUE_449820008: Steroid resistant nephrotic syndrome of
        childhood (disorder)
    :cvar VALUE_705065000: Childhood nephrotic syndrome (disorder)
    :cvar VALUE_48796009: Congenital nephrotic syndrome (disorder)
    :cvar VALUE_197601003: Finnish congenital nephrotic syndrome
        (disorder)
    :cvar VALUE_722369003: Congenital nephrotic syndrome due to diffuse
        mesangial sclerosis (disorder)
    :cvar VALUE_236384008: Congenital nephrotic syndrome with focal
        glomerulosclerosis (disorder)
    :cvar VALUE_236385009: Drash syndrome (disorder)
    :cvar VALUE_722118005: Congenital nephrotic syndrome due to
        congenital infection (disorder)
    :cvar VALUE_44785005: Minimal change disease (disorder)
    :cvar VALUE_236407003: Immunoglobulin A nephropathy (disorder)
    :cvar VALUE_445404003: Familial immunoglobulin A nephropathy
        (disorder)
    :cvar VALUE_282364005: Immunoglobulin A nephropathy associated with
        liver disease (disorder)
    :cvar VALUE_236411009: Immunoglobulin M nephropathy (disorder)
    :cvar VALUE_722119002: Idiopathic membranous glomerulonephritis
        (disorder)
    :cvar VALUE_722086002: Membranous glomerulonephritis due to
        malignant neoplastic disease (disorder)
    :cvar VALUE_722120008: Membranous glomerulonephritis caused by drug
        (disorder)
    :cvar VALUE_722168002: Membranous glomerulonephritis co-occurrent
        with infectious disease (disorder)
    :cvar VALUE_75888001: Mesangiocapillary glomerulonephritis, type I
        (disorder)
    :cvar VALUE_59479006: Mesangiocapillary glomerulonephritis, type II
        (disorder)
    :cvar VALUE_236409000: Mesangiocapillary glomerulonephritis type III
        (disorder)
    :cvar VALUE_236398000: Crescentic glomerulonephritis (disorder)
    :cvar VALUE_236403004: Focal segmental glomerulosclerosis (disorder)
    :cvar VALUE_445388002: Autosomal recessive focal segmental
        glomerulosclerosis (disorder)
    :cvar VALUE_444977005: Autosomal dominant focal segmental
        glomerulosclerosis (disorder)
    :cvar VALUE_713887002: FSGS co-occurrent with human immunodefiency
        virus infection (disorder)
    :cvar VALUE_722139003: Focal segmental glomerulosclerosis caused by
        lithium (disorder)
    :cvar VALUE_722147003: Focal segmental glomerulosclerosis due to
        sickle cell disease (disorder)
    :cvar VALUE_3704008: Diffuse endocapillary proliferative
        glomerulonephritis (disorder)
    :cvar VALUE_35546006: Mesangial proliferative glomerulonephritis
        (disorder)
    :cvar VALUE_83866005: Focal AND segmental proliferative
        glomerulonephritis (disorder)
    :cvar VALUE_46956008: Systemic vasculitis (disorder)
    :cvar VALUE_195353004: Wegener's granulomatosis (disorder)
    :cvar VALUE_239928004: Microscopic polyarteritis nodosa (disorder)
    :cvar VALUE_82275008: Allergic granulomatosis angiitis (disorder)
    :cvar VALUE_155441006: Polyarteritis nodosa (disorder)
    :cvar VALUE_236506009: Goodpasture's disease (disorder)
    :cvar VALUE_50581000: Goodpasture's syndrome (disorder)
    :cvar VALUE_68815009: Systemic lupus erythematosus
        glomerulonephritis syndrome (disorder)
    :cvar VALUE_191306005: Henoch-Schönlein purpura (disorder)
    :cvar VALUE_236502006: Renal involvement in scleroderma (disorder)
    :cvar VALUE_239947001: Essential mixed cryoglobulinemia (disorder)
    :cvar VALUE_128971000119101: Cryoglobulinemia due to chronic
        hepatitis C (disorder)
    :cvar VALUE_28807005: Secondary cryoglobulinemia (disorder)
    :cvar VALUE_197764002: Non-obstructive reflux-associated chronic
        pyelonephritis (disorder)
    :cvar VALUE_707208009: Familial non-obstructive reflux-associated
        chronic pyelonephritis (disorder)
    :cvar VALUE_204949001: Renal dysplasia (disorder)
    :cvar VALUE_737562008: Multicystic renal dysplasia (disorder)
    :cvar VALUE_710571007: Renal dysplasia due to fetal exposure to
        angiotensin converting enzyme inhibitor (disorder)
    :cvar VALUE_609572000: Maturity-onset diabetes of the young, type 5
        (disorder)
    :cvar VALUE_253864004: Familial hypoplastic, glomerulocystic kidney
        (disorder)
    :cvar VALUE_373584008: Congenital pelviureteric junction obstruction
        (disorder)
    :cvar VALUE_373585009: Congenital ureterovesical obstruction
        (disorder)
    :cvar VALUE_253900005: Congenital posterior urethral valves
        (disorder)
    :cvar VALUE_5187006: Prune belly syndrome (disorder)
    :cvar VALUE_445387007: Congenital neurogenic urinary bladder
        (finding)
    :cvar VALUE_61758007: Exstrophy of bladder sequence (disorder)
    :cvar VALUE_253904001: Megacystis-megaureter syndrome (disorder)
    :cvar VALUE_18417009: Oligomeganephronic hypoplasia of kidney
        (disorder)
    :cvar VALUE_90241004: Papillary necrosis (disorder)
    :cvar VALUE_723074006: Renal papillary necrosis due to diabetes
        mellitus (disorder)
    :cvar VALUE_722077007: Renal papillary necrosis caused by analgesic
        drug (disorder)
    :cvar VALUE_722085003: Renal papillary necrosis due to sickle cell
        disease (disorder)
    :cvar VALUE_698757009: Nephropathy due to acquired urinary tract
        obstruction (disorder)
    :cvar VALUE_722078002: Obstructive nephropathy due to neurogenic
        bladder (disorder)
    :cvar VALUE_722082000: Obstructive nephropathy due to benign
        prostatic hyperplasia (disorder)
    :cvar VALUE_722081007: Obstructive nephropathy due to carcinoma of
        prostate (disorder)
    :cvar VALUE_722089009: Obstructive nephropathy due to bladder cancer
        (disorder)
    :cvar VALUE_722088001: Obstructive nephropathy due to malignancy
        (disorder)
    :cvar VALUE_197808006: Idiopathic retroperitoneal fibrosis
        (disorder)
    :cvar VALUE_236017004: Malignant retroperitoneal fibrosis (disorder)
    :cvar VALUE_236015007: Drug-induced retroperitoneal fibrosis
        (disorder)
    :cvar VALUE_49120005: Retroperitoneal fibrosis (disorder)
    :cvar VALUE_95566004: Urolithiasis (disorder)
    :cvar VALUE_444717006: Calcium oxalate urolithiasis (disorder)
    :cvar VALUE_37497004: Enteric hyperoxaluria (disorder)
    :cvar VALUE_444690001: Magnesium ammonium phosphate urolithiasis
        (disorder)
    :cvar VALUE_267441009: Uric acid urolithiasis (disorder)
    :cvar VALUE_28689008: Interstitial nephritis (disorder)
    :cvar VALUE_428255004: Tubulointerstitial nephritis (disorder)
    :cvar VALUE_37061001: Granulomatous sarcoid nephropathy (disorder)
    :cvar VALUE_236514003: Toxic nephropathy (disorder)
    :cvar VALUE_439990003: Drug-induced interstitial nephritis
        (disorder)
    :cvar VALUE_59400006: Analgesic nephropathy (disorder)
    :cvar VALUE_704203009: Nephropathy induced by ciclosporin (disorder)
    :cvar VALUE_704205002: Nephropathy induced by tacrolimus (disorder)
    :cvar VALUE_704206001: Nephropathy induced by aminoglycoside
        (disorder)
    :cvar VALUE_704055002: Nephropathy induced by amphotericin
        (disorder)
    :cvar VALUE_53556002: Cis-platinum nephropathy (disorder)
    :cvar VALUE_4390004: Lithium nephropathy (disorder)
    :cvar VALUE_704204003: Nephropathy induced by lead (disorder)
    :cvar VALUE_236496000: Acute urate nephropathy (disorder)
    :cvar VALUE_190829000: Chronic urate nephropathy (disorder)
    :cvar VALUE_33763006: Hypercalcemic nephropathy (disorder)
    :cvar VALUE_7725007: Radiation nephritis (disorder)
    :cvar VALUE_3321001: Renal abscess (disorder)
    :cvar VALUE_80640009: Perirenal abscess (disorder)
    :cvar VALUE_44323002: Tuberculosis of kidney (disorder)
    :cvar VALUE_77377001: Leptospirosis (disorder)
    :cvar VALUE_102455002: Hemorrhagic nephroso-nephritis (disorder)
    :cvar VALUE_38898003: Xanthogranulomatous pyelonephritis (disorder)
    :cvar VALUE_713504001: Disorder of kidney co-occurrent with human
        immunodeficiency virus infection (disorder)
    :cvar VALUE_236706006: Urinary schistosomiasis (disorder)
    :cvar VALUE_40733004: Infectious disease (disorder)
    :cvar VALUE_421893009: Renal disorder associated with type I
        diabetes mellitus (disorder)
    :cvar VALUE_420279001: Renal disorder due to type 2 diabetes
        mellitus (disorder)
    :cvar VALUE_38481006: Hypertensive renal disease (disorder)
    :cvar VALUE_65443008: Malignant hypertensive renal disease
        (disorder)
    :cvar VALUE_445108007: Age related reduction of renal function
        (finding)
    :cvar VALUE_710565001: Nephropathy due to ischemia (disorder)
    :cvar VALUE_302233006: Renal artery stenosis (disorder)
    :cvar VALUE_51677000: Atheroembolism of renal arteries (disorder)
    :cvar VALUE_2900003: Hyperplasia of renal artery (disorder)
    :cvar VALUE_236488005: Renal artery occlusion (disorder)
    :cvar VALUE_15842009: Thrombosis of renal vein (disorder)
    :cvar VALUE_445236007: Cardiorenal syndrome (disorder)
    :cvar VALUE_51292008: Hepatorenal syndrome (disorder)
    :cvar VALUE_48713002: Amyloid nephropathy (disorder)
    :cvar VALUE_274945004: AA amyloidosis (disorder)
    :cvar VALUE_23132008: AL amyloidosis (disorder)
    :cvar VALUE_66451004: Familial visceral amyloidosis, Ostertag type
        (disorder)
    :cvar VALUE_367528006: Amyloid of familial Mediterranean fever
        (disorder)
    :cvar VALUE_32278006: Myeloma kidney (disorder)
    :cvar VALUE_373604002: Light chain deposition disease (disorder)
    :cvar VALUE_73305009: Fibrillary glomerulonephritis (disorder)
    :cvar VALUE_373421000: Diarrhea-associated hemolytic uremic syndrome
        (disorder)
    :cvar VALUE_373422007: Diarrhea-negative hemolytic uremic syndrome
        (disorder)
    :cvar VALUE_78129009: Thrombotic thrombocytopenic purpura (disorder)
    :cvar VALUE_111407006: Hemolytic uremic syndrome (disorder)
    :cvar VALUE_444976001: Congenital hemolytic uremic syndrome
        (disorder)
    :cvar VALUE_722721004: Familial hemolytic uremic syndrome (disorder)
    :cvar VALUE_373420004: Upshaw-Schulman syndrome (disorder)
    :cvar VALUE_736993008: Nephropathy following eclampsia (disorder)
    :cvar VALUE_736992003: Nephropathy following pre-eclampsia
        (disorder)
    :cvar VALUE_13886001: Sickle cell nephropathy (disorder)
    :cvar VALUE_28728008: Polycystic kidney disease, adult type
        (disorder)
    :cvar VALUE_253878003: Adult type polycystic kidney disease type 1
        (disorder)
    :cvar VALUE_253879006: Adult type polycystic kidney disease type 2
        (disorder)
    :cvar VALUE_28770003: Polycystic kidney disease, infantile type
        (disorder)
    :cvar VALUE_399340005: Hereditary nephritis (disorder)
    :cvar VALUE_236421001: Benign familial hematuria (disorder)
    :cvar VALUE_236418003: Thin basement membrane disease (disorder)
    :cvar VALUE_236439005: Cystic disease of kidney (disorder)
    :cvar VALUE_726017001: Mucin 1 related autosomal dominant
        tubulointerstitial kidney disease (disorder)
    :cvar VALUE_723373006: Autosomal dominant medullary cystic kidney
        disease with hyperuricemia (disorder)
    :cvar VALUE_46785007: Familial juvenile gout (disorder)
    :cvar VALUE_204958008: Nephronophthisis (disorder)
    :cvar VALUE_444830001: Juvenile nephronophthisis (disorder)
    :cvar VALUE_444558002: Infantile nephronophthisis (disorder)
    :cvar VALUE_444749006: Adolescent nephronophthisis (disorder)
    :cvar VALUE_446989009: Nephronophthisis type 4 (disorder)
    :cvar VALUE_446991001: Nephronophthisis type 5 (disorder)
    :cvar VALUE_447335007: Nephronophthisis type 6 (disorder)
    :cvar VALUE_236466005: Congenital Fanconi syndrome (disorder)
    :cvar VALUE_197744007: Renal tubulo-interstitial disorders in
        metabolic diseases (disorder)
    :cvar VALUE_444645005: Dent's disease (disorder)
    :cvar VALUE_79385002: Lowe syndrome (disorder)
    :cvar VALUE_698953004: Inherited aminoaciduria (disorder)
    :cvar VALUE_85020001: Cystinuria (disorder)
    :cvar VALUE_190681003: Cystinosis (disorder)
    :cvar VALUE_226309007: Familial renal glucosuria (disorder)
    :cvar VALUE_82236004: Familial x-linked hypophosphatemic vitamin D
        refractory rickets (disorder)
    :cvar VALUE_90505000: Autosomal recessive hypophosphatemic vitamin D
        refractory rickets (disorder)
    :cvar VALUE_1776003: Renal tubular acidosis (disorder)
    :cvar VALUE_24790002: Proximal renal tubular acidosis (disorder)
    :cvar VALUE_236461000: Distal renal tubular acidosis (disorder)
    :cvar VALUE_722468005: Distal renal tubular acidosis co-occurrent
        with sensorineural deafness (disorder)
    :cvar VALUE_111395007: Nephrogenic diabetes insipidus (disorder)
    :cvar VALUE_10406007: Lesch-Nyhan syndrome (disorder)
    :cvar VALUE_35759001: Ribose-phosphate pyrophosphokinase
        overactivity (disorder)
    :cvar VALUE_124274002: Deficiency of adenine phosphoribosyl
        transferase (disorder)
    :cvar VALUE_31742004: Arteriohepatic dysplasia (disorder)
    :cvar VALUE_707742001: Bartter syndrome (disorder)
    :cvar VALUE_707756004: Gitelman syndrome (disorder)
    :cvar VALUE_707747007: Pseudoprimary hyperaldosteronism (disorder)
    :cvar VALUE_237770005: Syndrome of apparent mineralocorticoid excess
        (disorder)
    :cvar VALUE_237743003: Glucocorticoid-suppressible
        hyperaldosteronism (disorder)
    :cvar VALUE_237604008: Maturity onset diabetes of the young, type 2
        (disorder)
    :cvar VALUE_43941006: Pseudohypoaldosteronism, type 1 (disorder)
    :cvar VALUE_15689008: Pseudohypoaldosteronism, type 2 (disorder)
    :cvar VALUE_237885008: Familial hypocalciuric hypercalcemia
        (disorder)
    :cvar VALUE_711152006: Autosomal dominant hypocalcemia (disorder)
    :cvar VALUE_80710001: Primary hypomagnesemia (disorder)
    :cvar VALUE_17901006: Primary hyperoxaluria (disorder)
    :cvar VALUE_65520001: Primary hyperoxaluria, type I (disorder)
    :cvar VALUE_40951006: Primary hyperoxaluria, type II (disorder)
    :cvar VALUE_734990008: Primary hyperoxaluria, type III (disorder)
    :cvar VALUE_16652001: Fabry's disease (disorder)
    :cvar VALUE_190919008: Xanthinuria (disorder)
    :cvar VALUE_236527004: Nail patella-like renal disease (disorder)
    :cvar VALUE_45582004: Rubinstein-Taybi syndrome (disorder)
    :cvar VALUE_7199000: Tuberous sclerosis syndrome (disorder)
    :cvar VALUE_46659004: Von Hippel-Lindau syndrome (disorder)
    :cvar VALUE_236443009: Medullary sponge kidney (disorder)
    :cvar VALUE_41729002: Horseshoe kidney (disorder)
    :cvar VALUE_445431000: Frasier syndrome (disorder)
    :cvar VALUE_446449009: Renal coloboma syndrome (disorder)
    :cvar VALUE_290006: Melnick-Fraser syndrome (disorder)
    :cvar VALUE_63247009: Williams syndrome (disorder)
    :cvar VALUE_24750000: Townes syndrome (disorder)
    :cvar VALUE_232059000: Laurence-Moon syndrome (disorder)
    :cvar VALUE_240096000: Mitochondrial cytopathy (disorder)
    :cvar VALUE_236419006: Progressive hereditary glomerulonephritis
        without deafness (disorder)
    :cvar VALUE_14669001: Acute renal failure syndrome (disorder)
    :cvar VALUE_722096006: Acute kidney injury due to hypovolemia
        (disorder)
    :cvar VALUE_722095005: Acute kidney injury due to circulatory
        failure (disorder)
    :cvar VALUE_722278006: Acute kidney injury due to sepsis (disorder)
    :cvar VALUE_23697004: Crush syndrome (disorder)
    :cvar VALUE_236428007: Nephrotoxic acute renal failure (disorder)
    :cvar VALUE_444794000: Acute necrosis of cortex of kidney (disorder)
    :cvar VALUE_36689008: Acute pyelonephritis (disorder)
    :cvar VALUE_126880001: Neoplasm of kidney (disorder)
    :cvar VALUE_254915003: Clear cell carcinoma of kidney (disorder)
    :cvar VALUE_408642003: Transitional cell carcinoma of kidney
        (disorder)
    :cvar VALUE_302849000: Nephroblastoma (disorder)
    :cvar VALUE_307604008: Mesoblastic nephroma (disorder)
    :cvar VALUE_236513009: Lymphomatous infiltrate of kidney
    :cvar VALUE_249582007: Absent kidney (finding)
    :cvar VALUE_722149000: Chronic kidney disease following excision of
        renal neoplasm (disorder)
    :cvar VALUE_722467000: Chronic kidney disease due to traumatic loss
        of kidney (disorder)
    :cvar VALUE_722098007: Chronic kidney disease following donor
        nephrectomy (disorder)
    :cvar VALUE_90688005: Chronic renal failure syndrome (disorder)
    :cvar VALUE_53298000: Hematuria syndrome (disorder)
    :cvar VALUE_29738008: Proteinuria (finding)
    :cvar VALUE_722150000: Chronic kidney disease due to systemic
        infection (disorder)
    :cvar VALUE_42399005: Renal failure syndrome (disorder)
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
    VALUE_1003 = "1003"
    VALUE_1019 = "1019"
    VALUE_1026 = "1026"
    VALUE_1035 = "1035"
    VALUE_1042 = "1042"
    VALUE_1057 = "1057"
    VALUE_1061 = "1061"
    VALUE_1074 = "1074"
    VALUE_1088 = "1088"
    VALUE_1090 = "1090"
    VALUE_1100 = "1100"
    VALUE_1116 = "1116"
    VALUE_1128 = "1128"
    VALUE_1137 = "1137"
    VALUE_1144 = "1144"
    VALUE_1159 = "1159"
    VALUE_1163 = "1163"
    VALUE_1171 = "1171"
    VALUE_1185 = "1185"
    VALUE_1192 = "1192"
    VALUE_1205 = "1205"
    VALUE_1214 = "1214"
    VALUE_1222 = "1222"
    VALUE_1233 = "1233"
    VALUE_1246 = "1246"
    VALUE_1251 = "1251"
    VALUE_1267 = "1267"
    VALUE_1279 = "1279"
    VALUE_1280 = "1280"
    VALUE_1298 = "1298"
    VALUE_1308 = "1308"
    VALUE_1312 = "1312"
    VALUE_1320 = "1320"
    VALUE_1331 = "1331"
    VALUE_1349 = "1349"
    VALUE_1354 = "1354"
    VALUE_1365 = "1365"
    VALUE_1377 = "1377"
    VALUE_1383 = "1383"
    VALUE_1396 = "1396"
    VALUE_1401 = "1401"
    VALUE_1417 = "1417"
    VALUE_1429 = "1429"
    VALUE_1438 = "1438"
    VALUE_1440 = "1440"
    VALUE_1455 = "1455"
    VALUE_1464 = "1464"
    VALUE_1472 = "1472"
    VALUE_1486 = "1486"
    VALUE_1493 = "1493"
    VALUE_1504 = "1504"
    VALUE_1515 = "1515"
    VALUE_1527 = "1527"
    VALUE_1536 = "1536"
    VALUE_1543 = "1543"
    VALUE_1558 = "1558"
    VALUE_1562 = "1562"
    VALUE_1570 = "1570"
    VALUE_1589 = "1589"
    VALUE_1591 = "1591"
    VALUE_1602 = "1602"
    VALUE_1618 = "1618"
    VALUE_1625 = "1625"
    VALUE_1639 = "1639"
    VALUE_1641 = "1641"
    VALUE_1656 = "1656"
    VALUE_1660 = "1660"
    VALUE_1673 = "1673"
    VALUE_1687 = "1687"
    VALUE_1694 = "1694"
    VALUE_1706 = "1706"
    VALUE_1710 = "1710"
    VALUE_1723 = "1723"
    VALUE_1734 = "1734"
    VALUE_1747 = "1747"
    VALUE_1752 = "1752"
    VALUE_1768 = "1768"
    VALUE_1775 = "1775"
    VALUE_1781 = "1781"
    VALUE_1799 = "1799"
    VALUE_1809 = "1809"
    VALUE_1813 = "1813"
    VALUE_1821 = "1821"
    VALUE_1832 = "1832"
    VALUE_1845 = "1845"
    VALUE_1850 = "1850"
    VALUE_1866 = "1866"
    VALUE_1878 = "1878"
    VALUE_1884 = "1884"
    VALUE_1897 = "1897"
    VALUE_1907 = "1907"
    VALUE_1911 = "1911"
    VALUE_1924 = "1924"
    VALUE_1930 = "1930"
    VALUE_1948 = "1948"
    VALUE_1953 = "1953"
    VALUE_1969 = "1969"
    VALUE_1976 = "1976"
    VALUE_1982 = "1982"
    VALUE_1995 = "1995"
    VALUE_2005 = "2005"
    VALUE_2014 = "2014"
    VALUE_2022 = "2022"
    VALUE_2033 = "2033"
    VALUE_2046 = "2046"
    VALUE_2051 = "2051"
    VALUE_2067 = "2067"
    VALUE_2079 = "2079"
    VALUE_2080 = "2080"
    VALUE_2098 = "2098"
    VALUE_2108 = "2108"
    VALUE_2112 = "2112"
    VALUE_2120 = "2120"
    VALUE_2131 = "2131"
    VALUE_2149 = "2149"
    VALUE_2154 = "2154"
    VALUE_2165 = "2165"
    VALUE_2177 = "2177"
    VALUE_2183 = "2183"
    VALUE_2196 = "2196"
    VALUE_2203 = "2203"
    VALUE_2219 = "2219"
    VALUE_2226 = "2226"
    VALUE_2235 = "2235"
    VALUE_2242 = "2242"
    VALUE_2257 = "2257"
    VALUE_2261 = "2261"
    VALUE_2274 = "2274"
    VALUE_2288 = "2288"
    VALUE_2290 = "2290"
    VALUE_2300 = "2300"
    VALUE_2316 = "2316"
    VALUE_2328 = "2328"
    VALUE_2337 = "2337"
    VALUE_2344 = "2344"
    VALUE_2359 = "2359"
    VALUE_2363 = "2363"
    VALUE_2371 = "2371"
    VALUE_2385 = "2385"
    VALUE_2392 = "2392"
    VALUE_2407 = "2407"
    VALUE_2411 = "2411"
    VALUE_2424 = "2424"
    VALUE_2430 = "2430"
    VALUE_2448 = "2448"
    VALUE_2453 = "2453"
    VALUE_2469 = "2469"
    VALUE_2476 = "2476"
    VALUE_2482 = "2482"
    VALUE_2495 = "2495"
    VALUE_2509 = "2509"
    VALUE_2513 = "2513"
    VALUE_2521 = "2521"
    VALUE_2532 = "2532"
    VALUE_2545 = "2545"
    VALUE_2550 = "2550"
    VALUE_2566 = "2566"
    VALUE_2578 = "2578"
    VALUE_2584 = "2584"
    VALUE_2597 = "2597"
    VALUE_2606 = "2606"
    VALUE_2610 = "2610"
    VALUE_2623 = "2623"
    VALUE_2634 = "2634"
    VALUE_2647 = "2647"
    VALUE_2652 = "2652"
    VALUE_2668 = "2668"
    VALUE_2675 = "2675"
    VALUE_2681 = "2681"
    VALUE_2699 = "2699"
    VALUE_2702 = "2702"
    VALUE_2718 = "2718"
    VALUE_2725 = "2725"
    VALUE_2739 = "2739"
    VALUE_2741 = "2741"
    VALUE_2756 = "2756"
    VALUE_2760 = "2760"
    VALUE_2773 = "2773"
    VALUE_2787 = "2787"
    VALUE_2794 = "2794"
    VALUE_2804 = "2804"
    VALUE_2815 = "2815"
    VALUE_2827 = "2827"
    VALUE_2836 = "2836"
    VALUE_2843 = "2843"
    VALUE_2858 = "2858"
    VALUE_2862 = "2862"
    VALUE_2870 = "2870"
    VALUE_2889 = "2889"
    VALUE_2891 = "2891"
    VALUE_2901 = "2901"
    VALUE_2917 = "2917"
    VALUE_2929 = "2929"
    VALUE_2938 = "2938"
    VALUE_2940 = "2940"
    VALUE_2955 = "2955"
    VALUE_2964 = "2964"
    VALUE_2972 = "2972"
    VALUE_2986 = "2986"
    VALUE_2993 = "2993"
    VALUE_3000 = "3000"
    VALUE_3016 = "3016"
    VALUE_3028 = "3028"
    VALUE_3037 = "3037"
    VALUE_3044 = "3044"
    VALUE_3059 = "3059"
    VALUE_3063 = "3063"
    VALUE_3071 = "3071"
    VALUE_3085 = "3085"
    VALUE_3092 = "3092"
    VALUE_3102 = "3102"
    VALUE_3118 = "3118"
    VALUE_3125 = "3125"
    VALUE_3139 = "3139"
    VALUE_3141 = "3141"
    VALUE_3156 = "3156"
    VALUE_3160 = "3160"
    VALUE_3173 = "3173"
    VALUE_3187 = "3187"
    VALUE_3194 = "3194"
    VALUE_3207 = "3207"
    VALUE_3211 = "3211"
    VALUE_3224 = "3224"
    VALUE_3230 = "3230"
    VALUE_3248 = "3248"
    VALUE_3253 = "3253"
    VALUE_3269 = "3269"
    VALUE_3276 = "3276"
    VALUE_3282 = "3282"
    VALUE_3295 = "3295"
    VALUE_3305 = "3305"
    VALUE_3314 = "3314"
    VALUE_3322 = "3322"
    VALUE_3333 = "3333"
    VALUE_3346 = "3346"
    VALUE_3351 = "3351"
    VALUE_3367 = "3367"
    VALUE_3379 = "3379"
    VALUE_3380 = "3380"
    VALUE_3398 = "3398"
    VALUE_3403 = "3403"
    VALUE_3419 = "3419"
    VALUE_3426 = "3426"
    VALUE_3435 = "3435"
    VALUE_3442 = "3442"
    VALUE_3457 = "3457"
    VALUE_3461 = "3461"
    VALUE_3474 = "3474"
    VALUE_3488 = "3488"
    VALUE_3490 = "3490"
    VALUE_3501 = "3501"
    VALUE_3517 = "3517"
    VALUE_3529 = "3529"
    VALUE_3538 = "3538"
    VALUE_3540 = "3540"
    VALUE_3555 = "3555"
    VALUE_3564 = "3564"
    VALUE_3572 = "3572"
    VALUE_3604 = "3604"
    VALUE_3615 = "3615"
    VALUE_3627 = "3627"
    VALUE_3636 = "3636"
    VALUE_3643 = "3643"
    VALUE_3658 = "3658"
    VALUE_3662 = "3662"
    VALUE_3670 = "3670"
    VALUE_3689 = "3689"
    VALUE_3691 = "3691"
    VALUE_3708 = "3708"
    VALUE_3712 = "3712"
    VALUE_3720 = "3720"
    VALUE_3731 = "3731"
    VALUE_3749 = "3749"
    VALUE_3847 = "3847"
    VALUE_3852 = "3852"
    VALUE_36171008 = "36171008"
    VALUE_52254009 = "52254009"
    VALUE_445119005 = "445119005"
    VALUE_449820008 = "449820008"
    VALUE_705065000 = "705065000"
    VALUE_48796009 = "48796009"
    VALUE_197601003 = "197601003"
    VALUE_722369003 = "722369003"
    VALUE_236384008 = "236384008"
    VALUE_236385009 = "236385009"
    VALUE_722118005 = "722118005"
    VALUE_44785005 = "44785005"
    VALUE_236407003 = "236407003"
    VALUE_445404003 = "445404003"
    VALUE_282364005 = "282364005"
    VALUE_236411009 = "236411009"
    VALUE_722119002 = "722119002"
    VALUE_722086002 = "722086002"
    VALUE_722120008 = "722120008"
    VALUE_722168002 = "722168002"
    VALUE_75888001 = "75888001"
    VALUE_59479006 = "59479006"
    VALUE_236409000 = "236409000"
    VALUE_236398000 = "236398000"
    VALUE_236403004 = "236403004"
    VALUE_445388002 = "445388002"
    VALUE_444977005 = "444977005"
    VALUE_713887002 = "713887002"
    VALUE_722139003 = "722139003"
    VALUE_722147003 = "722147003"
    VALUE_3704008 = "3704008"
    VALUE_35546006 = "35546006"
    VALUE_83866005 = "83866005"
    VALUE_46956008 = "46956008"
    VALUE_195353004 = "195353004"
    VALUE_239928004 = "239928004"
    VALUE_82275008 = "82275008"
    VALUE_155441006 = "155441006"
    VALUE_236506009 = "236506009"
    VALUE_50581000 = "50581000"
    VALUE_68815009 = "68815009"
    VALUE_191306005 = "191306005"
    VALUE_236502006 = "236502006"
    VALUE_239947001 = "239947001"
    VALUE_128971000119101 = "128971000119101"
    VALUE_28807005 = "28807005"
    VALUE_197764002 = "197764002"
    VALUE_707208009 = "707208009"
    VALUE_204949001 = "204949001"
    VALUE_737562008 = "737562008"
    VALUE_710571007 = "710571007"
    VALUE_609572000 = "609572000"
    VALUE_253864004 = "253864004"
    VALUE_373584008 = "373584008"
    VALUE_373585009 = "373585009"
    VALUE_253900005 = "253900005"
    VALUE_5187006 = "5187006"
    VALUE_445387007 = "445387007"
    VALUE_61758007 = "61758007"
    VALUE_253904001 = "253904001"
    VALUE_18417009 = "18417009"
    VALUE_90241004 = "90241004"
    VALUE_723074006 = "723074006"
    VALUE_722077007 = "722077007"
    VALUE_722085003 = "722085003"
    VALUE_698757009 = "698757009"
    VALUE_722078002 = "722078002"
    VALUE_722082000 = "722082000"
    VALUE_722081007 = "722081007"
    VALUE_722089009 = "722089009"
    VALUE_722088001 = "722088001"
    VALUE_197808006 = "197808006"
    VALUE_236017004 = "236017004"
    VALUE_236015007 = "236015007"
    VALUE_49120005 = "49120005"
    VALUE_95566004 = "95566004"
    VALUE_444717006 = "444717006"
    VALUE_37497004 = "37497004"
    VALUE_444690001 = "444690001"
    VALUE_267441009 = "267441009"
    VALUE_28689008 = "28689008"
    VALUE_428255004 = "428255004"
    VALUE_37061001 = "37061001"
    VALUE_236514003 = "236514003"
    VALUE_439990003 = "439990003"
    VALUE_59400006 = "59400006"
    VALUE_704203009 = "704203009"
    VALUE_704205002 = "704205002"
    VALUE_704206001 = "704206001"
    VALUE_704055002 = "704055002"
    VALUE_53556002 = "53556002"
    VALUE_4390004 = "4390004"
    VALUE_704204003 = "704204003"
    VALUE_236496000 = "236496000"
    VALUE_190829000 = "190829000"
    VALUE_33763006 = "33763006"
    VALUE_7725007 = "7725007"
    VALUE_3321001 = "3321001"
    VALUE_80640009 = "80640009"
    VALUE_44323002 = "44323002"
    VALUE_77377001 = "77377001"
    VALUE_102455002 = "102455002"
    VALUE_38898003 = "38898003"
    VALUE_713504001 = "713504001"
    VALUE_236706006 = "236706006"
    VALUE_40733004 = "40733004"
    VALUE_421893009 = "421893009"
    VALUE_420279001 = "420279001"
    VALUE_38481006 = "38481006"
    VALUE_65443008 = "65443008"
    VALUE_445108007 = "445108007"
    VALUE_710565001 = "710565001"
    VALUE_302233006 = "302233006"
    VALUE_51677000 = "51677000"
    VALUE_2900003 = "2900003"
    VALUE_236488005 = "236488005"
    VALUE_15842009 = "15842009"
    VALUE_445236007 = "445236007"
    VALUE_51292008 = "51292008"
    VALUE_48713002 = "48713002"
    VALUE_274945004 = "274945004"
    VALUE_23132008 = "23132008"
    VALUE_66451004 = "66451004"
    VALUE_367528006 = "367528006"
    VALUE_32278006 = "32278006"
    VALUE_373604002 = "373604002"
    VALUE_73305009 = "73305009"
    VALUE_373421000 = "373421000"
    VALUE_373422007 = "373422007"
    VALUE_78129009 = "78129009"
    VALUE_111407006 = "111407006"
    VALUE_444976001 = "444976001"
    VALUE_722721004 = "722721004"
    VALUE_373420004 = "373420004"
    VALUE_736993008 = "736993008"
    VALUE_736992003 = "736992003"
    VALUE_13886001 = "13886001"
    VALUE_28728008 = "28728008"
    VALUE_253878003 = "253878003"
    VALUE_253879006 = "253879006"
    VALUE_28770003 = "28770003"
    VALUE_399340005 = "399340005"
    VALUE_236421001 = "236421001"
    VALUE_236418003 = "236418003"
    VALUE_236439005 = "236439005"
    VALUE_726017001 = "726017001"
    VALUE_723373006 = "723373006"
    VALUE_46785007 = "46785007"
    VALUE_204958008 = "204958008"
    VALUE_444830001 = "444830001"
    VALUE_444558002 = "444558002"
    VALUE_444749006 = "444749006"
    VALUE_446989009 = "446989009"
    VALUE_446991001 = "446991001"
    VALUE_447335007 = "447335007"
    VALUE_236466005 = "236466005"
    VALUE_197744007 = "197744007"
    VALUE_444645005 = "444645005"
    VALUE_79385002 = "79385002"
    VALUE_698953004 = "698953004"
    VALUE_85020001 = "85020001"
    VALUE_190681003 = "190681003"
    VALUE_226309007 = "226309007"
    VALUE_82236004 = "82236004"
    VALUE_90505000 = "90505000"
    VALUE_1776003 = "1776003"
    VALUE_24790002 = "24790002"
    VALUE_236461000 = "236461000"
    VALUE_722468005 = "722468005"
    VALUE_111395007 = "111395007"
    VALUE_10406007 = "10406007"
    VALUE_35759001 = "35759001"
    VALUE_124274002 = "124274002"
    VALUE_31742004 = "31742004"
    VALUE_707742001 = "707742001"
    VALUE_707756004 = "707756004"
    VALUE_707747007 = "707747007"
    VALUE_237770005 = "237770005"
    VALUE_237743003 = "237743003"
    VALUE_237604008 = "237604008"
    VALUE_43941006 = "43941006"
    VALUE_15689008 = "15689008"
    VALUE_237885008 = "237885008"
    VALUE_711152006 = "711152006"
    VALUE_80710001 = "80710001"
    VALUE_17901006 = "17901006"
    VALUE_65520001 = "65520001"
    VALUE_40951006 = "40951006"
    VALUE_734990008 = "734990008"
    VALUE_16652001 = "16652001"
    VALUE_190919008 = "190919008"
    VALUE_236527004 = "236527004"
    VALUE_45582004 = "45582004"
    VALUE_7199000 = "7199000"
    VALUE_46659004 = "46659004"
    VALUE_236443009 = "236443009"
    VALUE_41729002 = "41729002"
    VALUE_445431000 = "445431000"
    VALUE_446449009 = "446449009"
    VALUE_290006 = "290006"
    VALUE_63247009 = "63247009"
    VALUE_24750000 = "24750000"
    VALUE_232059000 = "232059000"
    VALUE_240096000 = "240096000"
    VALUE_236419006 = "236419006"
    VALUE_14669001 = "14669001"
    VALUE_722096006 = "722096006"
    VALUE_722095005 = "722095005"
    VALUE_722278006 = "722278006"
    VALUE_23697004 = "23697004"
    VALUE_236428007 = "236428007"
    VALUE_444794000 = "444794000"
    VALUE_36689008 = "36689008"
    VALUE_126880001 = "126880001"
    VALUE_254915003 = "254915003"
    VALUE_408642003 = "408642003"
    VALUE_302849000 = "302849000"
    VALUE_307604008 = "307604008"
    VALUE_236513009 = "236513009"
    VALUE_249582007 = "249582007"
    VALUE_722149000 = "722149000"
    VALUE_722467000 = "722467000"
    VALUE_722098007 = "722098007"
    VALUE_90688005 = "90688005"
    VALUE_53298000 = "53298000"
    VALUE_29738008 = "29738008"
    VALUE_722150000 = "722150000"
    VALUE_42399005 = "42399005"


class CfEdtaPrdCodingStandard(Enum):
    EDTA = "EDTA"
    EDTA2 = "EDTA2"
    SNOMED = "SNOMED"


@dataclass
class CfEdtaPrd:
    class Meta:
        name = "CF_EDTA_PRD"

    coding_standard: Optional[CfEdtaPrdCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[CfEdtaPrdCode] = field(
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
