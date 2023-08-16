from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class LanguageCode(Enum):
    """
    :cvar AA: Afar
    :cvar AB: Abkhazian
    :cvar AE: Avestan
    :cvar AF: Afrikaans
    :cvar AK: Akan
    :cvar AM: Amharic
    :cvar AN: Aragonese
    :cvar AR: Arabic
    :cvar AS: Assamese
    :cvar AV: Avaric
    :cvar AY: Aymara
    :cvar AZ: Azerbaijani
    :cvar BA: Bashkir
    :cvar BE: Belarusian
    :cvar BG: Bulgarian
    :cvar BH: Bihari languages
    :cvar BI: Bislama
    :cvar BM: Bambara
    :cvar BN: Bengali
    :cvar BO: Tibetan
    :cvar BR: Breton
    :cvar BS: Bosnian
    :cvar CA: Catalan; Valencian
    :cvar CE: Chechen
    :cvar CH: Chamorro
    :cvar CO: Corsican
    :cvar CR: Cree
    :cvar CS: Czech
    :cvar CU: Church Slavic; Old Slavonic; Church Slavonic; Old
        Bulgarian; Old Church Slavonic
    :cvar CV: Chuvash
    :cvar CY: Welsh
    :cvar DA: Danish
    :cvar DE: German
    :cvar DV: Divehi; Dhivehi; Maldivian
    :cvar DZ: Dzongkha
    :cvar EE: Ewe
    :cvar EL: Greek, Modern (1453-)
    :cvar EN: English
    :cvar EO: Esperanto
    :cvar ES: Spanish; Castilian
    :cvar ET: Estonian
    :cvar EU: Basque
    :cvar FA: Persian
    :cvar FF: Fulah
    :cvar FI: Finnish
    :cvar FJ: Fijian
    :cvar FO: Faroese
    :cvar FR: French
    :cvar FY: Western Frisian
    :cvar GA: Irish
    :cvar GD: Gaelic; Scottish Gaelic
    :cvar GL: Galician
    :cvar GN: Guarani
    :cvar GU: Gujarati
    :cvar GV: Manx
    :cvar HA: Hausa
    :cvar HE: Hebrew
    :cvar HI: Hindi
    :cvar HO: Hiri Motu
    :cvar HR: Croatian
    :cvar HT: Haitian; Haitian Creole
    :cvar HU: Hungarian
    :cvar HY: Armenian
    :cvar HZ: Herero
    :cvar IA: Interlingua (International Auxiliary Language Association)
    :cvar ID: Indonesian
    :cvar IE: Interlingue; Occidental
    :cvar IG: Igbo
    :cvar II: Sichuan Yi; Nuosu
    :cvar IK: Inupiaq
    :cvar IO: Ido
    :cvar IS: Icelandic
    :cvar IT: Italian
    :cvar IU: Inuktitut
    :cvar JA: Japanese
    :cvar JV: Javanese
    :cvar KA: Georgian
    :cvar KG: Kongo
    :cvar KI: Kikuyu; Gikuyu
    :cvar KJ: Kuanyama; Kwanyama
    :cvar KK: Kazakh
    :cvar KL: Kalaallisut; Greenlandic
    :cvar KM: Central Khmer
    :cvar KN: Kannada
    :cvar KO: Korean
    :cvar KR: Kanuri
    :cvar KS: Kashmiri
    :cvar KU: Kurdish
    :cvar KV: Komi
    :cvar KW: Cornish
    :cvar KY: Kirghiz; Kyrgyz
    :cvar LA: Latin
    :cvar LB: Luxembourgish; Letzeburgesch
    :cvar LG: Ganda
    :cvar LI: Limburgan; Limburger; Limburgish
    :cvar LN: Lingala
    :cvar LO: Lao
    :cvar LT: Lithuanian
    :cvar LU: Luba-Katanga
    :cvar LV: Latvian
    :cvar MG: Malagasy
    :cvar MH: Marshallese
    :cvar MI: Maori
    :cvar MK: Macedonian
    :cvar ML: Malayalam
    :cvar MN: Mongolian
    :cvar MR: Marathi
    :cvar MS: Malay
    :cvar MT: Maltese
    :cvar MY: Burmese
    :cvar NA: Nauru
    :cvar NB: Bokmål, Norwegian; Norwegian Bokmål
    :cvar ND: Ndebele, North; North Ndebele
    :cvar NE: Nepali
    :cvar NG: Ndonga
    :cvar NL: Dutch; Flemish
    :cvar NN: Norwegian Nynorsk; Nynorsk, Norwegian
    :cvar NO: Norwegian
    :cvar NR: Ndebele, South; South Ndebele
    :cvar NV: Navajo; Navaho
    :cvar NY: Chichewa; Chewa; Nyanja
    :cvar OC: Occitan (post 1500); Provençal
    :cvar OJ: Ojibwa
    :cvar OM: Oromo
    :cvar OR: Oriya
    :cvar OS: Ossetian; Ossetic
    :cvar PA: Panjabi; Punjabi
    :cvar PI: Pali
    :cvar PL: Polish
    :cvar PS: Pushto; Pashto
    :cvar PT: Portuguese
    :cvar QU: Quechua
    :cvar RM: Romansh
    :cvar RN: Rundi
    :cvar RO: Romanian; Moldavian; Moldovan
    :cvar RU: Russian
    :cvar RW: Kinyarwanda
    :cvar SA: Sanskrit
    :cvar SC: Sardinian
    :cvar SD: Sindhi
    :cvar SE: Northern Sami
    :cvar SG: Sango
    :cvar SI: Sinhala; Sinhalese
    :cvar SK: Slovak
    :cvar SL: Slovenian
    :cvar SM: Samoan
    :cvar SN: Shona
    :cvar SO: Somali
    :cvar SQ: Albanian
    :cvar SR: Serbian
    :cvar SS: Swati
    :cvar ST: Sotho, Southern
    :cvar SU: Sundanese
    :cvar SV: Swedish
    :cvar SW: Swahili
    :cvar TA: Tamil
    :cvar TE: Telugu
    :cvar TG: Tajik
    :cvar TH: Thai
    :cvar TI: Tigrinya
    :cvar TK: Turkmen
    :cvar TL: Tagalog
    :cvar TN: Tswana
    :cvar TO: Tonga (Tonga Islands)
    :cvar TR: Turkish
    :cvar TS: Tsonga
    :cvar TT: Tatar
    :cvar TW: Twi
    :cvar TY: Tahitian
    :cvar UG: Uighur; Uyghur
    :cvar UK: Ukrainian
    :cvar UR: Urdu
    :cvar UZ: Uzbek
    :cvar VE: Venda
    :cvar VI: Vietnamese
    :cvar VO: Volapük
    :cvar WA: Walloon
    :cvar WO: Wolof
    :cvar XH: Xhosa
    :cvar YI: Yiddish
    :cvar YO: Yoruba
    :cvar ZA: Zhuang; Chuang
    :cvar ZH: Chinese
    :cvar ZU: Zulu
    :cvar Q1: Braille - for people who are unable to see
    :cvar Q2: American Sign Language
    :cvar Q3: Australian Sign Language
    :cvar Q4: British Sign Language
    :cvar Q5: Makaton - devised for children and adults with a variety
        of communication and Learning Disabilities
    """
    AA = "aa"
    AB = "ab"
    AE = "ae"
    AF = "af"
    AK = "ak"
    AM = "am"
    AN = "an"
    AR = "ar"
    AS = "as"
    AV = "av"
    AY = "ay"
    AZ = "az"
    BA = "ba"
    BE = "be"
    BG = "bg"
    BH = "bh"
    BI = "bi"
    BM = "bm"
    BN = "bn"
    BO = "bo"
    BR = "br"
    BS = "bs"
    CA = "ca"
    CE = "ce"
    CH = "ch"
    CO = "co"
    CR = "cr"
    CS = "cs"
    CU = "cu"
    CV = "cv"
    CY = "cy"
    DA = "da"
    DE = "de"
    DV = "dv"
    DZ = "dz"
    EE = "ee"
    EL = "el"
    EN = "en"
    EO = "eo"
    ES = "es"
    ET = "et"
    EU = "eu"
    FA = "fa"
    FF = "ff"
    FI = "fi"
    FJ = "fj"
    FO = "fo"
    FR = "fr"
    FY = "fy"
    GA = "ga"
    GD = "gd"
    GL = "gl"
    GN = "gn"
    GU = "gu"
    GV = "gv"
    HA = "ha"
    HE = "he"
    HI = "hi"
    HO = "ho"
    HR = "hr"
    HT = "ht"
    HU = "hu"
    HY = "hy"
    HZ = "hz"
    IA = "ia"
    ID = "id"
    IE = "ie"
    IG = "ig"
    II = "ii"
    IK = "ik"
    IO = "io"
    IS = "is"
    IT = "it"
    IU = "iu"
    JA = "ja"
    JV = "jv"
    KA = "ka"
    KG = "kg"
    KI = "ki"
    KJ = "kj"
    KK = "kk"
    KL = "kl"
    KM = "km"
    KN = "kn"
    KO = "ko"
    KR = "kr"
    KS = "ks"
    KU = "ku"
    KV = "kv"
    KW = "kw"
    KY = "ky"
    LA = "la"
    LB = "lb"
    LG = "lg"
    LI = "li"
    LN = "ln"
    LO = "lo"
    LT = "lt"
    LU = "lu"
    LV = "lv"
    MG = "mg"
    MH = "mh"
    MI = "mi"
    MK = "mk"
    ML = "ml"
    MN = "mn"
    MR = "mr"
    MS = "ms"
    MT = "mt"
    MY = "my"
    NA = "na"
    NB = "nb"
    ND = "nd"
    NE = "ne"
    NG = "ng"
    NL = "nl"
    NN = "nn"
    NO = "no"
    NR = "nr"
    NV = "nv"
    NY = "ny"
    OC = "oc"
    OJ = "oj"
    OM = "om"
    OR = "or"
    OS = "os"
    PA = "pa"
    PI = "pi"
    PL = "pl"
    PS = "ps"
    PT = "pt"
    QU = "qu"
    RM = "rm"
    RN = "rn"
    RO = "ro"
    RU = "ru"
    RW = "rw"
    SA = "sa"
    SC = "sc"
    SD = "sd"
    SE = "se"
    SG = "sg"
    SI = "si"
    SK = "sk"
    SL = "sl"
    SM = "sm"
    SN = "sn"
    SO = "so"
    SQ = "sq"
    SR = "sr"
    SS = "ss"
    ST = "st"
    SU = "su"
    SV = "sv"
    SW = "sw"
    TA = "ta"
    TE = "te"
    TG = "tg"
    TH = "th"
    TI = "ti"
    TK = "tk"
    TL = "tl"
    TN = "tn"
    TO = "to"
    TR = "tr"
    TS = "ts"
    TT = "tt"
    TW = "tw"
    TY = "ty"
    UG = "ug"
    UK = "uk"
    UR = "ur"
    UZ = "uz"
    VE = "ve"
    VI = "vi"
    VO = "vo"
    WA = "wa"
    WO = "wo"
    XH = "xh"
    YI = "yi"
    YO = "yo"
    ZA = "za"
    ZH = "zh"
    ZU = "zu"
    Q1 = "q1"
    Q2 = "q2"
    Q3 = "q3"
    Q4 = "q4"
    Q5 = "q5"


class LanguageCodingStandard(Enum):
    """
    :cvar NHS_DATA_DICTIONARY_LANGUAGE_CODE:
        http://www.datadictionary.nhs.uk/data_dictionary/attributes/l/language_code_de.asp
    """
    NHS_DATA_DICTIONARY_LANGUAGE_CODE = "NHS_DATA_DICTIONARY_LANGUAGE_CODE"


@dataclass
class Language:
    coding_standard: Optional[LanguageCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[LanguageCode] = field(
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
