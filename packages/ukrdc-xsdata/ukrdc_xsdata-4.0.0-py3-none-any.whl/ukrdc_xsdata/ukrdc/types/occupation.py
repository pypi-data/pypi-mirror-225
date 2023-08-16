from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

__NAMESPACE__ = "http://www.rixg.org.uk/"


class OccupationCode(Enum):
    """
    :cvar VALUE_01: Employed
    :cvar VALUE_02: Unemployed
    :cvar VALUE_03: Students who are undertaking full (at least 16 hours
        per week) or part-time (less than 16 hours per week) education
        or training and who are not working or actively seeking work
    :cvar VALUE_04: Long-term sick or disabled, those who are receiving
        Incapacity Benefit, Income Support or both; or Employment and
        Support Allowance
    :cvar VALUE_05: Homemaker looking after the family or home and who
        are not working or actively seeking work
    :cvar VALUE_06: Not receiving benefits and who are not working or
        actively seeking work
    :cvar VALUE_07: Unpaid voluntary work who are not working or
        actively seeking work
    :cvar VALUE_08: Retired
    :cvar ZZ: Not Stated (Asked but declined to provide a response)
    """
    VALUE_01 = "01"
    VALUE_02 = "02"
    VALUE_03 = "03"
    VALUE_04 = "04"
    VALUE_05 = "05"
    VALUE_06 = "06"
    VALUE_07 = "07"
    VALUE_08 = "08"
    ZZ = "ZZ"


class OccupationCodingStandard(Enum):
    """
    :cvar NHS_DATA_DICTIONARY_EMPLOYMENT_STATUS:
        http://www.datadictionary.nhs.uk/data_dictionary/attributes/e/emp/employment_status_de.asp
    """
    NHS_DATA_DICTIONARY_EMPLOYMENT_STATUS = "NHS_DATA_DICTIONARY_EMPLOYMENT_STATUS"


@dataclass
class Occupation:
    coding_standard: Optional[OccupationCodingStandard] = field(
        default=None,
        metadata={
            "name": "CodingStandard",
            "type": "Element",
            "namespace": "",
        }
    )
    code: Optional[OccupationCode] = field(
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
