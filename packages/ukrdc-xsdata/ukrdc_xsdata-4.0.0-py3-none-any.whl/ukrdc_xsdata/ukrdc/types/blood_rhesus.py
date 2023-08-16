from enum import Enum

__NAMESPACE__ = "http://www.rixg.org.uk/"


class BloodRhesus(Enum):
    """See https://www.datadictionary.nhs.uk/data_dictionary/attributes/p/person/person_rhesus_factor_de.asp

    :cvar POS: RhD-Positive (does have the Rh D antigen)
    :cvar NEG: RhD-Negative (does not have the antigen)
    """
    POS = "POS"
    NEG = "NEG"
