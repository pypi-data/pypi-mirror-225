from enum import Enum

__NAMESPACE__ = "http://www.rixg.org.uk/"


class BloodGroup(Enum):
    """See https://www.datadictionary.nhs.uk/data_dictionary/attributes/p/person/person_blood_group_de.asp

    :cvar A: Blood Group A
    :cvar B: Blood Group B
    :cvar AB: Blood Group AB
    :cvar O: Blood Group O
    """
    A = "A"
    B = "B"
    AB = "AB"
    O = "O"
