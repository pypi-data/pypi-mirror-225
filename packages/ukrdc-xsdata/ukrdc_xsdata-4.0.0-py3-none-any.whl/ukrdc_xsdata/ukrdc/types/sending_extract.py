from enum import Enum

__NAMESPACE__ = "http://www.rixg.org.uk/"


class SendingExtract(Enum):
    """
    :cvar SURVEY: CSV files produced either by FormStorm scanning or
        sent directly from the SharedHD project
    :cvar PVMIG: Data taken from the PV2 Database
    :cvar HSMIG: Data taken from the HealthShare Database
    :cvar PV: Data sent from Units in PV XML Format
    :cvar RADAR: Data from the RADAR System
    :cvar UKRDC: Data supplied directly in RDA Format
    :cvar MIRTH: Data supplied in RDA Format which has been produced by
        our UKRDC Extract Tool
    :cvar UKRR: Data taken from the UKRR Database
    """
    SURVEY = "SURVEY"
    PVMIG = "PVMIG"
    HSMIG = "HSMIG"
    PV = "PV"
    RADAR = "RADAR"
    UKRDC = "UKRDC"
    MIRTH = "MIRTH"
    UKRR = "UKRR"
